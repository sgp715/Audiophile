# Audiophile
If you are like me, sometimes you get tired of staring at the screen. Or if you're like me you sometimes just don't want to read. Well, Audiophile is here to help. It periodically scrapes the New York Times best articles and generates a narration of them. Then all you have to do is click play and you have the sweet sounds of a robotic female voice whispering geopolitical nothings into your ear. You can check out the hosted version or clone this repo and run it locally.

## Setup
  * Install Docker
  * Go to https://newsapi.org and get a key
  * Open up the docker file and replace [API_KEY] with your key
  * To build the docker image
  ```
  $ docker build -t audiophile .
  ```
## Run
  * To run the a container from the image (NOTE: this will take a while because it scrapes everything initially; be patient :) )
  ```
  $ docker run --name phile -p 0.0.0.0:[PORT]:80 audiophile -d
  ```
  * Subsequently, to start or stop the container use
  ```
  $ docker start/stop phile
  ```
