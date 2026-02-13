# Use the official Python 3.10 image
FROM python:3.10

# Set the working directory to /code
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code

# Install requirements
# We use --no-cache-dir to keep the image small
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Create a directory for the database instance if it doesn't exist
# and ensure it's writable by the user running the app (User 1000 in HF Spaces)
RUN mkdir -p /code/instance && chmod -R 777 /code/instance && chmod -R 777 /code

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Run the application with Gunicorn
# Bind to 0.0.0.0:7860
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:7860"]
