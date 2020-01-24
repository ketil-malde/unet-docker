# Change the configuration here:
IMAGENAME = docker-test
COMMAND   = bash
# No need to change anything below this line

# Allows you to use sshfs to mount disks
SSHFSOPTIONS = --cap-add SYS_ADMIN --device /dev/fuse

.docker: Dockerfile
	docker build -t $(IMAGENAME) .
	touch .docker

# Using -it for interactive use
RUNCMD=docker run --rm $(SSHFSOPTIONS) -it $(IMAGENAME)  

# Replace 'bash' with the command you want to do
default: .docker
	$(RUNCMD) $(COMMAND)

