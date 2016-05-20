package com.icloud.ritwikdesai;

/**
 * Created by ritwikdesai on 04/03/16.
 */
import android.content.Context;
import android.content.DialogInterface;
import android.support.v7.app.AlertDialog;
import android.text.InputType;
import android.text.method.PasswordTransformationMethod;
import android.widget.EditText;
import android.widget.Toast;

/**
 * Created by ritwikdesai on 11/02/16.
 */
public class PasswordDialog {

    public static interface PasswordReceivedListener{
        public void onReceive(String password);
    }

    PasswordReceivedListener listener;
    Context context;
    public PasswordDialog(Context context, PasswordReceivedListener listener){
        this.context = context;
        this.listener = listener;

    }

    private AlertDialog build(){
        final EditText editText = new EditText(context);
        editText.setInputType(InputType.TYPE_TEXT_VARIATION_PASSWORD);
        editText.setTransformationMethod(PasswordTransformationMethod.getInstance());

        AlertDialog.Builder builder = new AlertDialog.Builder(context)
                .setTitle("Authenticate")
                .setMessage("Enter your password")
                .setView(editText)
                .setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        listener.onReceive(editText.getText().toString());
                    }
                });

        return builder.create();
    }

    public void show(){
        build().show();
    }


}