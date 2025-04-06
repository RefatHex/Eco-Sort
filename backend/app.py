from flask import Flask, request, jsonify
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tensorflow as tf
import io
import base64
import os

app = Flask(__name__)

# Load model
model = tf.keras.applications.ResNet50(weights='imagenet')

# Bin classification rules
BIN_RULES = {
    "yellow": ["bottle", "can", "wrapper", "cup", "packaging", "box", "cardboard", "plastic"],
    "purple": ["coffee", "mug"],
    "black": ["food", "tissue", "scrap", "banana", "apple", "orange", "paper towel", "leftovers"]
}

def add_label_to_image(image, label, bin_color):
    """Draw classification label directly on the image"""
    try:
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        draw = ImageDraw.Draw(image)
        
        # Use a larger font
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Determine text color based on bin color
        text_color = "black" if bin_color == "yellow" else "white"
        box_color = {
            "yellow": "#FFFF00",
            "purple": "#800080", 
            "black": "#000000"
        }.get(bin_color, "#000000")
        
        # Draw background rectangle
        draw.rectangle([(10, 10), (400, 90)], fill=box_color)
        
        # Draw text
        draw.text((20, 20), f"{label.capitalize()}\n{bin_color.capitalize()} Bin", 
                 font=font, fill=text_color)
        
        return image
    except Exception as e:
        print(f"Error annotating image: {e}")
        return image

@app.route('/classify_image', methods=['POST'])
def classify_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    image_file = request.files['image']
    
    try:
        # Open and process image
        image = Image.open(image_file.stream)
        
        # Classification
        img_for_pred = image.resize((224, 224))
        x = np.array(img_for_pred, dtype=np.float32)
        x = np.expand_dims(x, axis=0)
        x = tf.keras.applications.resnet50.preprocess_input(x)
        
        preds = model.predict(x)
        label = tf.keras.applications.resnet50.decode_predictions(preds, top=1)[0][0][1].lower()
        
        # Determine bin
        bin_color = "black"  # default
        for color, keywords in BIN_RULES.items():
            if any(keyword in label for keyword in keywords):
                bin_color = color
                break
        
        # Add label to original image
        annotated_img = add_label_to_image(image.copy(), label, bin_color)
        
        # Convert annotated image to base64
        buffered = io.BytesIO()
        annotated_img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Prepare response
        response = {
            "detected_object": label,
            "disposal_bin": f"{bin_color} bin",
            "labeled_image": f"data:image/jpeg;base64,{img_str}"
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)