# JARVIS Android V1

A starter Android app for Android 11+ with a holographic-style animated Compose interface,
Android speech recognition, Android text-to-speech, basic offline time/date/greeting responses,
and an optional connection to your own JARVIS backend.

## Requirements
- Android Studio Ladybug (2024.2.1) or newer recommended
- JDK 17 (Android Studio bundled JBR 17 is suitable)
- Android SDK Platform 35
- Android phone running Android 11 or newer
- USB cable and USB debugging for direct install, or build APK and transfer it

## Open the project
1. Extract `JARVIS_Android_V1.zip`.
2. Open Android Studio.
3. Choose **Open** and select the extracted `JARVIS_Android_V1` folder.
4. Allow Gradle sync to complete.
5. If prompted, install Android SDK Platform 35 and Build Tools.
6. Connect your OPPO phone, enable Developer options and USB debugging, then press Run.

## Enable Developer options on OPPO
1. Settings > About device / About phone.
2. Tap Build number (or Version) seven times.
3. Enter your device PIN if requested.
4. Settings > Additional settings > Developer options.
5. Enable USB debugging.
6. Connect the phone and accept the RSA authorization prompt.

Menu labels may differ slightly by ColorOS version.

## Build a debug APK
In Android Studio: Build > Build Bundle(s) / APK(s) > Build APK(s).

Or from the project root in a terminal:
```bash
gradle assembleDebug
```
If you have generated the Gradle wrapper in Android Studio, use:
```bash
./gradlew assembleDebug
```
On Windows:
```powershell
.\gradlew.bat assembleDebug
```
APK output:
`app/build/outputs/apk/debug/app-debug.apk`

The debug APK is for testing. For sharing outside development, create a signed release APK using Build > Generate Signed Bundle / APK.

## First launch
- Tap MICROPHONE and grant microphone permission.
- Try: "Hello JARVIS", "What time is it?", "What is today's date?"
- Android SpeechRecognizer may use an online recognition service depending on the device's speech service and settings.
- Android TextToSpeech uses installed voice data and can often speak without internet once the voice is installed.

## Connect to the future JARVIS backend
Open the gear icon and enter your private HTTPS backend URL ending in `/chat`.
The backend should accept:
```json
{"message":"Hello JARVIS"}
```
and return:
```json
{"reply":"Hello. How may I help?"}
```
Do not put an OpenAI API key in the APK. Store it only on your private backend. Use HTTPS and add authentication before exposing the backend outside your local network.

## Current V1 limitations
- This is a phone-first UI and voice prototype, not a complete autonomous phone controller.
- Offline commands: greeting, time and date.
- The notes, direct app launching, battery telemetry, wake word, persistent Room memory, background listening, phone calling/SMS, notification reading and PC pairing are future milestones.
- Speech recognition availability and offline behavior depend on the installed Android speech service.
- No always-on microphone or wake-word service is included. This avoids battery drain and Android background microphone restrictions.

## Troubleshooting
- Gradle sync failure: verify JDK 17 and SDK Platform 35 are installed; use Android Studio's bundled JDK.
- Phone not detected: enable USB debugging, use a data-capable USB cable, and accept the RSA prompt.
- No speech recognition: install/update Google app or your device's speech recognition service and check network/microphone permissions.
- No voice output: install a Text-to-Speech voice under Android Settings > Language & input > Text-to-speech output.
