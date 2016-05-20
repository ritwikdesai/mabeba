package com.icloud.ritwikdesai.interfaces;

import android.content.Context;
import android.webkit.JavascriptInterface;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by ritwikdesai on 03/03/16.
 */
public class Bridge {

    public static interface BridgeInterface{
        public JSONObject execute(JSONObject data) throws JSONException;
    }

    public BridgeInterface bridgeInterface;

    public Bridge(BridgeInterface i){
        bridgeInterface = i;
    }

    @JavascriptInterface
    public String send(String data){
        try{
            JSONObject obj = new JSONObject(data);
            JSONObject result = bridgeInterface.execute(obj);
            return (result == null)?"":result.toString();
        }catch (JSONException e){
            e.printStackTrace();
        }

        return "";
    }

}
