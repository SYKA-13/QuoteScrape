# Dockerfile
FROM python:3.11

# Set the working directory
WORKDIR /myapp

# Copy and Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy Selenium script
COPY scraper.py .

# Execute the script
CMD ["python", "scraper.py"]

