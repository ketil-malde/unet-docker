# Change the configuration here.
# Include your useid/name as part of IMAGENAME to avoid conflicts
IMAGENAME = docker-test
COMMAND   = bash
DISKS     = -v /data/deep/data:/data:ro -v $(PWD):/project
USERID    = $(shell id -u)
GROUPID   = $(shell id -g)
USERNAME  = $(shell whoami)
PORT      = -p 8888:8888
RUNTIME   =
# --runtime=nvidia 
# No need to change anything below this line

# Allows you to use sshfs to mount disks
SSHFSOPTIONS = --cap-add SYS_ADMIN --device /dev/fuse

.docker: Dockerfile requirements-apt.txt requirements-pip.txt
	docker build --build-arg user=$(USERNAME) --build-arg uid=$(USERID) --build-arg gid=$(GROUPID) -t $(USERNAME)-$(IMAGENAME) .
	touch .docker

# Using -it for interactive use
RUNCMD=docker run $(RUNTIME) --rm --user $(USERID):$(GROUPID) $(PORT) $(SSHFSOPTIONS) $(DISKS) -it $(USERNAME)-$(IMAGENAME)

# Replace 'bash' with the command you want to do
default: .docker
	$(RUNCMD) $(COMMAND)

jupyter:
	$(RUNCMD) jupyter notebook --ip '$(hostname -I)' --port 8888
