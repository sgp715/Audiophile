# Audiophile

## Startup server
* Manually
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

  6. start the server
  ```
  $ gunicorn -b 127.0.0.1:80 app:app
  ```
* Run the startup.sh script

## Start the scraper
1. Create a environment variable for the projcet home
```
$ export PHILE_HOME=~/Audiophile
```
2. Create the following cronjob by running <code> crontab -e </code>
```
0 0 * * * $PHILE_HOME/phile/bin/python3.5 $PHLE_HOME/audiophile.py
```
