import 'dart:async';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:passcode_screen/circle.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:passcode_screen/passcode_screen.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:local_auth/local_auth.dart';

class SecurityScreen extends StatefulWidget {
  @override
  _SecurityScreenState createState() => _SecurityScreenState();
}

class _SecurityScreenState extends State<SecurityScreen> {
  // none OR passcode OR biometric
  final StreamController<bool> _verificationNotifier =
      StreamController<bool>.broadcast();
  final storage = FlutterSecureStorage();
  final LocalAuthentication localAuthentication = LocalAuthentication();
  String authType = 'none';
  String passcode;

  @override
  void initState() {
    super.initState();

    WidgetsBinding.instance.addPostFrameCallback(postBuildCallback);
  }

  Future<void> loadSettings() async {
    await hasPasscode().then((hasPasscode) => {
          if (hasPasscode)
            setState(() {
              authType = "passcode";
            })
        });

    await loadPasscode().then((value) => {
          if (value != null)
            {
              setState(() {
                passcode = value;
              })
            }
        });

    await hasBiometric().then((hasBiometric) => {
          if (hasBiometric)
            setState(() {
              authType = "biometric";
            })
        });
  }

  @override
  Widget build(BuildContext context) {
    if (authType == 'none') {
      return Container(
          color: Color.fromRGBO(30, 30, 30, 1),
          child: SizedBox(height: 0, width: 0));
    } else if (authType == 'biometric') {
      return Container(
          color: Color.fromRGBO(30, 30, 30, 1),
          child: SizedBox(height: 0, width: 0));
    } else if (authType == 'passcode') {
      // else, it's passcode
      return Container(
          child: PasscodeScreen(
              title: Text(
                "Enter Passcode",
                style: TextStyle(color: Colors.white, fontSize: 30),
              ),
              backgroundColor: Color.fromRGBO(30, 30, 30, 1),
              passwordDigits: 4,
              passwordEnteredCallback: onPasscodeEntered,
              cancelButton: SizedBox(width: 0, height: 0),
              deleteButton: Text("Delete"),
              shouldTriggerVerification: _verificationNotifier.stream,
              isValidCallback: () =>
                  Navigator.popAndPushNamed(context, '/mainScreen'),
              circleUIConfig: CircleUIConfig(
                  fillColor: Color.fromRGBO(154, 205, 50, 0.8))));
    } else {
      return Container(
          color: Color.fromRGBO(30, 30, 30, 1),
          child: SizedBox(height: 0, width: 0));
    }
  }

  void postBuildCallback(_) async {
    await loadSettings();
    if (authType == "biometric") {
      authenticateUser().then((isAuthenticated) => {
            if (isAuthenticated)
              Navigator.popAndPushNamed(context, '/mainScreen')
            else
              exit(1)
          });
    } else if (authType == "none") {
      Navigator.popAndPushNamed(context, '/mainScreen');
    }
  }

  @override
  void dispose() {
    _verificationNotifier.close();
    super.dispose();
  }

  Future<String> loadPasscode() async {
    String passcode = await storage.read(key: 'passcode');
    return passcode;
  }

  Future<bool> hasPasscode() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    bool hasPasscode = prefs.getBool("hasPasscode") ?? false;
    return hasPasscode;
  }

  Future<bool> hasBiometric() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    bool hasBiometric = prefs.getBool("hasBiometric") ?? false;
    return hasBiometric;
  }

  onPasscodeEntered(String enteredPasscode) {
    // Testing:
    // bool isValid = '1234' == enteredPasscode;
    bool isValid = passcode == enteredPasscode;
    _verificationNotifier.add(isValid);
  }

  Future<bool> authenticateUser() async {
    bool isAuthenticated = false;
    try {
      isAuthenticated = await localAuthentication.authenticateWithBiometrics(
          localizedReason: "Please authenticate to enter the app",
          useErrorDialogs: true,
          stickyAuth: true);
    } on PlatformException catch (e) {
      print(e);
    }

    return isAuthenticated;
  }
}
