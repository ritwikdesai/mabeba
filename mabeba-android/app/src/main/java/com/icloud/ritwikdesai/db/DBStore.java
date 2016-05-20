package com.icloud.ritwikdesai.db;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.hardware.usb.UsbRequest;
import android.util.Pair;

import com.icloud.ritwikdesai.crypto.Crypto;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

/**
 * Created by ritwikdesai on 18/02/16.
 */
public class DBStore {

    private static DBStore instance;

    private final Context context;

    private DBStore(Context c){
        this.context = c;
    }


    public ArrayList<UserAccount> getUserAccounts(){
        DBStoreHelper helper = new DBStoreHelper(context);
        return helper.getUserAccounts();
    }

    public boolean deleteUserAccount(UserAccount o){
        DBStoreHelper helper = new DBStoreHelper(context);
        return helper.delete(o);
    }

    public static DBStore getInstance(Context c){
        if(instance == null) instance = new DBStore(c);
        return instance;
    }

    public static class DBStoreHelper extends SQLiteOpenHelper{

        private static final String DB_NAME = "SemXDb";
        private static final String TABLE_NAME = "SITES";
        private static final int DB_VERSION = 1;

        private static final String COL_ID = "id";
        private static final String COL_SITE = "site_name";
        private static final String COL_USER_ID = "username";
        private static final String COL_TOKEN_URL = "token_url";
        private static final String COL_SECRET = "secret";
        private static final String COL_OTP_SALT = "otp_salt";

        private Context context;

        public DBStoreHelper(Context context){
            super(context,DB_NAME,null,DB_VERSION);
        }

        @Override
        public void onCreate(SQLiteDatabase db) {
            StringBuilder builder = new StringBuilder();
            builder.append("CREATE TABLE " + TABLE_NAME);
            builder.append("( " + COL_ID + " INTEGER PRIMARY KEY, ");
            builder.append( COL_SITE + " TEXT NOT NULL, ");
            builder.append( COL_USER_ID + " TEXT NOT NULL, ");
            builder.append( COL_TOKEN_URL + " TEXT NOT NULL, ");
            builder.append( COL_SECRET + " TEXT NOT NULL, ");
//            builder.append( COL_OTP_SALT + " TEXT NOT NULL, ");
            builder.append("UNIQUE ("+COL_SITE+" , " + COL_USER_ID + ")");
            builder.append(")");
            db.execSQL(builder.toString());

        }

        @Override
        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
            db.execSQL("DROP TABLE IF EXISTS " + TABLE_NAME);
            onCreate(db);
        }

        public void insert(UserAccount account){
            SQLiteDatabase db = this.getWritableDatabase();

            ContentValues values = new ContentValues();
            values.put(COL_ID,System.currentTimeMillis());
            values.put(COL_SITE,account.getSite());
            values.put(COL_USER_ID,account.getUsername());
            values.put(COL_TOKEN_URL,account.getTokenUrl());
            values.put(COL_SECRET, account.getSecret());
//            values.put(COL_OTP_SALT,account.getOtpSalt());

            db.insert(TABLE_NAME,null,values);
            db.close();
        }

        public ArrayList<UserAccount> getUserAccounts(){
            ArrayList<UserAccount> accounts = new ArrayList<UserAccount>();
            String query  = "SELECT * FROM " + TABLE_NAME;
            SQLiteDatabase db = this.getReadableDatabase();

            Cursor cursor = db.rawQuery(query,null);
            if(cursor.moveToFirst()){
                do{
                    UserAccount o = new UserAccount.Builder()
                            .setSite(cursor.getString(1))
                            .setUsername(cursor.getString(2))
                            .setTokenUrl(cursor.getString(3))
                            .setSecret(cursor.getString(4))
//                            .setOtpSalt(cursor.getString(5))
                            .build();

                    accounts.add(o);

                }while (cursor.moveToNext());
            }
            db.close();

            return accounts;
        }

        public boolean delete(UserAccount o) {
            SQLiteDatabase db = this.getWritableDatabase();
            int row = db.delete(TABLE_NAME,COL_SITE + " =? AND " + COL_USER_ID +" =?",new String[]{o.getSite(),o.getUsername()});
            return (row == 1);
        }
    }
}
