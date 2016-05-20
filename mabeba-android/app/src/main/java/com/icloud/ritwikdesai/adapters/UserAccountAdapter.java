package com.icloud.ritwikdesai.adapters;

import android.content.Context;
import android.util.ArraySet;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ListAdapter;
import android.widget.TextView;

import com.icloud.ritwikdesai.R;
import com.icloud.ritwikdesai.db.UserAccount;

import java.util.ArrayList;

/**
 * Created by ritwikdesai on 04/03/16.
 */
public class UserAccountAdapter extends BaseAdapter {

    private ArrayList<UserAccount> accounts;
    private Context context;
    public UserAccountAdapter(Context context,ArrayList<UserAccount> accounts){
        this.accounts = accounts;
        this.context = context;
    }

    public void update(ArrayList<UserAccount> accounts){
        this.accounts = accounts;
        notifyDataSetChanged();
    }

    @Override
    public int getCount() {
        return accounts.size();
    }

    @Override
    public UserAccount getItem(int position) {
        return accounts.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        UserAccount o = getItem(position);
        if(convertView == null){
            LayoutInflater inflater = (LayoutInflater) this.context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            convertView = inflater.inflate(R.layout.account_row, null);
        }

        TextView siteTextView = (TextView) convertView.findViewById(R.id.siteName);
        siteTextView.setText(o.getSite());
        TextView usernameTextView = (TextView) convertView.findViewById(R.id.username);
        usernameTextView.setText(o.getUsername());

        return convertView;
    }
}
