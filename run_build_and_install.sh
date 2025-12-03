#!/usr/bin/env bash
set -euo pipefail

# Helper script to build the project and install the resulting APK to a connected device.
# Usage: ./run_build_and_install.sh
# If your Android SDK is in a nonstandard location, set ANDROID_SDK_ROOT before running:
#   export ANDROID_SDK_ROOT="$HOME/Android/Sdk"

echo "--- ENV ---"
echo "PWD=$(pwd)"
echo "ANDROID_SDK_ROOT=${ANDROID_SDK_ROOT:-<not set>}"

printf "\n--- TOOLS ---\n"
for t in aapt2 d8 zipalign apksigner adb javac openssl; do
  which "$t" >/dev/null 2>&1 && echo "$t: $(which $t)" || echo "$t: NOT FOUND"
done

# If d8 isn't in PATH, try to locate it under the Android SDK and add it to PATH for this run
if ! command -v d8 >/dev/null 2>&1; then
  SDK_ROOT="${ANDROID_SDK_ROOT:-$HOME/Android/Sdk}"
  D8_PATH=""
  for p in "$SDK_ROOT"/build-tools/*/d8 "$HOME/AndroidSDK"/build-tools/*/d8; do
    if [ -x "$p" ]; then
      D8_PATH="$p"
      break
    fi
  done
  if [ -n "$D8_PATH" ]; then
    D8_DIR=$(dirname "$D8_PATH")
    echo "Found d8 at: $D8_PATH — adding $D8_DIR to PATH for this run"
    export PATH="$D8_DIR:$PATH"
  else
    echo "d8 not found in PATH or SDK build-tools. The build may produce an APK without classes.dex."
    echo "Install Android build-tools (sdkmanager 'build-tools;33.0.2') or add d8 to PATH to include compiled code in the APK."
  fi
fi

# Make sure the main build script exists
if [ ! -f ./sanctuary_build.sh ]; then
  echo "ERROR: sanctuary_build.sh not found in project root"
  exit 2
fi

chmod +x ./sanctuary_build.sh || true

echo "\n--- RUNNING: ./sanctuary_build.sh ---"
./sanctuary_build.sh || true

APK_PATH=our_build/aligned.apk

if [ -f "$APK_PATH" ]; then
  echo "\nAPK produced:"
  ls -l "$APK_PATH"
else
  echo "\nNo APK produced at $APK_PATH"
  exit 3
fi

# List devices
echo "\n--- ADB DEVICES ---"
adb devices -l || true

device_count=$(adb devices -l 2>/dev/null | sed 1d | awk 'NF' | wc -l || echo 0)
echo "Device count: $device_count"

if [ "$device_count" -gt 0 ]; then
  echo "\nInstalling APK to first connected device..."
  adb install -r "$APK_PATH" || (
    echo "Install failed, attempting uninstall+reinstall"
    adb uninstall com.sanctuary.prime.scepter || true
    adb install -r "$APK_PATH"
  )
  echo "\nDone. If install succeeded, open the app on the device."
else
  echo "\nNo devices connected; connect a device or start an emulator and re-run this script."
fi
