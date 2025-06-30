FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Copy only necessary files
COPY . /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y awscli && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Expose the port for FastAPI
EXPOSE 8000

# Use uvicorn to serve the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]