#!/bin/bash

# Configuration
CURRENT_DIR="$PWD"
UPLOAD_FOLDER="$CURRENT_DIR/uploads"
SHARE_FOLDER="$CURRENT_DIR/share"
IMAGE_EXTENSIONS="jpg,jpeg,png,gif,bmp,webp"

# Verify folders
if [ ! -d "$UPLOAD_FOLDER" ] || [ ! -d "$SHARE_FOLDER" ]; then
    echo "Error: Either 'uploads' or 'share' directory doesn't exist in $CURRENT_DIR."
    exit 1
fi

# Convert comma-separated IMAGE_EXTENSIONS to pipe-separated for regex matching
IMAGE_EXT_REGEX=$(echo $IMAGE_EXTENSIONS | sed 's/,/|/g')

# Iterate over all images in the UPLOAD_FOLDER
for image in $UPLOAD_FOLDER/*; do
    # Check if the file matches the allowed extensions and is not a thumbnail
    if [[ ! "$image" =~ _th\.($IMAGE_EXT_REGEX)$ ]]; then
        
        # Extract the full filename (including extension)
        FULL_NAME=$(basename "$image")
        BASE_NAME="${FULL_NAME%.*}" # name without extension

        # Check if the JSON file for this image exists in the SHARE_FOLDER
        JSON_EXISTS=false
        for json_file in $SHARE_FOLDER/*.json; do
            if grep -q "\"original_filename\": \"$FULL_NAME\"" "$json_file"; then
                JSON_EXISTS=true
                break
            fi
        done

        # Create a JSON if it doesn't exist for this image
        if ! $JSON_EXISTS; then
            IMAGE_UUID=$(uuidgen)
            echo "{\"original_filename\": \"$FULL_NAME\"}" > "$SHARE_FOLDER/$IMAGE_UUID.json"
            echo "Created JSON for $FULL_NAME with UUID $IMAGE_UUID."
        fi
    fi
done

echo "Script execution completed."
