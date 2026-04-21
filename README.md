Really simple KernelSU module to serve the missing TelephonyBaseUtilsStub class systemlessly, so that phone calls can be received and not dropped by the modem from 4G&5G connections. Generated with assistance from Gemini by iterating over the diagonistic files & system logs. I'm not an android developer so this is a very janky AI generated fix that hopefully works. The generator script asks for the ims.apk from the (hardcoded) location, you can extract it from your ROM payload and change the corresponding location. Other dependencies are installed by the script. The diagonistic script is meant to run in a root shell from the phone. Let me know if it doesn't work for you.

AI generated explanation below:

# Xiaomi IMS Native Injection Fix (QPR2/3)

A surgical KernelSU module to restore VoLTE/VoWiFi on Xiaomi devices running custom Android 16 ROMs where the `TelephonyBaseUtilsStub` framework is missing.

## The Problem
Many custom ROMs include the Qualcomm IMS app but omit the proprietary Xiaomi framework JARs. This causes a fatal `ClassNotFoundException` or `NoClassDefFoundError` for `android.telephony.TelephonyBaseUtilsStub`, crashing the IMS service.

## Why Other Fixes Fail
* **EROFS:** Modern partitions are read-only; you cannot simply add the missing `.jar`.
* **Monolithic ART Cache:** Framework overlays are ignored because the system uses a pre-compiled boot image.
* **Signature Enforcement:** Modifying the APK usually breaks the UID 1001 (Radio) status.

## The "V9" Solution
This module uses a multi-stage bypass strategy:
1. **Native Injection:** The missing classes and `isMiuiRom()` methods are forged in Smali and injected directly into the `ims.apk` bytecode.
2. **Cryptographic Forgery:** The APK is re-signed with AOSP Test Keys.
3. **SELinux Surgical Patching:** Since the signature change demotes the app to `priv_app`, this module injects custom `sepolicy.rule` patches to allow the demoted app to communicate with `vendor_hal_telephony_service2`.
4. **Bind Mounting:** The patched APK is forcefully mapped over the system original during the `post-fs-data` boot stage.

## License
Licensed under the **GNU General Public License v3.0**. See the `LICENSE` file for details.
