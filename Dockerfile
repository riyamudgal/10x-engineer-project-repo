# Use the Python 3.11 slim image as the base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the Docker image
COPY backend/requirements.txt /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the Docker image
COPY backend/ /app/

# Command to run the application
CMD ["python", "main.py"]
