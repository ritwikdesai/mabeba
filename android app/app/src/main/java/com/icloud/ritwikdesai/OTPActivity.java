package com.icloud.ritwikdesai;

import android.animation.ObjectAnimator;
import android.os.Bundle;
import android.os.Handler;
import android.os.StrictMode;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.animation.LinearInterpolator;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.icloud.ritwikdesai.crypto.Crypto;

/**
 * Created by ritwikdesai on 07/03/16.
 */
public class OTPActivity extends AppCompatActivity {

    private Toolbar toolbar;
    private TextView textViewOTP;
    private TextView textViewUsername;
    private ProgressBar progressBar;

    private Handler handler;
    private Runnable otpUpdater;

    private Bundle bundle;
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setUpViews();
    }

    private void setUpViews(){
        setContentView(R.layout.otp_activity);

        toolbar = (Toolbar)findViewById(R.id.toolbar);
        toolbar.setTitle(String.format("One Time Password: "+getValue("site")));
        setSupportActionBar(toolbar);

        progressBar = (ProgressBar) findViewById(R.id.progressBar);

        textViewUsername = (TextView)findViewById(R.id.username);
        textViewUsername.setText(getValue("username"));

        textViewOTP = (TextView) findViewById(R.id.textViewOTP);
        textViewOTP.setText(getOTP(getValue("otp_salt")));
        handler = new Handler();
        otpUpdater = new Runnable() {
            @Override
            public void run() {
                int progress =  (int) (System.currentTimeMillis() / 1000) % 30 ;
                progressBar.setProgress(progress*100);

                textViewOTP.setText(getOTP(getValue("otp_salt")));

                ObjectAnimator animation = ObjectAnimator.ofInt(progressBar, "progress", (progress+1)*100);
                animation.setDuration(1000);
                animation.setInterpolator(new LinearInterpolator());
                animation.start();

                handler.postDelayed(this, 1000);
            }
        };


    }

    private String getOTP(String otp_salt) {
        if(otp_salt == "NA") return otp_salt;
        return Crypto.generateOTP(otp_salt);
    }

    @Override
    protected void onResume() {
        super.onResume();
        handler.postDelayed(otpUpdater,1000);
    }

    public String getValue(String key ) {
        if (bundle == null) {
            bundle = getIntent().getExtras();
        }
        return bundle.getString(key,"NA");
    }
}
