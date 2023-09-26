#!/bin/bash

# The directory containing images
IMAGE_DIR="$1"

# Thumbnail size
THUMBNAIL_WIDTH=128
THUMBNAIL_HEIGHT=128

# Check if convert (from ImageMagick) is installed
if ! command -v convert &> /dev/null
then
    echo "convert (from ImageMagick) could not be found. Please install it."
    exit
fi

# Convert string to lower case function
to_lower() {
    echo "$1" | tr '[:upper:]' '[:lower:]'
}

# Process each image in the directory
for img in "$IMAGE_DIR"/*; do
    # Ensure the file exists (in case no matches are found for the pattern)
    [ -e "$img" ] || continue

    # Extract the extension and convert to lowercase
    ext=$(to_lower "${img##*.}")

    # Check if the file is an image (by extension)
    if [[ "$ext" =~ ^(jpg|jpeg|png|webp|bmp|gif)$ ]]; then

        # Construct the thumbnail filename
        base="${img%.*}"
        thumbnail="${base}_th.${ext}"

        # Only generate a thumbnail if it doesn't exist
        if [[ ! -f "$thumbnail" ]]; then
            convert "$img" -resize ${THUMBNAIL_WIDTH}x${THUMBNAIL_HEIGHT} "$thumbnail"
        fi
    fi
done

