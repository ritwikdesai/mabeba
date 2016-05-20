package com.icloud.ritwikdesai.net;

import android.os.AsyncTask;
import android.util.Base64;
import android.util.Log;

import com.icloud.ritwikdesai.crypto.Crypto;
import com.icloud.ritwikdesai.db.UserAccount;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.net.MalformedURLException;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import java.security.spec.InvalidKeySpecException;

import javax.crypto.BadPaddingException;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSession;
import javax.net.ssl.X509TrustManager;

/**
 * Created by ritwikdesai on 10/02/16.
 */
public class RegisterTask extends AsyncTask<String,Void,UserAccount> implements TrustStoreInterface {

    public static interface RegisterListener{
        public void onResultReceived(UserAccount o);
        public void onErrorReceived(String message);
    }

    private RegisterListener registerListener;

    private String errorMsg = "";

    public RegisterTask(RegisterListener listener){
        this.registerListener = listener;
    }

    @Override
    protected UserAccount doInBackground(String... params) {

        UserAccount account = null;

        try {
            HTTPSClient client = new HTTPSClient(params[0],this);
            long t1 = System.currentTimeMillis();
            HTTPSClient.InputStreamReader reader = new HTTPSClient.InputStreamReader(client.getInputStream());
            long t2 = System.currentTimeMillis();
            Log.d("REGISTER","" +(t2-t1));
            JSONObject o = reader.readJSONResponse();
            String encrypted = o.getString("register");

            byte [] aes_key = Crypto.generateAESKey(params[1],params[2],Crypto.ITER_100K,Crypto.KEY_LEN_256);
            byte [] decrypted = Crypto.aesDecrypt(Base64.decode(encrypted,Base64.DEFAULT),aes_key);

            String plain = new String(decrypted,"UTF-8");
            JSONObject data = new JSONObject(plain);
            account = new UserAccount.Builder()
                    .setUsername(data.getString("username"))
                    .setTokenUrl(data.getString("token_url"))
                    .setSite(data.getString("site"))
                    .setSecret(Crypto.encryptWithKeyStore(data.getString("secret"),"CredentialStore")).build();
//                    .setOtpSalt(Crypto.encryptWithKeyStore(data.getString("otp_salt"),"CredentialStore")).build();

        } catch (MalformedURLException e) {
            e.printStackTrace();
            this.errorMsg = e.getMessage();
        }catch (JSONException e){
            e.printStackTrace();
            this.errorMsg = e.getMessage();
        } catch (InvalidKeySpecException e) {
            e.printStackTrace();
            this.errorMsg = e.getMessage();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            this.errorMsg = e.getMessage();
        } catch (NoSuchPaddingException e) {
            e.printStackTrace();
            this.errorMsg = e.getMessage();
        } catch (InvalidKeyException e) {
            e.printStackTrace();
            this.errorMsg = e.getMessage();
        } catch (InvalidAlgorithmParameterException e) {
            e.printStackTrace();
            this.errorMsg = e.getMessage();
        } catch (IllegalBlockSizeException e) {
            e.printStackTrace();
            this.errorMsg = e.getMessage();
        } catch (BadPaddingException e) {
            e.printStackTrace();
            this.errorMsg = e.getMessage();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
            this.errorMsg = e.getMessage();
        }finally {
            return account;
        }

    }


    @Override
    protected void onPostExecute(UserAccount userAccount) {
        if(userAccount == null){
            registerListener.onErrorReceived(this.errorMsg);
        }else{
            registerListener.onResultReceived(userAccount);
        }
    }

    @Override
    public void trustPolicy() {
        try {
            HttpsURLConnection.setDefaultHostnameVerifier(new HostnameVerifier(){
                public boolean verify(String hostname, SSLSession session) {
                    return true;
                }});
            SSLContext context = SSLContext.getInstance("TLS");
            context.init(null, new X509TrustManager[]{new X509TrustManager(){
                public void checkClientTrusted(X509Certificate[] chain,
                                               String authType) throws CertificateException {}
                public void checkServerTrusted(X509Certificate[] chain,
                                               String authType) throws CertificateException {}
                public X509Certificate[] getAcceptedIssuers() {
                    return new X509Certificate[0];
                }}}, new SecureRandom());
            HttpsURLConnection.setDefaultSSLSocketFactory(
                    context.getSocketFactory());
        } catch (Exception e) { // should never happen
            e.printStackTrace();
        }
    }
}
