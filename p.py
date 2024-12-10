import requests
from PIL import Image, ImageOps
import tkinter as tk
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
        # Get the API URL for the exhibit based on the RFID ID
        api_url = rfid_to_exhibit_mapping.get(exhibit_id)
        if not api_url:
            print("No exhibit found for this RFID tag.")
            return None, None, None

        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        exhibit_data = response.json()
        
        # Extract data from the response
        title = exhibit_data.get('label', 'No title')
        description = exhibit_data.get('description', 'No description')
        
        # Extract image URL from the image array (if available)
        image_url = ""
        if "image" in exhibit_data and len(exhibit_data["image"]) > 0:
            image_url = exhibit_data["image"][0].get("urlImage", "")
        
        # Return the relevant information
        return title, description, image_url
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exhibit data: {e}")
        return None, None, None

# Function to display text and image in tkinter window
def display_text_and_image(title, description, image_url):
    label_title.config(text=title)
    label_description.config(text=description)
    
    # If image_url is available, display the image
    if image_url:
        try:
            # Fetch the image from the URL
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))  # Open image from URL
            image = ImageOps.fit(image, (300, 200), method=0)  # Resize and crop the image
            img_tk = ImageTk.PhotoImage(image)  # Convert image to Tkinter format
            
            # Display the image
            label_image.config(image=img_tk)
            label_image.image = img_tk  # Keep a reference to the image
        except Exception as e:
            print(f"Error displaying image: {e}")
            label_image.config(image=None)  # Clear image if there's an error
    else:
        label_image.config(image=None)  # If no image URL, clear the image

# Function to handle RFID scan and display results
def scan_rfid():
    try:
        print("Place your RFID tag near the reader...")
        id, text = reader.read()  # Read the RFID tag
        
        print(f"ID: {id}")
        title, description, image_url = get_exhibit_data(id)  # Fetch exhibit data based on RFID ID
        
        if title:
            print(f"Exhibit: {title}")
            print(f"Description: {description}")
            
            # Display the exhibit text and image
            display_text_and_image(title, description, image_url)
        else:
            label_title.config(text="No exhibit data found.")
            label_description.config(text="")
            label_image.config(image=None)  # Clear image if no data found
    finally:
        GPIO.cleanup()

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
