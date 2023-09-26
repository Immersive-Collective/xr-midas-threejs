#!/bin/bash

# Default to the current directory if no argument is given
DIR="${1:-.}"

# Check if the provided path is a directory
if [ ! -d "$DIR" ]; then
    echo "Error: $DIR is not a directory."
    exit 1
fi

# Function to convert file paths to JSON format
generate_json() {
    echo "["
    while IFS= read -r path; do
        # Exclude index.json from the output
        if [[ "$path" != "$DIR/index.json" ]]; then
            printf '    "%s",\n' "$path"
        fi
    done | sed '$s/,$//'
    echo "]"
}

# Use find to get all files and send to the generate_json function
find "$DIR" -type f | generate_json > "$DIR/index.json"

echo "index.json has been created in $DIR"
