#!/bin/bash

save_dir=~/smarn/smarn_screenshots

if [ ! -d "$save_dir" ]; then
    mkdir -p "$save_dir"
fi

get_display_server() {
    if [ ! -z "$WAYLAND_DISPLAY" ]; then
        echo "w"
    elif [ ! -z "$DISPLAY" ]; then
        echo "x"
    else
        echo "unknown"
    fi
}

take_screenshot() {
    display_server=$(get_display_server)
    current_time=$(date +"%Y-%m-%d_%H-%M-%S")
    screenshot_file="${save_dir}/smarn_${current_time}.png"

    if [ "$display_server" = "w" ]; then
        if command -v grim &> /dev/null; then
            grim "$screenshot_file"
            if [ $? -eq 0 ]; then
                echo "Screenshot saved to $screenshot_file"
            else
                echo "Grim failed, trying gnome-screenshot"
                if command -v gnome-screenshot &> /dev/null; then
                    gnome-screenshot -f "$screenshot_file" && echo "Screenshot saved to $screenshot_file"
                else
                    echo "gnome-screenshot is not installed"
                fi
            fi
        else
            echo "Grim is not installed"
        fi
    elif [ "$display_server" = "x" ]; then
        if command -v scrot &> /dev/null; then
            scrot "$screenshot_file" && echo "Screenshot saved to $screenshot_file"
        else
            echo "scrot is not installed"
        fi
    else
        echo "Could not detect display server"
    fi
}

take_screenshot
