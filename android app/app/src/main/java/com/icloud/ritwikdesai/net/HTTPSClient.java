package com.icloud.ritwikdesai.net;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;

import javax.net.ssl.HttpsURLConnection;

/**
 * Created by ritwikdesai on 10/02/16.
 */
public class HTTPSClient implements TrustStoreInterface {

    public static class InputStreamReader{
        private InputStream inputStream;

        public InputStreamReader(InputStream stream){
            this.inputStream = stream;
        }

        public JSONObject readJSONResponse(){
            JSONObject o = null;

            try{
                BufferedReader reader = new BufferedReader(new java.io.InputStreamReader(this.inputStream));
                StringBuilder builder = new StringBuilder();
                String input;
                while((input = reader.readLine()) != null){
                    builder.append(input);
                }

                reader.close();

                String obj = builder.toString();
                o = new JSONObject(obj);
            }catch (IOException e){
                e.printStackTrace();
            }catch (JSONException e){
                e.printStackTrace();
            }finally {
                return o;
            }
        }
    }

    private TrustStoreInterface storeInterface;
    private URL httpsURL;

    public HTTPSClient(String Url) throws MalformedURLException {
        this(Url,null);
    }
    public HTTPSClient(String Url,TrustStoreInterface policy) throws MalformedURLException {
        if(policy == null) trustPolicy();
        else{
            policy.trustPolicy();
        }
        this.httpsURL = new URL(Url);
    }

    public InputStream getInputStream(){
        InputStream stream = null;
        try {
            HttpsURLConnection conn = (HttpsURLConnection)this.httpsURL.openConnection();
            if(conn != null){
                stream = conn.getInputStream();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }finally {
            return stream;
        }

    }

    @Override
    public void trustPolicy() {
        throw new UnsupportedOperationException("Currently trust policy is not implemented");
    }


}
