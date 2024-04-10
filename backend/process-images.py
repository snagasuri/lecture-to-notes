from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()  





































from openai import OpenAI
import base64
from PIL import Image
import io
import os

# Assuming your OpenAI API Key is set in an environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Function to resize and encode the image
def resize_and_encode_image(image_path, resize_width):
    # Open and resize the image
    with Image.open(image_path) as img:
        # Calculate the new height maintaining the aspect ratio
        aspect_ratio = img.height / img.width
        new_height = int(resize_width * aspect_ratio)
        
        # Resize the image
        resized_img = img.resize((resize_width, new_height))
        
        print(f"Original dimensions: {img.size}")
        print(f"Resized dimensions: {resized_img.size}")

        resized_img.save("temp_resized_image.jpg")

        # Convert the resized image to a bytes object
        img_byte_arr = io.BytesIO()
        resized_img.save(img_byte_arr, format=img.format)
        
        # Encode the image in base64
        base64_encoded_image = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        return base64_encoded_image

# Correctly setting up the base directory path
base_dir = r"C:\Users\ramna\Desktop\lec2notes\backend"  # Using a raw string for the file path

# Initialize an empty string to hold all descriptions
all_descriptions = ""

# Looping through each image
for i in range(1, 4):
    image_path = f"{base_dir}\\{str(i).zfill(4)}.jpg"
    base64_image = resize_and_encode_image(image_path, 256)

    # Prepare the payload correctly for the API request
    payload = {
        "model": "gpt-4-vision-preview",
        # "messages": [
        #     {
        #         "role": "user",
        #         "content": "What’s in this image?"
        #     },
        #     {
        #         "type": "image_url",
        #         "image_url": {
        #         "content": f"data:image/jpeg;base64,{base64_image}"
        #     }
        # ],
        # "max_tokens": 700
        "messages": [
        {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": ("You are a notes transcriber for blind people in my algorithms class. Look at the images and construct a comprehensive series of class notes. The following information is the previous slides' information, use them as context to build the notes. If CONTENT is empty or just logistical class stuff, that's fine, transcribe it anyways as those are probably just the first couple of slides. Don't worry about personal information, I'm a student at Vanderbilt. CONTENT: "+ all_descriptions)
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 900
    }

    # Attempting the request to the OpenAI API
    try:
        result = client.chat.completions.create(**payload)

        if result.choices and len(result.choices) > 0:
            description = result.choices[0].message.content
            all_descriptions += description + "\n"
    except Exception as e:
        print(f"An error occurred: {str(e)}")

print(all_descriptions)


#upload file to node -> send to flask -> convert pdf to images in flask -> run api calls -> get text -> return back to nextjs