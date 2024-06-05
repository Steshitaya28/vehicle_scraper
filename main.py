from flask import Flask, request, render_template
from scripts.image_fetcher import sanitize_model_name, fetch_image_path
from scripts.image_scraper import fetch_image, download_image
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_image', methods=['POST'])
def fetch_image_endpoint():
    car_model = request.form['car_model']
    
    if not car_model:
        return render_template('index.html', error="No car model provided")
    
    sanitized_model = sanitize_model_name(car_model)
    image_path = fetch_image_path(car_model)

    if image_path:
        image_url = f"/car_images/{os.path.basename(image_path)}"
        return render_template('index.html', car_model=car_model, image_url=image_url)
    
    # If image is not found, fetch and save it
    img_url = fetch_image(car_model)
    if img_url:
        save_path = os.path.join('car_images', f"{sanitized_model}.jpg")
        download_image(img_url, save_path)
        
        image_url = f"/car_images/{os.path.basename(save_path)}"
        return render_template('index.html', car_model=car_model, image_url=image_url)
    else:
        return render_template('index.html', error="Failed to find and download the image")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000 , debug = True)
