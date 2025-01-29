#!/bin/bash


# shell command version of script

# Constants
BASE_URL="https://api.smartthings.com/v1"
OAUTH_TOKEN="your_oauth_token"  # Replace with your OAuth token
DEVICE_ID="your_device_id"      # Replace with your ZigBang door lock's device ID

# Headers for SmartThings API requests
AUTH_HEADER="Authorization: Bearer $OAUTH_TOKEN"
CONTENT_HEADER="Content-Type: application/json"

# Function to get the lock status
get_lock_status() {
    response=$(curl -s -H "$AUTH_HEADER" -H "$CONTENT_HEADER" "$BASE_URL/devices/$DEVICE_ID/status")
    
    # Extract lock status using grep, sed, and awk
    lock_status=$(echo "$response" | grep -o '"lock": *"[^"]*' | awk -F '":' '{print $2}' | tr -d '"')
    
    echo "$lock_status"
}

# Function to unlock the door
unlock_door() {
    unlock_command='{"commands":[{"component":"main","capability":"absoluteweather46907.lock","command":"unlock"}]}'
    
    # Send the unlock request
    unlock_response=$(curl -s -X POST -H "$AUTH_HEADER" -H "$CONTENT_HEADER" -d "$unlock_command" "$BASE_URL/devices/$DEVICE_ID/commands")
    
    # Check if the response indicates success
    if echo "$unlock_response" | grep -q '"status":"success"'; then
        echo "Door successfully unlocked."
    else
        echo "Failed to unlock the door."
    fi
}

# Main logic
lock_status=$(get_lock_status)

if [ "$lock_status" == "locked.en" ]; then
    echo "Lock Status: Locked"
    unlock_door
else
    echo "Lock Status: Unlocked"
fi
