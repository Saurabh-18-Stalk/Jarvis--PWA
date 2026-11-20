# JARVIS Native Companion (Android + Windows)

This is the first Flutter native companion foundation for the existing JARVIS project. It is a separate app from the GitHub Pages PWA.

## Current starter features
- One Flutter codebase targeting Android and Windows.
- English, Hindi and Marathi voice locale selection.
- Speech-to-text and text-to-speech using device/browser-independent native plugins (availability depends on installed language packs and OS speech services).
- Private FastAPI backend connection and health check.
- AI chat through the existing `POST /api/chat` endpoint.
- Native file picker: the user explicitly chooses files; the app does not silently scan the whole phone or PC.
- Save AI output to a user-selected location.
- YouTube content package and social media post drafting prompts. These are drafts only; publishing is not wired to accounts.
- Generated code is saved as text only. The app does not execute generated code.

## Android build
Install Flutter stable and Android Studio with Android SDK. From this folder:

```bash
flutter create --platforms=android,windows --project-name jarvis_companion .
flutter pub get
flutter run -d android
flutter build apk --release
```

Install the resulting APK from `build/app/outputs/flutter-apk/app-release.apk`. Android will ask the user to approve installing apps from the chosen source. Microphone permission is requested by the speech plugin when needed. File access uses Android's system picker and only selected files.

## Windows build
On Windows with Flutter and Visual Studio (Desktop development with C++) installed:

```powershell
flutter create --platforms=android,windows --project-name jarvis_companion .
flutter pub get
flutter run -d windows
flutter build windows --release
```

The Windows build output is under `build\windows\x64\runner\Release`. Package the whole Release directory, not only the EXE.

## Backend setup
Enter the deployed HTTPS backend URL and JARVIS bearer token in Settings. Keep provider keys in the backend host's private environment variables only. The backend should allow the app origin if it is used from a browser; native Flutter requests are not subject to browser CORS, but still require HTTPS and proper authentication.

## Important limitations
- Android does not permit unrestricted access to every file by default. JARVIS uses the system document picker so the user grants access to selected files/folders.
- Windows file selection is user-driven. Broad disk access should require explicit Windows permissions and confirmation.
- Background wake-word listening, always-on microphone, full offline speech recognition, system-wide Windows automation, and remote social account posting are not implemented in this starter.
- YouTube uploads and social publishing require official platform APIs, OAuth consent, scopes, quota management and explicit confirmation. Never share passwords or session cookies with JARVIS.
- AI chat and code generation require the private backend and internet.
- Review generated code before running it. No code is automatically executed.
