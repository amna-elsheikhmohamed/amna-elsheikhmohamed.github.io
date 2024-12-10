import requests
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

# Initialize RFID reader
reader = SimpleMFRC522()

# Mapping of RFID tags to specific Louvre exhibit API URLs (Example RFID mapping)
rfid_to_exhibit_mapping = {
    12345: "https://collections.louvre.fr/en/ark:/53355/cl010000029.json",  # Example Louvre exhibit URL
    67890: "https://collections.louvre.fr/en/ark:/53355/cl010000030.json",  # Another exhibit URL
}

# Function to fetch exhibit data from the Louvre API
def fetch_exhibit_data(exhibit_id):
    try:
        # Get the API URL for the exhibit based on the RFID ID
        api_url = rfid_to_exhibit_mapping.get(exhibit_id)
        if not api_url:
            print("No exhibit found for this RFID tag.")
            return None, None, None

        # Make the API request to the Louvre API
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP errors
        
        # Parse the JSON data from the response
        exhibit_data = response.json()

        # Extract the relevant data (title, description, and image)
        title = exhibit_data.get('label', 'No title')
        description = exhibit_data.get('description', 'No description')
        
        # Handle the case where images are in an array
        images = exhibit_data.get('image', [])
        image_url = images[0]['urlImage'] if images else ''  # Take the first image if available

        # Return the extracted data
        return title, description, image_url
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the Louvre API: {e}")
        return None, None, None

# Function to display an image in Tkinter
def display_image(image_url):
    try:
        response = requests.get(image_url)  # Get the image content
        image = Image.open(BytesIO(response.content))  # Open image from the response content
        
        # Resize the image for display (optional)
        image = image.resize((400, 300), Image.ANTIALIAS)
        
        # Convert to format that Tkinter can use (ImageTk required)
        img_tk = ImageTk.PhotoImage(image)
        
        # Update the label with the new image
        label_image.config(image=img_tk)
        label_image.image = img_tk  # Keep a reference to the image to prevent garbage collection
    except Exception as e:
        print(f"Error displaying image: {e}")

# Function to display title and description in Tkinter
def display_text(title, description):
    label_title.config(text=title)
    label_description.config(text=description)

# Function to handle RFID scan and fetch the exhibit data
def scan_rfid():
    try:
        print("Place your RFID tag near the reader...")
        id, text = reader.read()  # Read the RFID tag
        
        print(f"ID: {id}")
        title, description, image_url = fetch_exhibit_data(id)  # Fetch exhibit data based on RFID ID
        
        if title and description:
            print(f"Exhibit: {title}")
            print(f"Description: {description}")
            
            # Display the exhibit image and text
            display_image(image_url)
            display_text(title, description)
        else:
            label_title.config(text="No exhibit data found.")
            label_description.config(text="")
            label_image.config(image=None)  # Clear image if no data found
    finally:
        GPIO.cleanup()  # Ensure GPIO is cleaned up after use

# Set up the Tkinter window
window = tk.Tk()
window.title("Louvre Exhibit Viewer")
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

# Start the Tkinter window loop
window.mainloop()






# Hi 👋! My name is Amna, and I'm a New Intern from the Digital Experience Department

<h1 align="center">Internship Weekly Summary</h1>
<p align="center">
  <a href="#week1">Week 1 🌸</a> | 
  <a href="#week2">Week 2 🌺</a> | 
  <a href="#week3">Week 3 📝</a> | 
  <a href="#week4">Week 4 🌺</a> | 

</p>

---

<h1 id="week1" align="center">Week 1 🌸</h1>

### Sunday
-	The week began with an official introduction to the team and  the signing of the internship contract. 
-	Tour of the National Museum: I went on an immersive tour of the National Museum to familiarize myself with the exhibits, layout, and visitor engagement techniques currently in place.
-	Completing 12 Visitor Engagement Sheets: I observed visitor interactions and completed 12 engagement observation sheets. This activity provided insights into how visitors respond to various exhibits, particularly multimedia ones, helping us understand their engagement levels and areas for improvement.

