# Use an official Python runtime as a parent image
FROM tensorflow/tensorflow:1.15.2-gpu-py3

# Set the working directory to 
WORKDIR /project

# User configuration - override with --build-arg
ARG user=myuser
ARG group=mygroup
ARG uid=1000
ARG gid=1000

# Some debs want to interact, even with apt-get install -y, this fixes it
ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/project

# Install any needed packages from apt
RUN apt-get update && apt-get install -y sudo python3 python3-pip git

# Configure user
RUN groupadd -g $gid $user
RUN useradd -u $uid -g $gid $user
RUN usermod -a -G sudo $user
RUN passwd -d $user

# following https://machinelearningmastery.com/how-to-train-an-object-detection-model-with-keras/
RUN git clone https://github.com/rteuwens/Mask_RCNN.git
# The official version needs a small fix (https://github.com/matterport/Mask_RCNN.git)
RUN cd Mask_RCNN && python setup.py install

RUN pip3 install --trusted-host pypi.python.org numpy scipy Pillow cython matplotlib scikit-image keras>=2.0.8 opencv-python h5py imgaug IPython

COPY src /src

# Run when the container launches
CMD "bash"
