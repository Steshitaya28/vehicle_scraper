import os
import difflib
from scripts.image_scraper import sanitize_model_name

def fetch_image_path(car_model, car_images_dir='static'):
    sanitized_model = sanitize_model_name(car_model)
    available_images = os.listdir(car_images_dir)

    # Find the closest match
    closest_matches = difflib.get_close_matches(sanitized_model, available_images, n=1, cutoff=0.5)

    if closest_matches:
        image_path = os.path.join(car_images_dir, closest_matches[0])
        if os.path.exists(image_path):
            return image_path
    return None

# Example usage
if __name__ == "__main__":
    user_input = "MARUTI SUZUKI INDIA LTD VITARA BREZZA ZXI+1.5L 5MT BS6"
    image_path = fetch_image_path(user_input)
    if image_path:
        print(f"Image found: {image_path}")
    else:
        print("Image not found.")
