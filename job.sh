#!/bin/bash

SCREENSHOT_DIR=~/smarn/smarn_screenshots

mkdir -p "$SCREENSHOT_DIR"

timestamp=$(date +"%Y%m%d_%H%M%S")

filename="screenshot_${timestamp}.png"

filepath="$SCREENSHOT_DIR/$filename"

scrot "$filepath"

echo "Screenshot saved: $filepath"