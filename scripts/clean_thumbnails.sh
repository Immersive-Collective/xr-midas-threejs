#!/bin/bash

# The directory containing images
IMAGE_DIR="$1"

# Convert string to lower case function
to_lower() {
    echo "$1" | tr '[:upper:]' '[:lower:]'
}

# Delete thumbnails in the directory
for img in "$IMAGE_DIR"/*_th.*; do
    # Ensure the file exists (in case no matches are found for the pattern)
    [ -e "$img" ] || continue

    # Extract the extension and convert to lowercase
    ext=$(to_lower "${img##*.}")

    # Check if the file is an image thumbnail (by extension)
    if [[ "$ext" =~ ^(jpg|jpeg|png|webp|bmp)$ ]]; then
        rm "$img"
        echo "Deleted thumbnail: $img"
    fi
done
