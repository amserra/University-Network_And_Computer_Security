import 'dart:convert';
import 'package:crypto/crypto.dart';

// Get Digit Power ex: getDigitPower(5) = 100_000 (1 and 5 zeros)
int getDigitPower(noDigits) {
  var result = 1;
  for (var i = 0; i < noDigits; i++) {
    result = result * 10;
  }
  return result;
}

// Generate TOTP code
String totp(kdf) {
  var noDigits = 6;

  var time = DateTime.now().millisecondsSinceEpoch ~/ 1000;

  String step = (time ~/ 30).toString();

  while (step.length < 16) {
    step = '0' + step;
  }

  var stepBytes = utf8.encode(step);
  var hmacSha256 = new Hmac(sha256, utf8.encode(kdf));
  var digest = hmacSha256.convert(stepBytes).bytes;

  var offset = digest[digest.length - 1] & 0xf;

  var binary = ((digest[offset] & 0x7f) << 24) |
      ((digest[offset + 1] & 0xff) << 16) |
      ((digest[offset + 2] & 0xff) << 8) |
      (digest[offset + 3] & 0xff);

  var otp = binary % getDigitPower(noDigits);

  String result = otp.toString();

  while (result.length < noDigits) {
    result = '0' + result;
  }
  return result;
}

int timeToRegen() {
  int time = DateTime.now().millisecondsSinceEpoch ~/ 1000; // to seconds
  int step = (time % 30); // time
  int timeToRegen = 30 - step; // to countdown
  return timeToRegen;
}
