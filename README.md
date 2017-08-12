# Audiophile

## Setup
  * Install Docker
  * Go to https://newsapi.org and get a key
  * Open up the docker file and replace [API_KEY] with your key
  * To build the docker image
  ```
  $ docker build -t audiophile .
  ```
## Run
  * To run the a container from the image
  ```
  $ docker run --name phile -p 0.0.0.0:[PORT]:80 audiophile -d
  ```
  * Subsequently, to start or stop the container use
  ```
  $ docker start/stop phile
  ```
