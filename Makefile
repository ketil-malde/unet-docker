# Change the configuration here.
# Include your useid/name as part of IMAGENAME to avoid conflicts
IMAGENAME = unet
CONFIG    = tensorflow
COMMAND   = bash
DISKS     = -v $(PWD)/../imagesim-docker:/data:ro -v $(PWD):/project
# DISKS     = -v /data/deep/data:/data:ro -v $(PWD):/project
PORT      =
GPU       = 0
RUNTIME   = --gpus device=$(GPU)
# No need to change anything below this line
USERID    = $(shell id -u)
GROUPID   = $(shell id -g)
USERNAME  = $(shell whoami)

# Allows you to use sshfs to mount disks
SSHFSOPTIONS = --cap-add SYS_ADMIN --device /dev/fuse

USERCONFIG   = --build-arg user=$(USERNAME) --build-arg uid=$(USERID) --build-arg gid=$(GROUPID)

.docker: docker/Dockerfile
	docker build $(USERCONFIG) -t $(USERNAME)-$(IMAGENAME) -f docker/Dockerfile docker

# Using -it for interactive use
RUNCMD=docker run $(RUNTIME) --rm --user $(USERID):$(GROUPID) $(PORT) $(SSHFSOPTIONS) $(DISKS) -it $(USERNAME)-$(IMAGENAME)

# Replace 'bash' with the command you want to do
default: .docker
	$(RUNCMD) $(COMMAND)

train: .docker
	$(RUNCMD) python3 /src/train.py

test: .docker
	$(RUNCMD) python3 /src/test.py
