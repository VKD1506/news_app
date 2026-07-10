# Android Wrapper

This folder contains a simple Android app that opens your News App URL in a WebView.

Before building

1. Start the Flask app on your computer.
2. Make sure your phone and computer are on the same Wi-Fi network.
3. Open the `android` folder in Android Studio.
4. Let Android Studio download the Gradle wrapper and Android SDK components.
5. Build `app` or generate a signed APK.

Recommended URL format

- `http://192.168.1.20:5000/` for local Wi-Fi testing
- `https://your-site.example.com` for hosted deployment

Why this approach

- Your current project is a Flask web app, not a native Android app.
- The Android wrapper can point to either a local Wi-Fi URL or a hosted URL.

APK steps in Android Studio

1. Open the `android` folder as a project.
2. Wait for the Gradle sync to finish.
3. Use `Build` -> `Build Bundle(s) / APK(s)` -> `Build APK(s)`.
4. For a shareable install file, use `Build` -> `Generate Signed Bundle / APK`.
