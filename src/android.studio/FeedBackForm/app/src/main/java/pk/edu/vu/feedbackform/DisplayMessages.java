package pk.edu.vu.feedbackform;

import android.content.Context;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

public class DisplayMessages extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display_messages);
    }

    public void viewFeedback(View view){
        /*Step#1: Validate the content*/
        EditText editEmail = (EditText) findViewById(R.id.editEmailSearch);
        if(editEmail.getText() == null || editEmail.getText().toString().length() <= 0){
            editEmail.setError("Invalid email address");
            return;
        }
        String email = editEmail.getText().toString();
        String fileName = email.replace('@','_') + ".json";

        String output = readFileAsString(this.getApplicationContext(),fileName);
        if(output == null || output.length() <= 0){
            editEmail.setError("No record found");
        }
        EditText editFeedback = (EditText) findViewById(R.id.editFeedback);
        try {
            JSONObject json = new JSONObject(output);
            StringBuilder sb = new StringBuilder();
            sb.append("Email: "+json.getString("email")+"\n");
            sb.append("Subject: "+json.getString("subject")+"\n");
            sb.append("Feedback: "+json.getString("body")+"\n");
            editFeedback.setText(sb.toString());
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }

    private String readFileAsString(Context context, String fileName){
        BufferedReader in = null;
        String line = "";
        String output = "";
        StringBuilder sb = new StringBuilder();
        try {
            in = new BufferedReader(new FileReader(new File(context.getFilesDir(), fileName)));
            while((line = in.readLine()) != null){
                sb.append(line);
                output = (line != null)?line:"";
            }
            return output;
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }
}
