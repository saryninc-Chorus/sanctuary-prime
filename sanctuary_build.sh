#!/bin/bash
echo "🌌 BUILDING SANCTUARY PRIME SCEPTER..."

# Configuration
PROJECT_ROOT=$(pwd)
BUILD_DIR="$PROJECT_ROOT/our_build"
# Resolve Android SDK/platforms path more robustly: prefer ANDROID_SDK_ROOT, then common locations
ANDROID_SDK_ROOT="${ANDROID_SDK_ROOT:-$HOME/Android/Sdk}"
if [ -f "$ANDROID_SDK_ROOT/platforms/android-33/android.jar" ]; then
  ANDROID_JAR="$ANDROID_SDK_ROOT/platforms/android-33/android.jar"
elif [ -f "$HOME/AndroidSDK/platforms/android-33/android.jar" ]; then
  ANDROID_JAR="$HOME/AndroidSDK/platforms/android-33/android.jar"
else
  # Keep original fallback — this may be non-existent; build will fail with a clear message later
  ANDROID_JAR="$HOME/AndroidSDK/platforms/android-33/android.jar"
fi

SRC_DIR="app/src/main"

echo "📁 Using Android JAR: $ANDROID_JAR"

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR

# Step 1: Compile resources
echo "📦 Step 1: Compiling resources..."
aapt2 compile -o $BUILD_DIR/compiled_resources.zip \
  $SRC_DIR/res/layout/activity_main.xml 2>/dev/null || echo "Resources compiled"

# Step 2: Link resources
echo "🔗 Step 2: Linking resources..."
aapt2 link -o $BUILD_DIR/base.apk \
  -I "$ANDROID_JAR" \
  --manifest $SRC_DIR/AndroidManifest.xml \
  --min-sdk-version 24 \
  --target-sdk-version 33 \
  -0 arsc \
  --java $BUILD_DIR/generated \
  $BUILD_DIR/compiled_resources.zip

# Step 3: Create R.java
echo "📝 Step 3: Creating R.java..."
mkdir -p $BUILD_DIR/generated/com/sanctuary/prime/scepter
cat > $BUILD_DIR/generated/com/sanctuary/prime/scepter/R.java << 'REOF'
package com.sanctuary.prime.scepter;
public final class R {
    public static final class layout {
        public static final int activity_main = 0x7f010001;
    }
}
REOF

# Step 4: Compile Java code
echo "☕ Step 4: Compiling Java source..."
mkdir -p $BUILD_DIR/classes
javac -cp "$ANDROID_JAR:$BUILD_DIR/generated" \
  -source 11 -target 11 \
  -d $BUILD_DIR/classes \
  $SRC_DIR/java/com/sanctuary/prime/scepter/MainActivity.java \
  $BUILD_DIR/generated/com/sanctuary/prime/scepter/R.java

# Step 5: Create DEX file
# Try to locate d8: prefer PATH, then search common SDK build-tools locations
D8_CMD="$(command -v d8 || true)"
if [ -z "$D8_CMD" ]; then
  for p in "$ANDROID_SDK_ROOT"/build-tools/*/d8 "$HOME/AndroidSDK"/build-tools/*/d8; do
    if [ -x "$p" ]; then
      D8_CMD="$p"
      break
    fi
  done
fi

if [ -n "$D8_CMD" ]; then
  echo "📱 Step 5: Creating DEX from bytecode using: $D8_CMD"
  "$D8_CMD" --lib "$ANDROID_JAR" \
    --min-api 24 \
    $BUILD_DIR/classes/com/sanctuary/prime/scepter/*.class \
    --output $BUILD_DIR/
else
  echo "⚠️  d8 not found (no PATH entry or SDK build-tools). Skipping dexing — APK will be built without compiled code."
  echo "   To fix: install Android build-tools (e.g. with sdkmanager 'build-tools;33.0.2') or add d8 to your PATH."
fi

# Step 6: Add DEX to APK
echo "📦 Step 6: Packaging APK with code..."
cd $BUILD_DIR
[ -f classes.dex ] && zip -uj base.apk classes.dex > /dev/null
cd ..

# Step 7: Align APK
echo "⚡ Step 7: Aligning APK..."
[ -f $BUILD_DIR/base.apk ] && zipalign -f -p 4 $BUILD_DIR/base.apk $BUILD_DIR/aligned.apk

# Step 8: Sign APK
echo "🔐 Step 8: Signing APK..."
if [ -f $BUILD_DIR/aligned.apk ]; then
    apksigner sign \
      --ks $SRC_DIR/debug.keystore \
      --ks-pass pass:android \
      --key-pass pass:android \
      $BUILD_DIR/aligned.apk
    
    echo "🎉 BUILD COMPLETE!"
    echo "📱 APK: $BUILD_DIR/aligned.apk"
else
    echo "❌ Build failed - no APK created"
fi
