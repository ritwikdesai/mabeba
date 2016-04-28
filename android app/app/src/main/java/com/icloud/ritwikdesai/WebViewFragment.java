package com.icloud.ritwikdesai;

import android.app.Fragment;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebView;
import android.widget.Toast;

import com.icloud.ritwikdesai.interfaces.Bridge;

import org.json.JSONObject;

/**
 * Created by ritwikdesai on 03/03/16.
 */
public class WebViewFragment extends Fragment{

    private WebView webView;
    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        WebView.setWebContentsDebuggingEnabled(true);
        View v = inflater.inflate(R.layout.fragment_web,container,false);
        webView = (WebView) v.findViewById(R.id.webView);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.addJavascriptInterface(new Bridge((Bridge.BridgeInterface)getActivity()),"bridge");
        webView.loadUrl("file:///android_asset/index.html");
        return v;
    }

    public void connect(String id){
      webView.loadUrl("javascript:connectPeer('"+ id +"');");
    }

    public void requestToken(JSONObject token){

        webView.loadUrl("javascript:triggerToken('" +
                token.optString("url","") +"','"+
                token.optString("username","") +"','"+
                token.optString("timestamp","") +"','"+
                token.optString("data","")+"');");
    }

    public void resetPeer(){
        webView.loadUrl("javascript:resetPeer();");
    }
}
