import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:myapp/securityScreen.dart';
import 'package:myapp/settingsScreen.dart';
import 'mainScreen.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    const title = 'SecureAuth';
    return MaterialApp(
        title: title,
        debugShowCheckedModeBanner: false,
        initialRoute: '/securityScreen',
        routes: {
          '/securityScreen': (context) => SecurityScreen(),
          '/mainScreen': (context) => MainScreen(),
          '/settings': (context) => SettingsScreen()
        },
        theme: ThemeData(
            visualDensity: VisualDensity.adaptivePlatformDensity,
            textTheme:
                GoogleFonts.openSansTextTheme(Theme.of(context).textTheme)));
  }
}
