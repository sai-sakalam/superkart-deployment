FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to the container's working directory
COPY . .

# Install dependencies from the requirements file
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Run the Flask app with gunicorn on port 7860 (the Hugging Face Spaces port)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:7860", "app:app"]
