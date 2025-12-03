#!/bin/bash
# Create temporary certificate
openssl genrsa -out key.pem 2048
openssl req -new -key key.pem -out request.pem
openssl x509 -req -days 3650 -in request.pem -signkey key.pem -out certificate.pem

# Convert to PKCS12
openssl pkcs12 -export -in certificate.pem -inkey key.pem -out keystore.p12 -password pass:android

# Sign the APK
apksigner sign --ks keystore.p12 --ks-pass pass:android our_build/aligned.apk

echo "✅ APK signed with new certificate"
