#!/bin/bash

# Check if the correct number of arguments are passed
if [ "$#" -ne 2 ]; then
    echo "Usage: ./speed_up.sh <times_faster> <input_filename>"
    exit 1
fi

# Extract arguments
TIMES_FASTER=$1
INPUT_FILE=$2
OUTPUT_FILE="${INPUT_FILE%.*}_${TIMES_FASTER}x.mp4"

# Calculate the speed factor
SPEED_FACTOR=$(echo "scale=5; 1/$TIMES_FASTER" | bc)

# Execute the ffmpeg command
ffmpeg -i "$INPUT_FILE" -vf "setpts=${SPEED_FACTOR}*PTS" -an "$OUTPUT_FILE"

echo "File has been saved to: $OUTPUT_FILE"
