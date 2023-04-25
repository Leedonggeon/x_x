# Use the official Python base image with Python 3.10.9
FROM python:3.10.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .



# Install the Python dependencies
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose a port for the application to run on (if needed)
EXPOSE 8000

# Start the application (replace with your own command)
CMD ["python", "app.py"]
