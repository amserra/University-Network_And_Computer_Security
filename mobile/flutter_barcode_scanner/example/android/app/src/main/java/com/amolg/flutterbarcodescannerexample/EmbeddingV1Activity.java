package com.amolg.flutterbarcodescannerexample;

import android.os.Bundle;
import io.flutter.app.FlutterActivity;
import androidx.annotation.NonNull;
import io.flutter.embedding.android.FlutterFragmentActivity;
import io.flutter.embedding.engine.FlutterEngine;
import io.flutter.plugins.GeneratedPluginRegistrant;

public class EmbeddingV1Activity extends FlutterFragmentActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        GeneratedPluginRegistrant.registerWith(new FlutterEngine(this));
    }
}