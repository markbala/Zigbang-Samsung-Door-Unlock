import requests

# Set up SmartThings API:
#     You will need to create a SmartThings developer account at https://account.smartthings.com.
#     Register a new SmartApp or use an existing device, and generate an OAuth token that can be used in API requests.

# Find the Door Lock device ID:
#     You need to know the device ID of the ZigBang door lock in your SmartThings setup. This can be found via the SmartThings API or the SmartThings IDE.

# Constants
BASE_URL = "https://api.smartthings.com/v1"
OAUTH_TOKEN = "your_oauth_token"  # Replace with your OAuth token
DEVICE_ID = "your_device_id"      # Replace with your ZigBang door lock's device ID

# Headers for SmartThings API requests
headers = {
    "Authorization": f"Bearer {OAUTH_TOKEN}",
    "Content-Type": "application/json"
}

# Check the lock status and unlock if locked
def unlock_if_locked():
    url = f"{BASE_URL}/devices/{DEVICE_ID}/status"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        lock_status = response.json().get("components", {}).get("main", {}).get("absoluteweather46907.lockstaterelease", {}).get("lock", {}).get("value")
        print(f"Lock Status: {'Locked' if lock_status == 'locked.en' else 'Unlocked'}")
        if lock_status == "locked.en":
            unlock_url = f"{BASE_URL}/devices/{DEVICE_ID}/commands"
            data = {"commands": [{"component": "main", "capability": "absoluteweather46907.lock", "command": "unlock"}]}
            unlock_response = requests.post(unlock_url, headers=headers, json=data)
            if unlock_response.status_code == 200:
                print("Door successfully unlocked.")
            else:
                print(f"Failed to unlock: {unlock_response.status_code}")
    else:
        print(f"Failed to get lock status: {response.status_code}")

# Run the function
if __name__ == "__main__":
    unlock_if_locked()
