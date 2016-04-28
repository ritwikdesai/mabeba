package com.icloud.ritwikdesai;

import android.app.AlertDialog;
import android.app.Dialog;
import android.app.Fragment;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.TextView;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;
import com.icloud.ritwikdesai.adapters.UserAccountAdapter;
import com.icloud.ritwikdesai.crypto.Crypto;
import com.icloud.ritwikdesai.db.DBStore;
import com.icloud.ritwikdesai.db.UserAccount;
import com.icloud.ritwikdesai.net.RegisterTask;
import com.icloud.ritwikdesai.net.RequestBuilder;
import com.icloud.ritwikdesai.scan.ScannerActivity;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

/**
 * A placeholder fragment containing a simple view.
 */
public class MainActivityFragment extends Fragment implements AdapterView.OnItemClickListener,AdapterView.OnItemLongClickListener,RegisterTask.RegisterListener,PasswordDialog.PasswordReceivedListener {

    //
    private PasswordDialog passwordDialog;
    private ProgressDialog progressDialog;
    private Bundle bundle;
    //

    private String TAG = "MainActivityFragment";
    private TextView statusLabelView;
    private TextView statusTextView;
    private ListView listView;
    private ProgressBar progressBar;

    private boolean isConnected = false;
    private UserAccountAdapter adapter;

    private DBStore dbStore;

    public MainActivityFragment() {
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_main, container, false);
        statusLabelView = (TextView)v.findViewById(R.id.statusLabel);
        statusTextView = (TextView) v.findViewById(R.id.statusText);
        statusTextView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                TextView view = (TextView)v;
                if(view.getText().toString().equals("Disconnected")){
                    updateStatus("","");
                    ((MainActivity)getActivity()).resetPeer();
                }
            }
        });
        listView = (ListView) v.findViewById(R.id.accountListView);
        listView.setOnItemClickListener(this);
        listView.setOnItemLongClickListener(this);
        progressBar = (ProgressBar) v.findViewById(R.id.loading_spinner);

        dbStore = DBStore.getInstance(getActivity().getApplicationContext());

        return v;
    }

    @Override
    public void onResume() {
        super.onResume();
        if(adapter == null){
            adapter = new UserAccountAdapter(getActivity().getApplicationContext(),dbStore.getUserAccounts());
            listView.setAdapter(adapter);
        }else {
            adapter.update(dbStore.getUserAccounts());
        }

    }

    public void updateStatus(final String statusLabel, final String statusText){

        getActivity().runOnUiThread(new Runnable() {
            @Override
            public void run() {
                if(statusText == ""){
                    progressBar.setVisibility(View.VISIBLE);
                }else{
                    progressBar.setVisibility(View.GONE);
                }
                statusLabelView.setText(statusLabel);
                statusTextView.setText(statusText);
            }
        });

    }

    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
        if(!isConnected){
            scan();
        }else{

            UserAccount o = adapter.getItem(position);
            Log.d(TAG,o.getSecret());
            RequestBuilder builder = new RequestBuilder();
            builder.setSecret(Crypto.decryptWithKeyStore(o.getSecret(),"CredentialStore"));
            builder.setUsername(o.getUsername());
            builder.setTokenUrl(o.getTokenUrl());
            builder.setTimestamp(String.valueOf(System.currentTimeMillis()/1000));
            try {
                JSONObject object = builder.build();
                ((MainActivity)getActivity()).requestToken(object,position);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }

    private void scan() {
        IntentIntegrator intentIntegrator = IntentIntegrator.forFragment(this);
        intentIntegrator.setCaptureActivity(ScannerActivity.class);
        intentIntegrator.setOrientationLocked(true);
        intentIntegrator.initiateScan();
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        IntentResult scanResult = IntentIntegrator.parseActivityResult(requestCode,resultCode,data);
        if(scanResult != null){
            String id = scanResult.getContents();
            updateStatus("","");
            ((MainActivity)getActivity()).connect(id);
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    public void setConnected(boolean what){
        isConnected = what;
    }

//    public void startOTP(int position){
//        UserAccount o = adapter.getItem(position);
//
//        Intent intent = new Intent(getActivity(),OTPActivity.class);
//        intent.putExtra("site",o.getSite());
//        intent.putExtra("username",o.getUsername());
//        intent.putExtra("otp_salt",Crypto.decryptWithKeyStore(o.getOtpSalt(),"CredentialStore"));
//        startActivity(intent);
//    }

    public void register(String tokenUrl,String salt){
        bundle = new Bundle();
        bundle.putString("Token Url",tokenUrl);
        bundle.putString("Salt",salt);
        passwordDialog = new PasswordDialog(getActivity(),this);
        passwordDialog.show();
    }


    @Override
    public void onResultReceived(UserAccount o) {
        Log.d(TAG,o.getSecret());
        DBStore.DBStoreHelper helper = new DBStore.DBStoreHelper(getActivity().getApplicationContext());
        helper.insert(o);
        progressDialog.dismiss();
        adapter.update(dbStore.getUserAccounts());

    }

    @Override
    public void onErrorReceived(String message) {

    }

    @Override
    public void onReceive(String password) {
        progressDialog = ProgressDialog.show(getActivity(),"Loading","Getting Registration Details");
        RegisterTask task = new RegisterTask(this);
        task.execute(bundle.getString("Token Url"),password,bundle.getString("Salt"));
    }

    @Override
    public boolean onItemLongClick(AdapterView<?> parent, View view, final int position, long id) {
        AlertDialog.Builder alert = new AlertDialog.Builder(
                getActivity());
        alert.setTitle("Delete!!");
        alert.setMessage("Are you sure to delete?");
        alert.setPositiveButton("YES", new DialogInterface.OnClickListener() {

            @Override
            public void onClick(DialogInterface dialog, int which) {
                UserAccount o = adapter.getItem(position);
                if(dbStore.deleteUserAccount(o)){
                    adapter.update(dbStore.getUserAccounts());
                }
                dialog.dismiss();

            }
        });
        alert.setNegativeButton("NO", new DialogInterface.OnClickListener() {

            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        });

        alert.show();
        return true;
    }
}
