import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the Excel file and extract the car models
def load_car_models(excel_path):
    df = pd.read_excel(excel_path)
    return df.apply(lambda row: f"{row['Brand']} {row['Models']}", axis=1).tolist()

def fetch_image(query):
    search_query = quote_plus(query)
    search_url = f"https://www.google.com/search?tbm=isch&q={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tags = soup.find_all("img")
    img_urls = [img['src'] for img in image_tags if 'http' in img['src']]
    return img_urls[0] if img_urls else None

def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)

def scrape_images(car_models_list):
    os.makedirs('car_images', exist_ok=True)
    for car_model in car_models_list:
        sanitized_model = sanitize_model_name(car_model)
        save_path = os.path.join('car_images', f"{sanitized_model}.jpg")

        if not os.path.exists(save_path):
            logging.info(f"Fetching image for: {car_model}")
            img_url = fetch_image(car_model)
            if img_url:
                download_image(img_url, save_path)
                logging.info(f"Downloaded: {car_model} as {sanitized_model}.jpg")
            else:
                logging.warning(f"Image not found for: {car_model}")
        else:
            logging.info(f"Image already exists for: {car_model}, skipping download.")

def sanitize_model_name(model_name):
    return model_name.replace(' ', '_').replace('/', '_').replace('\\', '_').replace('+', '_').replace('.', '_').replace('-', '_').upper()

if __name__ == "__main__":
    excel_path = 'scripts/Vehicle_Models.xlsx'
    car_models_list = load_car_models(excel_path)
    scrape_images(car_models_list)
