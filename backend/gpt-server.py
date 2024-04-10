from openai import OpenAI
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
load_dotenv()  



from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import os
from openai import OpenAI
import base64
from PIL import Image
import io

app = Flask(__name__)

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def convert_pdf_to_images(pdf_bytes):
    images = []
    doc = fitz.open("pdf", pdf_bytes)
    for page in doc:
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))
        images.append(img)
    return images

def resize_and_encode_image(image, resize_width):
    aspect_ratio = image.height / image.width
    new_height = int(resize_width * aspect_ratio)

    resized_img = image.resize((resize_width, new_height))

    img_byte_arr = io.BytesIO()
    resized_img.save(img_byte_arr, format='JPEG')  # Saving as JPEG for consistency
    resized_img.save("temp_resized_image.jpg")
    base64_encoded_image = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    return base64_encoded_image

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # Convert the uploaded PDF file to images
        images = convert_pdf_to_images(file.read())

        all_descriptions = ""
        for image in images:
            base64_image = resize_and_encode_image(image, 256)
            payload = {
                "model": "gpt-4-vision-preview",
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
  "max_tokens": 2000
    }
            try:
                result = client.chat.completions.create(**payload)
                if result.choices and len(result.choices) > 0:
                    description = result.choices[0].message.content
                    all_descriptions += description + "\n"
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        return jsonify({'description': all_descriptions}), 200

    return jsonify({'error': 'File processing failed'}), 400

if __name__ == '__main__':
    app.run(debug=True)

