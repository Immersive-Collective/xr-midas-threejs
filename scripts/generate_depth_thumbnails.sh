#!/bin/bash

# Get the absolute path of the provided directory
IMAGE_DIR=$(realpath "$1")

# Check if directory is provided
if [[ -z "$IMAGE_DIR" ]]; then
    echo "Please provide the path to the directory with images as an argument."
    exit 1
fi

# Directory with output images
OUTPUT_DIR="${IMAGE_DIR%/uploads}/outputs"

# Allowed file extensions
ALLOWED_EXTENSIONS="jpg jpeg png webp heic bmp JPG JPEG PNG WEBP HEIC BMP"

# Function to check if a file has an allowed extension
has_allowed_extension() {
    local filename="$1"
    local extension="${filename##*.}"
    for ext in $ALLOWED_EXTENSIONS; do
        if [[ "$ext" == "$extension" ]]; then
            return 0
        fi
    done
    return 1
}

# Function to create a thumbnail for an image

create_thumbnail() {
    local depth_image_path="$1"

    # Determine the original image path from the depth image path
    local original_image_path="${depth_image_path%_depth.*}.${depth_image_path##*.}"
    local thumbnail_path="${original_image_path%.*}_th.${original_image_path##*.}"

    if [[ -f "$depth_image_path" ]]; then
        if [[ ! -f "$thumbnail_path" ]]; then
            echo "Creating thumbnail for $original_image_path..."
            convert "$original_image_path" -resize '400x400>' "$thumbnail_path"
        else
            echo "Thumbnail for $original_image_path already exists."
        fi
    else
        echo "No depth image for $original_image_path. Skipping thumbnail creation."
    fi
}



# Loop through each file in the image directory
for filepath in "$IMAGE_DIR"/*; do
    if [[ -f "$filepath" ]] && has_allowed_extension "$filepath"; then
        create_thumbnail "$filepath"
    fi
done
