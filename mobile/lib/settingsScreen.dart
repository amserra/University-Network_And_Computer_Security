import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:passcode_screen/circle.dart';
import 'package:passcode_screen/passcode_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:local_auth/local_auth.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SettingsScreen extends StatefulWidget {
  @override
  _SettingsScreenState createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  var localAuth = LocalAuthentication();
  final StreamController<bool> verificationNotifier =
      StreamController<bool>.broadcast();
  final storage = new FlutterSecureStorage();
  // state
  bool passcodeEnabled = false;
  bool biometricEnabled = false;
  bool supportsBiometric = false;
  String passcode;

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

  Future<bool> checkSupportsBiometric() async {
    bool canCheckBiometrics = await localAuth.canCheckBiometrics;
    return canCheckBiometrics;
  }

  @override
  void initState() {
    super.initState();

    hasPasscode().then((hasPasscode) => {
          if (hasPasscode)
            setState(() {
              passcodeEnabled = true;
            })
        });

    hasBiometric().then((hasBiometric) => {
          if (hasBiometric)
            setState(() {
              biometricEnabled = true;
            })
        });

    checkSupportsBiometric().then((canCheckBiometrics) => {
          if (canCheckBiometrics)
            setState(() {
              supportsBiometric = true;
            })
        });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: Color.fromRGBO(30, 30, 30, 1),
        appBar: AppBar(
            backgroundColor: Color.fromRGBO(36, 36, 36, 1),
            title: Text('SecureAuth'),
            elevation: 20.0),
        body: Container(
          padding: EdgeInsets.only(left: 20, top: 20, right: 20),
          child: Column(
            children: [
              Text("You can lock your app with: passcode, biometrics or none",
                  style: TextStyle(color: Colors.white, fontSize: 20)),
              SizedBox(height: 50),
              SwitchListTile.adaptive(
                  title:
                      Text("Passcode", style: TextStyle(color: Colors.white)),
                  value: passcodeEnabled,
                  onChanged: (newValue) async {
                    if (newValue != passcodeEnabled) {
                      if (newValue) {
                        showLockScreen(context);
                        bool didNotCancel =
                            await verificationNotifier.stream.first;
                        if (didNotCancel) {
                          setState(() {
                            passcodeEnabled = true;
                            biometricEnabled = false;
                          });
                          setPrefs(true, false);
                        }
                      } else {
                        await storage.delete(key: 'passcode');
                        setState(() {
                          passcodeEnabled = false;
                        });
                        setPrefs(false, false);
                      }
                    }
                  }),
              SwitchListTile.adaptive(
                  title:
                      Text("Biometrics", style: TextStyle(color: Colors.white)),
                  value: biometricEnabled && supportsBiometric,
                  onChanged: (newValue) async {
                    if (newValue != biometricEnabled) {
                      if (newValue && supportsBiometric) {
                        bool isAuthenticated = await authenticateUser();
                        if (isAuthenticated) {
                          setState(() {
                            passcodeEnabled = false;
                            biometricEnabled = true;
                          });
                          setPrefs(false, true);
                        }
                        // save in sharedprefs
                      } else if (!newValue) {
                        setState(() {
                          biometricEnabled = false;
                        });
                        setPrefs(false, false);
                      }
                    }
                  })
            ],
          ),
        ));
  }

  showLockScreen(BuildContext context) {
    Navigator.push(
        context,
        PageRouteBuilder(
          pageBuilder: (context, animation, secondaryAnimation) =>
              PasscodeScreen(
                  title: Text(
                    'Set Passcode',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: Colors.white, fontSize: 28),
                  ),
                  circleUIConfig: CircleUIConfig(
                      fillColor: Color.fromRGBO(154, 205, 50, 0.8)),
                  passwordEnteredCallback: onPasscodeEntered,
                  cancelButton: Text(
                    'Cancel',
                    style: const TextStyle(fontSize: 16, color: Colors.white),
                    semanticsLabel: 'Cancel',
                  ),
                  deleteButton: Text(
                    'Delete',
                    style: const TextStyle(fontSize: 16, color: Colors.white),
                    semanticsLabel: 'Delete',
                  ),
                  shouldTriggerVerification: verificationNotifier.stream,
                  backgroundColor: Colors.black.withOpacity(0.8),
                  cancelCallback: onPasscodeCancelled,
                  passwordDigits: 4),
        ));
  }

  onPasscodeEntered(String enteredPasscode) async {
    await storage.write(key: 'passcode', value: enteredPasscode);
    verificationNotifier.add(true);
    setState(() {
      passcode = enteredPasscode;
    });
  }

  onPasscodeCancelled() {
    verificationNotifier.add(false);
    Navigator.maybePop(context);
  }

  @override
  void dispose() {
    verificationNotifier.close();
    super.dispose();
  }

  Future<void> setPrefs(bool hasPasscode, bool hasBiometric) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setBool('hasPasscode', hasPasscode);
    prefs.setBool('hasBiometric', hasBiometric);
  }

  Future<bool> authenticateUser() async {
    bool isAuthenticated = false;
    try {
      isAuthenticated = await localAuth.authenticateWithBiometrics(
          localizedReason: "Please authenticate to start using biometrics",
          useErrorDialogs: true,
          stickyAuth: true);
    } on PlatformException catch (e) {
      print(e);
    }

    return isAuthenticated;
  }
}
