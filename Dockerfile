# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Create a directory for storing images
RUN mkdir -p car_images

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the Flask app
CMD ["python", "main.py"]
