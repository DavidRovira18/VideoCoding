# Use an official Ubuntu runtime as a parent image
FROM ubuntu:latest

# Update and install necessary dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Define environment variable
ENV PATH="/app:${PATH}"

# Run ffmpeg when the container launches
CMD ["ffmpeg"]
