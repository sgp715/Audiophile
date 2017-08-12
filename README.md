# Audiophile

<<<<<<< HEAD
## Install
=======
## Startup server
* sudo apt-get install virtualenv
>>>>>>> 6f58d31c34b3217fb7d908b9222827ca6b2548b3
* Manually
  ### Startup Flask server
    1. clone the repo
    2. cd into the repo and create a virtual environment
    ```
    $ virtualenv venv --python=python3.5
    ```
    3. create a file called config.json and put in the api key
    ```
    {"key":"api_key"}
    ```

    4. make the static folder
    ```
    mkdir static
    ```

<<<<<<< HEAD
    6. start the server
    ```
    $ gunicorn -b 127.0.0.1:80 app:app
    ```
  * Run the startup.sh script

  ### Configure Apache
    1. https://www.vioan.eu/blog/2016/10/10/deploy-your-flask-python-app-on-ubuntu-with-apache-gunicorn-and-systemd/
=======
  6. start the server
  ```
  $ gunicorn -b 127.0.0.1:80 app:app
  ```
* Run the startup.sh script
  1. give it permissions to execute
  ```
  $ chmod +x start.sh
  ```
>>>>>>> 6f58d31c34b3217fb7d908b9222827ca6b2548b3

  ### Start the scraper
  1. create the following cronjob by running <code> crontab -e </code>
  ```
  0 0 * * * [PHILE_HOME]/phile/bin/python3.5 [PHLE_HOME]/audiophile.py
  ```
    * where [PHILE_HOME] is wherever the package was installed
  * Docker
    1. Install Docker
    2. To build the docker image
    ```
    $ docker build -t audiophile .
    ```
    3. To run the a container from the image
    ```
    $ docker run --name phile -p 0.0.0.0:[PORT]:80 audiophile -d
    ```
