# Use an official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy required files
COPY . /app

# Install dependencies (including cryptography)
RUN pip install flask cryptography

# Expose port
EXPOSE 5050

# Command to run Flask app
CMD ["python", "server.py"]
