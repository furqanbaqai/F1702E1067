package pk.edu.vu.feedbackform;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;


public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void viewFeedback(View view){
        Intent intent = new Intent(this,DisplayMessages.class);
        startActivity(intent);
    }

    /**
     * Procedure which will be triggered when SAVE button is pressed
     * @param view
     */
    public void saveFeedback(View view){
        //Context context = this.getApplicationContext();
        /*Step#1: Get all controls from the UI */
        EditText editEmail = (EditText) findViewById(R.id.editEmailSearch);
        EditText editSubject = (EditText) findViewById(R.id.editSubject);
        EditText editBody = (EditText) findViewById(R.id.editBody);

        /*Validate fields and save content*/
        if(!validateFields(editEmail,editSubject,editBody)){
            // TODO! Save the content in the file
            String fileName = emailToFileName(editEmail.getText().toString());
            String jsonText = getJsonString(editEmail.getText().toString(),
                    editSubject.getText().toString(),
                        editBody.getText().toString());
            writeStringInAFile(jsonText,fileName);
            // Clear the form
            editBody.setText("");
            editEmail.setText("");
            editSubject.setText("");
        }

    }

    public boolean validateFields(EditText editEmail, EditText editSubject, EditText editBody){
        boolean haveError = false;
         /* Check email address */
        if(editEmail.getText() == null || editEmail.getText().toString().length() <= 0){
            editEmail.setError("Field can not be empty");
            haveError = true;
        }else{
            // Check for email address syntax
            // TODO! Validate email address syntax
            // haveError = true;
        }

        /*Check subject*/
        if(editSubject.getText() == null  || editSubject.getText().toString().length() <= 0) {
            editSubject.setError("Field can not be empty");
            haveError = true;
        }

        /*Check body*/
        if(editBody.getText() == null || editSubject.getText().toString().length() <= 0){
            editBody.setError("Field can not be null");
            haveError = true;
        }
        return haveError;
    }

    private void writeStringInAFile( final String fileContents, String fileName){
        try {
            // FileWriter out = new FileWriter(new File(context.getFilesDir(),fileName));
            FileOutputStream out = openFileOutput(fileName,Context.MODE_PRIVATE | Context.MODE_APPEND);
            out.write((fileContents+"\n").getBytes());
            out.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private String readFileAsString(Context context, String fileName){
        BufferedReader in = null;
        String line = "";

        try {
            in = new BufferedReader(new FileReader(new File(context.getFilesDir(), fileName)));
            while((line = in.readLine()) != null);
            return line;
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    private String emailToFileName(String emailAdd){
        return emailAdd.replace('@','_') + ".json";
    }

    private String getJsonString(String email, String subject, String body){
        JSONObject json = new JSONObject();
        try {
            json.put("email",email);
            json.put("subject",subject);
            json.put("body",body);
            return json.toString();
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return null;
    }
}
