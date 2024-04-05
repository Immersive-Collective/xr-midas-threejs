#!/bin/bash

# Name of the temporary folder where the certificates will be saved
TMP_CERT_DIR="/tmp/browser-sync-certs"

# Ensure mkcert is installed
if ! command -v mkcert &> /dev/null; then
    echo "mkcert is not installed. Please install it and then run this script."
    exit 1
fi

# Ensure browser-sync is installed
if ! command -v browser-sync &> /dev/null; then
    echo "browser-sync is not installed. Please install it and then run this script."
    exit 1
fi

# Get external IP address
EXTERNAL_IP=$(curl -s ifconfig.me)

# Create a temporary directory to store the certs
mkdir -p "$TMP_CERT_DIR"

# Generate certificates
mkcert -key-file="$TMP_CERT_DIR/$EXTERNAL_IP-key.pem" -cert-file="$TMP_CERT_DIR/$EXTERNAL_IP.pem" $EXTERNAL_IP

# Start browser-sync with the generated certificates
browser-sync start --https --key "$TMP_CERT_DIR/$EXTERNAL_IP-key.pem" --cert "$TMP_CERT_DIR/$EXTERNAL_IP.pem" --proxy "127.0.0.1:5050" --files "templates/**/*.*"

# Clean up (optional: remove the temporary directory after browser-sync terminates)
# rm -r "$TMP_CERT_DIR"
