# Docker Image for Binder

<!--
This is derived from the following setup:
https://github.com/RobotLocomotion/drake/tree/dc2a9394d/.binder
-->

*Note that due to Binder conventions, this directory MUST always be in the root
of the repository and named either `binder` or `.binder`. This image is NOT
intended for use by most developers or users.*

These instructions are for running the image locally. For Binder itself, you
should only need to visit the link from the root-level README.

To create a Docker image and run a Docker container similar to those used by
[Binder](https://mybinder.org) for local debugging purposes, execute the
following `build` and `run` commands from the top level of this Git repository:

```bash
docker build -f .binder/Dockerfile -t binder .
docker run --rm -it --name mybinder -p 8888:8888 binder
```

For the URLs printed, only open the `127.0.0.1:8888` URL (including the login
token) in a web browser on your host system.

To stop the running container, simply exit it from the terminal with Ctrl+C.

*Note*: If you want to test the Docker image with the current source tree
(without copying, so you can modify source files), insert the arguments
`-v "${PWD}:/home/jovyan/pygccxml"` before the image name (`binder`) to mount it
directly. This will *not* act on any changes to `./setup.py`.
