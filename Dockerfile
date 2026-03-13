# Use a slim version of Python to keep the image small
FROM python:3.12-slim

# Create a directory for our app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the libraries from your requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files into the container
COPY . .

# Render uses port 10000 by default for web services
ENV PORT=10000
EXPOSE 10000

# Start the server using Python
CMD ["python", "app_server.py"]