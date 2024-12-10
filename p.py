import requests
import cv2
import tkinter as tk
import numpy as np
from io import BytesIO
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

# Initialize RFID reader
reader = SimpleMFRC522()

# Mapping of RFID tags to specific Louvre exhibit API URLs
rfid_to_exhibit_mapping = {
    12345: "https://collections.louvre.fr/en/ark:/53355/cl010000029.json",  # Example Louvre exhibit URL
    67890: "https://collections.louvre.fr/en/ark:/53355/cl010000030.json",  # Another exhibit URL
}

# Function to get exhibit data from the Louvre API
def get_exhibit_data(exhibit_id):
    try:
        api_url = rfid_to_exhibit_mapping.get(exhibit_id)
        if not api_url:
            print("No exhibit found for this RFID tag.")
            return None, None, None

        response = requests.get(api_url)
        response.raise_for_status()  # Check if the request was successful
        exhibit_data = response.json()

        title = exhibit_data.get('label', 'No title')
        description = exhibit_data.get('description', 'No description')

        image_url = ""
        if "image" in exhibit_data and len(exhibit_data["image"]) > 0:
            image_url = exhibit_data["image"][0].get("urlImage", "")

        return title, description, image_url
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exhibit data: {e}")
        return None, None, None

# Function to display text and image in tkinter window
def display_text_and_image(title, description, image_url):
    label_title.config(text=title)
    label_description.config(text=description)

    if image_url:
        try:
            # Fetch image using requests
            response = requests.get(image_url)
            image_data = BytesIO(response.content)

            # Convert the byte data to a numpy array for OpenCV
            img_array = np.asarray(bytearray(image_data.read()), dtype=np.uint8)

            # Decode the image into an OpenCV format
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            # Convert image from BGR (OpenCV format) to RGB (Tkinter format)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Convert the OpenCV image into a format that Tkinter can use
            img_tk = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)  # Ensure color format is correct
            img_tk = cv2.imencode('.png', img_tk)[1].tobytes()  # Convert to bytes

            # Create a Tkinter-compatible image and update the label
            photo = tk.PhotoImage(data=img_tk)
            label_image.config(image=photo)
            label_image.image = photo  # Keep a reference to avoid garbage collection
        except Exception as e:
            print(f"Error displaying image: {e}")
            label_image.config(image=None)
    else:
        label_image.config(image=None)

# Function to scan RFID and display corresponding exhibit
def scan_rfid():
    try:
        print("Place your RFID tag near the reader...")
        id, text = reader.read()  # Read the RFID tag
        
        print(f"Scanned ID: {id}")
        title, description, image_url = get_exhibit_data(id)  # Fetch exhibit data based on RFID ID
        
        if title:
            print(f"Exhibit: {title}")
            print(f"Description: {description}")
            # Display the exhibit image and text
            display_text_and_image(title, description, image_url)
        else:
            label_title.config(text="No exhibit data found.")
            label_description.config(text="")
            label_image.config(image=None)  # Clear image if no data found
    finally:
        GPIO.cleanup()  # Ensure GPIO is cleaned up after scanning

# Setup tkinter window
window = tk.Tk()
window.title("Museum RFID Exhibit Viewer")
window.geometry("600x500")

# Create labels for displaying title, description, and image
label_title = tk.Label(window, text="Exhibit Title", font=("Arial", 20))
label_title.pack(pady=20)

label_description = tk.Label(window, text="Exhibit Description", font=("Arial", 12), wraplength=500)
label_description.pack(pady=10)

label_image = tk.Label(window)
label_image.pack(pady=10)

# Create a button to trigger RFID scanning
scan_button = tk.Button(window, text="Scan RFID", font=("Arial", 14), command=scan_rfid)
scan_button.pack(pady=20)

# Start the tkinter window loop
window.mainloop()
pip install opencv-python requests numpy
