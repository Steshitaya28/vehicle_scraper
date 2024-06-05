import os
from scripts.image_scraper import load_car_models, scrape_images
from scripts.image_fetcher import fetch_image_path

def main():
    # Scrape images first
    excel_path = 'scripts/Vehicle_Models.xlsx'
    car_models_list = load_car_models(excel_path)
    scrape_images(car_models_list)

    # Prompt user for input
    user_input = input("Enter the car model: ")

    # Fetch an image for the specific car model
    image_path = fetch_image_path(user_input)
    if image_path:
        print(f"Image found: {image_path}")
    else:
        print("Image not found. Attempting to fetch and download the image.")

        # If image is not found, try to fetch and download it
        from scripts.image_scraper import fetch_image, download_image, sanitize_model_name

        img_url = fetch_image(user_input)
        if img_url:
            sanitized_model = sanitize_model_name(user_input)
            save_path = os.path.join('car_images', f"{sanitized_model}.jpg")
            download_image(img_url, save_path)
            print(f"Downloaded and saved image: {save_path}")
        else:
            print("Failed to find and download the image.")

if __name__ == "__main__":
    main()
