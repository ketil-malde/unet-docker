# Use an official Python runtime as a parent image
FROM nvidia/cuda

# Set the working directory to 
WORKDIR /project

# Copy what you need into the working directory
COPY requirements.txt /project

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y python3 python3-pip sshfs
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
# EXPOSE 80

# Define environment variable
# Use only GPU 0
ENV CUDA_VISIBLE_DEVICES 0

# Run when the container launches
CMD "bash"