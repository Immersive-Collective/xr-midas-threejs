#!/bin/bash

# Extract the IP address of Oculus Quest using adb and grep/awk
IP=$(adb shell ip route | grep -o 'src [0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+' | awk '{print $2}')

# Check if IP was found
if [ -z "$IP" ]; then
    echo "Failed to get IP address of Oculus Quest."
    exit 1
fi

# Connect to Oculus Quest over Wi-Fi
adb tcpip 5555 && adb connect $IP:5555
