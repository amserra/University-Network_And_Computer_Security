import 'package:flutter/services.dart';
import 'package:pbkdf2_dart/pbkdf2_dart.dart';
import 'package:crypto/crypto.dart';
import 'package:convert/convert.dart';
import 'package:circular_countdown_timer/circular_countdown_timer.dart';
import 'package:flutter/material.dart';
import 'dart:async';
import 'package:flutter_barcode_scanner/flutter_barcode_scanner.dart';
import 'crypto.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class MainScreen extends StatefulWidget {
  MainScreen({Key key}) : super(key: key);

  @override
  _MainScreenState createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  String code;
  String secretKey;
  Timer timer;
  int firstValueTime = timeToRegen();
  // 500ms of offset, to ensure that a new code is generated every time
  int offset = 500;
  CountDownController _controller = CountDownController();
  final _storage = FlutterSecureStorage();
  // Calling setState on an asynchronous event. But since it's asynchronous, the initState method has already finished
  @override
  void initState() {
    super.initState();

    readSecretKey().then((value) {
      setState(() {
        secretKey = value;
      });

      timer = Timer.periodic(Duration(seconds: 1), (_) {
        generateOTP();
      });
    });
  }

  Future<String> readSecretKey() async {
    String secretStorage = await _storage.read(key: 'secretKey');
    return secretStorage;
  }

  Future<void> storeSecret(String newSecretKey) async {
    await _storage.write(key: 'secretKey', value: newSecretKey);
  }

  void generateOTP() {
    if (secretKey != null) {
      // Create PBKDF2 instance using the SHA256 hash. The default is to use SHA1
      var gen = new PBKDF2(hash: sha256.newInstance());

      // Generate a 64 byte key using the given password and salt, with 1000 iterations
      var key = gen.generateKey(secretKey, "CTcPcC4x", 10000, 64);

      //List<int> to HexString
      var kdf = hex.encode(key);

      //Apply TOTP algorithm
      var totpCode = totp(kdf);
      setState(() {
        code = totpCode;
      });
    }
  }

  Future<void> readQRcode() async {
    String barcodeScanRes;
    // Platform messages may fail, so we use a try/catch PlatformException.
    try {
      barcodeScanRes = await FlutterBarcodeScanner.scanBarcode(
          "#ff6666", "Cancel", true, ScanMode.QR);
      print(barcodeScanRes);
    } on PlatformException {
      barcodeScanRes = 'Failed to get platform version.';
    }

    if (!mounted) return;

    if (barcodeScanRes == null) {
      setState(() {
        secretKey = null;
      });
    } else {
      var uri = Uri.parse(barcodeScanRes);
      var newSecretKey = uri.queryParameters['secret'];
      await storeSecret(newSecretKey);
      int newFirstValueTime = timeToRegen();
      setState(() {
        secretKey = newSecretKey;
        firstValueTime = newFirstValueTime;
      });
      timer.cancel();
      timer = Timer.periodic(Duration(seconds: 1), (_) {
        generateOTP();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color.fromRGBO(30, 30, 30, 1),
      appBar: AppBar(
        backgroundColor: Color.fromRGBO(36, 36, 36, 1),
        title: Text('SecureAuth'),
        elevation: 20.0,
        actions: [
          Padding(
              padding: EdgeInsets.only(right: 20),
              child: GestureDetector(
                  onTap: () => Navigator.pushNamed(context, '/settings'),
                  child: Icon(Icons.settings)))
        ],
      ),
      body: Center(
          child: Column(
        children: [
          SizedBox(height: 80),
          secretKey != null
              ? CircularCountDownTimer(
                  duration: firstValueTime,
                  // Controller to control (i.e Pause, Resume, Restart) the Countdown
                  controller: _controller,
                  width: 80,
                  height: 80,
                  color: Colors.white,
                  fillColor: Color.fromRGBO(154, 205, 50, 0.8),
                  backgroundColor: null,
                  strokeWidth: 4.0,
                  textStyle: TextStyle(
                      fontSize: 22.0,
                      color: Colors.white,
                      fontWeight: FontWeight.bold),
                  isReverse: true,
                  isReverseAnimation: true,
                  isTimerTextShown: true,
                  // Function which will execute when the Countdown Ends
                  onComplete: () {
                    // Here, do whatever you want
                    _controller.restart(duration: 30);
                  },
                )
              : SizedBox(height: 0),
          SizedBox(height: 80),
          Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: getCodeText()),
        ],
      )),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: readQRcode,
        label: Text('Scan new QR code'),
        tooltip: 'Scan new QR code',
        icon: Icon(Icons.qr_code),
        backgroundColor: Color.fromRGBO(154, 205, 50, 0.8),
      ),
    );
  }

  List<Widget> getCodeText() {
    List<Widget> widgetArray = List<Widget>();

    if (secretKey == null || code == null) {
      widgetArray.add(Text(
        'You don\'t have a code',
        style: TextStyle(color: Colors.white, fontSize: 25),
      ));
    } else {
      widgetArray.add(
        Text(
          'Your code is:',
          style: TextStyle(color: Colors.white, fontSize: 25),
        ),
      );
      widgetArray.add(SizedBox(height: 50));
      widgetArray.add(Text(
        '$code',
        // style: Theme.of(context).textTheme.headline4,
        style: TextStyle(color: Colors.white, fontSize: 60),
      ));
    }

    return widgetArray;
  }
}
