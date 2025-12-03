package com.sanctuary.prime.scepter;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Inflate the XML layout (res/layout/activity_main.xml)
        setContentView(R.layout.activity_main);

        // Populate the TextView defined in the layout
        TextView textView = findViewById(R.id.main_text);
        if (textView != null) {
            textView.setText("🌌 SANCTUARY PRIME SCEPTER\n\n✅ Built with our own system\n🔥 No Gradle, no restrictions");
            textView.setTextSize(24);
            int padding = (int) (getResources().getDisplayMetrics().density * 16);
            textView.setPadding(padding, padding, padding, padding);
        }
    }
}