### Monday
- Engaging with visitors and gathering feedback through surveys. This survey aimed to understand their opinions on the museum’s multimedia.

### Tuesday & Wednesday
- 	I dedicated time to studying Power BI, a powerful tool for analyzing data. My focus was on creating an analysis of the multimedia survey data, which I called the “Visitor Survey Analysis.” Through tutorials and practice, I learned how to use Power BI's basic functionalities to visualize feedback data.

### Thursday
- I created a GitHub account and made a simple vlog to recap my week’s activities.
-	I drafted a report using the results and insights from the Visitor Survey Analysis conducted in Power BI.

---

## Lessons Learned
- From Power BI:
  - I learn how to clean and sort the data.
  - I learn how to unpivot columns
  -  I learn about silence visualization it really cool and make the graphics more interactive


## Challenges
- 	Initially unsure if I cleaned the data correctly, but I checked with Tooba for confirmation.
- 	Some aspects of the data were challenging to visualize effectively.For example, complex visitor feedback, especially in textual responses, made it difficult to present insights clearly and concisely.

## Conclusion
I have always been eager to learn more about Power BI, so it was great to work with real data during my internship. I hope to take a course to further enhance my knowledge of it. I’ve visited the museum twice before, but this time feels different because I’m focused on learning about the technologies available at the museum, rather than just the historical aspects.

**All the tools I used**
<p align="left">
  <a href="https://github.com/your-username" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" height="60" alt="GitHub logo" />
  </a>
  <img src="https://img.icons8.com/color/48/000000/microsoft-excel-2019.png" height="60" alt="Excel logo" />
  <img src="https://img.icons8.com/color/48/000000/power-bi.png" height="60" alt="Power BI logo" />
</p>

---

<h1 id="week2" align="center">Week 2 🌺</h1>

This week,  My supervisor assigned me to fork the Australian Center for Moving Image’s source code using Ruby and Jekyll to create an audio guide for a fictional exhibition. My main tasks involved customizing the website's design, adding audio generated with a text-to-speech tool, and utilizing multimedia elements published on the Qatar Museum website.

### Sunday
- Explore material to understand the project.
- Downloaded Ruby and Jekyll, set them up, and ran the project code.
### Monday
- Studied the code and attempted to understand its structure and logic.
- Watched tutorials about YAML to learn how it works.
- Tried modifying the website’s design.
### Tuesday 
- Tried modifying the website’s design.
- Created some content and images to add to the site.
- Explored free tools for converting text to speech in different languages.
- Add audios in different languages
- create simple Excel to compare Language and Audio Duration which I created with tools for converting text to speech in different languages such as Eleven Labs.
  
    <img src="https://github.com/user-attachments/assets/166e1f31-1fc4-4309-8949-c431eaae8006" alt="Processed Image" height="200" width="auto">
## Challenges
- Learning Ruby, which is a new framework for me.
- Finding it challenging to stay motivated with Ruby, as it feels old and doesn't interest me.
  
## Overview

<a align="center" href="https://amna-am1803081.github.io/welcome/">Click here to vist the Audio Guide🎧</a>

<a target="_blank">
  <img src="https://github.com/user-attachments/assets/8848d810-156c-433d-9257-41d653b04195" alt="Processed Image" height="200" width="auto">
<a target="_blank">
  <img src="https://github.com/user-attachments/assets/b636cce9-245c-4216-85af-b3fd8c51a343" alt="Processed Image" height="200" width="auto">
</a>

## All the tools I used
<p align="left">
<!-- Eleven Labs logo -->
<a href="https://elevenlabs.io/" target="_blank">
  <img src="https://ubos.tech/wp-content/uploads/2024/01/ElevenLabs-Logo.png" height="60" alt="Eleven Labs logo" />
</a>
  
  <!-- Ruby logo -->
  <a href="https://www.ruby-lang.org/en/" target="_blank">
    <img src="https://upload.wikimedia.org/wikipedia/commons/7/73/Ruby_logo.svg" height="60" alt="Ruby logo" />
  </a>
</p>

<h1 id="week3" align="center">Week 3 📝</h1>

