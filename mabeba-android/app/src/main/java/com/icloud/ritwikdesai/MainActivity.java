package com.icloud.ritwikdesai;

import android.content.Intent;
import android.os.Bundle;
import android.os.SystemClock;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Toast;

import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;
import com.icloud.ritwikdesai.crypto.Crypto;
import com.icloud.ritwikdesai.interfaces.Bridge;
import com.icloud.ritwikdesai.scan.ScannerActivity;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.InputStream;
import java.security.NoSuchAlgorithmException;
import java.security.spec.InvalidKeySpecException;

public class MainActivity extends AppCompatActivity implements Bridge.BridgeInterface {

    private MainActivityFragment mainFragment;
    private WebViewFragment webViewFragment;
    private static final String TAG = "MAIN ACTIVITY";

    private int itemPosition = 0;

    private long t1 =0;
    private  long t2 = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        setUpViews();
        setUpKeyStore();
    }

    private void setUpKeyStore() {
         String alias = "CredentialStore";
         Crypto.initKeyStore(this,alias);
    }

    private void setUpViews() {
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        mainFragment = (MainActivityFragment) getFragmentManager().findFragmentById(R.id.fragment);
        webViewFragment = (WebViewFragment) getFragmentManager().findFragmentById(R.id.fragmentWeb);

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_register) {
            IntentIntegrator integrator = new IntentIntegrator(this);
            integrator.setCaptureActivity(ScannerActivity.class);
            integrator.setOrientationLocked(true);
            integrator.initiateScan();
        }else if(id == R.id.action_reset){
            mainFragment.updateStatus("","");
            resetPeer();
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        IntentResult scanResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, data);
        if (scanResult != null && scanResult.getContents() != null) {
            try{
                JSONObject register = new JSONObject(scanResult.getContents());
                final String tokenUrl = register.getString("token");
                final String salt = register.getString("salt");
                mainFragment.register(tokenUrl,salt);
//                t2 = System.currentTimeMillis();
//                mainFragment.updateStatus("Time: ","" + (t2-t1));

            }catch (JSONException e){
                e.printStackTrace();
                Toast.makeText(getApplicationContext(),"Invalid QR Code",Toast.LENGTH_SHORT).show();
            }
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    @Override
    public JSONObject execute(JSONObject data) throws JSONException {
        if(data.getString("id").equals("peerReady")){
            mainFragment.updateStatus("ID: ",data.getString("data"));
        }else if(data.getString("id").equals("peerConnected")){
            mainFragment.setConnected(true);
            mainFragment.updateStatus("Connected: ",data.getString("data"));
        }else if(data.getString("id").equals("responseToken")){
            if(data.getString("data").equals("Success")){
                mainFragment.updateStatus("","Token Generated Successfully");
            }else{
                mainFragment.updateStatus("","Token Generation Failed");
            }
        }else if(data.getString("id").equals("peerDisconnected")){
            mainFragment.updateStatus("",data.getString("data"));
        }
        else if(data.getString("id").equals("timestamp")){
        }
        return null;
    }

    public void connect(String id){
        webViewFragment.connect(id);
    }

    public void requestToken(JSONObject token,int position){
        itemPosition = position;
        webViewFragment.requestToken(token);
    }

    public void resetPeer(){
        mainFragment.setConnected(false);
        webViewFragment.resetPeer();
    }
}
