# Audiophile

## Install
  * Install Docker
  * To build the docker image
  ```
  $ docker build -t audiophile .
  ```
## Run
  * To run the a container from the image
  ```
  $ docker run --name phile -p 0.0.0.0:[PORT]:80 audiophile -d
  ```
