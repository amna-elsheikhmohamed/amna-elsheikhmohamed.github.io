import requests
import tkinter as tk
from io import BytesIO

# Simulate RFID data for testing (skip hardware part)
def simulate_rfid_scan():
    # Simulating a scanned RFID ID
    id = 12345
    print(f"Simulated ID: {id}")
    title, description, image_url = get_exhibit_data(id)
    if title:
        display_text_and_image(title, description, image_url)

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

            # Use Tkinter PhotoImage to display the image
            image_photo = tk.PhotoImage(data=image_data.read())  # Load image data directly from response
            label_image.config(image=image_photo)
            label_image.image = image_photo  # Keep a reference to avoid garbage collection
        except Exception as e:
            print(f"Error displaying image: {e}")
            label_image.config(image=None)
    else:
        label_image.config(image=None)

# Setup tkinter window
window = tk.Tk()
window.title("Museum RFID Exhibit Viewer")
window.geometry("600x500")

label_title = tk.Label(window, text="Exhibit Title", font=("Arial", 20))
label_title.pack(pady=20)

label_description = tk.Label(window, text="Exhibit Description", font=("Arial", 12), wraplength=500)
label_description.pack(pady=10)

label_image = tk.Label(window)
label_image.pack(pady=10)

# Simulate RFID scanning by calling simulate_rfid_scan directly
simulate_rfid_scan()

window.mainloop()