This week, I’m looking into a new platform, Getty’s Quire, to explore its capabilities in publishing an exhibition catalogue. My task involves forking existing code to create a custom publication, testing out its features, and experimenting with different formats: a downloadable PDF, an e-book, and an online version and check if it does support Arabic language.

## Challenges and Achievements
I tried to install Quire and Node on my laptop, but it didn’t work. I asked Tooba for help, but it didn’t work on her laptop either. I think there might be an issue with the platform, so I emailed their support team. They sent me some solutions, and I’ll try them later and update you.

  <img src="https://github.com/user-attachments/assets/dc40ab7a-9af7-4c92-b3f9-4df44eac4808" alt="Processed Image" height="200" width="auto">

### Thursday
Today, our team visited the Arab Museum of Modern Art to explore the exhibition *Seeing Is Believing: The Art and Influence of Gérôme*. We aimed to experience it from a guest’s perspective and to check the audio guide available there.

It was an amazing and entirely new experience for me—my first time learning about Orientalism in art. I was captivated by Gérôme’s realistic style; he portrayed Arab life with authenticity, capturing the essence of that time period without imposing European perspectives. His art is rich in detail and color, truly bringing history to life. I was also amazed at how well-preserved the paintings were. Despite being over 200 years old, they looked almost new, as if they had just been painted.

  <img src="https://github.com/user-attachments/assets/1be9e9ee-a138-4017-ba07-bb5355f1f3d4" alt="Processed Image" height="200" width="auto">

The first two sections of the exhibition were the most intriguing for me, especially the multimedia displays, which revealed details I hadn’t noticed before. For instance, in one of Gérôme's paintings depicting prayer, he showed people in different postures. This caught my attention because, in Islam, we pray in unison, moving through the same stages together. The multimedia explanation helped me realize that Gérôme likely intended to capture all the stages of prayer within a single scene.

  <img src="https://github.com/user-attachments/assets/45b25b98-5156-4ff5-9a36-14b76e0e9bd5" alt="Processed Image" height="200" width="auto">

The audio guide added an extra layer of enjoyment to the experience, offering a brief yet captivating story behind each painting. It wasn’t just informative it brought the artwork to life in a way that felt personal and engaging. With its distinctive and clear voice, the audio guide truly enhanced the exhibition, making the experience even more immersive.

  <img src="https://github.com/user-attachments/assets/16fc9889-ea43-4995-b139-5c03175c646e" alt="Processed Image" height="200" width="auto">
  <img src="https://github.com/user-attachments/assets/d59c9ca2-b235-4487-a437-1c1a486cb6fc" alt="Processed Image" height="200" width="auto">
---

<h1 id="week4" align="center">Week 4 💫 </h1>

- My task this week is to explore different museum online collections and choose collection to analyze using Power BI. 
- I chose The Museum of Modern Art (MoMA) Collection, which contains a dataset of artists and artworks. I've attempting to visualize it.
  
## Challenges
One challenge I faced was trying to use a line chart or Gantt to visualize the birth and death dates, as well as the age of the artist, but it didn’t work for me. So, I ended up using a table instead. I think it would be cooler if it were a chart.

## Overview
  
<a align="center" href="https://app.powerbi.com/groups/me/reports/85d90aa7-29fa-4188-9617-af6fa8f2fec8/f128069a26bd1f8567ff?experience=power-bi">Click here to vist my Dashboard📈</a>

<img src="https://github.com/user-attachments/assets/87e23e54-7fbc-4cb5-9a30-3da7e4c7d897" alt="Processed Image" height="200" width="auto">


----
<p align="center">
  &copy; 2024 Qatar Museum Internship
  <img src="https://www.qna.org.qa/en/News-Area/News/2024-08/07/qnacdn.azureedge.net/-/media/Project/QNA/QNAImages/2024-08/01/qna_mtahef_1_8_2024.jpg?h=630&la=en&w=840&modified=20240801180243" height="60" alt="Stats Graph" />
  <a href="https://github.com/your-username" target="_blank">
  </a>
</p>
