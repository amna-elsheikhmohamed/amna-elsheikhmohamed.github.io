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
            print_colored("No exhibit found for this RFID tag.", "red")
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
        print_colored(f"Error fetching exhibit data: {e}", "red")
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

            # Resize the image to fit within the tkinter window
            img_height, img_width = img.shape[:2]
            max_width, max_height = 500, 300  # Desired max dimensions for the image
            scale = min(max_width / img_width, max_height / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            img_resized = cv2.resize(img, (new_width, new_height))

            # Convert image from BGR (OpenCV format) to RGB (Tkinter format)
            img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

            # Convert the OpenCV image into a format that Tkinter can use
            img_tk = cv2.imencode('.png', img_rgb)[1].tobytes()
            photo = tk.PhotoImage(data=img_tk)

            # Update the label with the image
            label_image.config(image=photo)
            label_image.image = photo  # Keep a reference to avoid garbage collection
        except Exception as e:
            print_colored(f"Error displaying image: {e}", "red")
            label_image.config(image=None)
    else:
        label_image.config(image=None)

# Function to print messages in colored text
def print_colored(message, color):
    if color == "red":
        print(f"\033[91m{message}\033[0m")  # Red text
    elif color == "blue":
        print(f"\033[94m{message}\033[0m")  # Blue text
    else:
        print(message)

# Function to scan RFID and display corresponding exhibit
def scan_rfid():
    try:
        print_colored("Place your RFID tag near the reader...", "blue")
        id, text = reader.read()  # Read the RFID tag

        print_colored(f"Scanned ID: {id}", "blue")
        title, description, image_url = get_exhibit_data(id)  # Fetch exhibit data based on RFID ID

        if title:
            print_colored(f"Exhibit: {title}", "blue")
            print_colored(f"Description: {description}", "blue")
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
