# Docker Image for Binder

<!--
This is derived from the following setup:
https://github.com/RobotLocomotion/drake/tree/dc2a9394d/.binder
-->

*Note that due to Binder conventions, this directory MUST always be in the root
of the repository and named either `binder` or `.binder`. This image is NOT
intended for use by most developers or users.*

To create a Docker image and run a Docker container similar to those used by
[Binder](https://mybinder.org) for local debugging purposes, execute the
following `pull`, `build`, and `run` commands from the top level of this Git
repository:

```bash
cd pygccxml
docker build -f .binder/Dockerfile -t binder .
docker run --rm -it --name mybinder -p 8888:8888 binder
```

Copy and paste the URL (including the login token) that is displayed in the
terminal into the web browser of your choice.

To stop the running container, simply exit it from the terminal with Ctrl+C.

*Note*: If you want to test the Docker image with the current source tree
(without copying, so you can modify source files), add the arguments
`-v ${PWD}:/home/jovyan/pygccxml` to mount it directly.
