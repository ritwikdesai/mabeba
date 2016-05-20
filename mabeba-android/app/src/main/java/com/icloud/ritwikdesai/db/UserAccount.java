package com.icloud.ritwikdesai.db;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by ritwikdesai on 10/02/16.
 */
public class UserAccount {
    private String tokenUrl;
    private String username;
    private String secret;
    //private String otpSalt;
    private String site;

    public static UserAccount createUserAccount(JSONObject o) throws JSONException {
        Log.d("Accout Object",o.toString());

        Builder accountBuilder = new Builder()
//                .setOtpSalt(o.getString("otp_salt"))
                .setSecret(o.getString("secret"))
                .setTokenUrl(o.getString("token_url"))
                .setUsername(o.getString("username"))
                .setSite(o.getString("site"));
        return accountBuilder.build();

    }

    public static class Builder{
        private String tokenUrl;
        private String username;
        private String secret;
//        private String otpSalt;
        private String site;

        public Builder(){

        }

        public Builder setUsername(String username) {
            this.username = username;
            return this;
        }

        public Builder setTokenUrl(String tokenUrl) {
            this.tokenUrl = tokenUrl;
            return this;
        }

        public Builder setSecret(String secret) {
            this.secret = secret;
            return this;
        }

//        public Builder setOtpSalt(String otpSalt) {
//            this.otpSalt = otpSalt;
//            return this;
//        }

        public String getSite() {
            return site;
        }

        public Builder setSite(String site) {
            this.site = site;
            return this;
        }

        public UserAccount build(){
            UserAccount o = new UserAccount();
            o.setUsername(this.username);
            o.setTokenUrl(this.tokenUrl);
            o.setSecret(this.secret);
//            o.setOtpSalt(this.otpSalt);
            o.setSite(this.site);
            return o;
        }
    }

//    public String getOtpSalt() {
//        return otpSalt;
//    }

    public String getSecret() {
        return secret;
    }

    public String getTokenUrl() {
        return tokenUrl;
    }

    public String getUsername() {
        return username;
    }

    public String getSite() {
        return site;
    }

//    protected void setOtpSalt(String otpSalt) {
//        this.otpSalt = otpSalt;
//    }

    protected void setSecret(String secret) {
        this.secret = secret;
    }

    protected void setTokenUrl(String tokenUrl) {
        this.tokenUrl = tokenUrl;
    }

    protected void setUsername(String username) {
        this.username = username;
    }

    protected void setSite(String site) {
        this.site = site;
    }

    @Override
    public String toString() {
        return "Account: "+getSite() +" " + getUsername() + " "+ getTokenUrl() + " " + getSecret();
    }
}
