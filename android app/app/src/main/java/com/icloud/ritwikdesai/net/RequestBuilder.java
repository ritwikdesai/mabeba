package com.icloud.ritwikdesai.net;

import com.icloud.ritwikdesai.crypto.Crypto;

import org.json.JSONException;
import org.json.JSONObject;

import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

import javax.crypto.BadPaddingException;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;

/**
 * Created by ritwikdesai on 18/02/16.
 */
public class RequestBuilder {
    private String tokenUrl;
    private String username;
    private String secret;
    private String timestamp;

    public RequestBuilder(){

    }

    public RequestBuilder setSecret(String secret) {
        this.secret = secret;
        return this;
    }

    public RequestBuilder setTimestamp(String timestamp) {
        this.timestamp = timestamp;
        return this;
    }

    public RequestBuilder setTokenUrl(String tokenUrl) {
        this.tokenUrl = tokenUrl;
        return this;
    }

    public RequestBuilder setUsername(String username) {
        this.username = username;
        return this;
    }

    public String getSecret() {
        return secret;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public String getTokenUrl() {
        return tokenUrl;
    }

    public String getUsername() {
        return username;
    }

    public JSONObject build() throws JSONException {
        JSONObject o = null;
        try {
//            o = new JSONObject();
//            o.put("url",this.tokenUrl);
//            o.put("username",this.username);
//            String msg = this.username + "," + this.timestamp;
//            o.put("data",Crypto.toBase64Encoded(Crypto.aesEncrypt(msg.getBytes(),Crypto.toByteArray(this.secret))));

            o = new JSONObject();
            o.put("url",this.tokenUrl);
            o.put("username",this.username);
            o.put("timestamp",""+this.timestamp);
            String msg = this.username + "," + this.timestamp;
            byte[] key = Crypto.hmac256(this.secret,this.username+this.timestamp);
            o.put("data",Crypto.toBase64Encoded(Crypto.aesEncrypt(msg.getBytes(),key)));

        } catch (InvalidAlgorithmParameterException e) {
            e.printStackTrace();
        } catch (InvalidKeyException e) {
            e.printStackTrace();
        } catch (NoSuchPaddingException e) {
            e.printStackTrace();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (BadPaddingException e) {
            e.printStackTrace();
        } catch (IllegalBlockSizeException e) {
            e.printStackTrace();
        }finally {
            return o;
        }
    }
}
