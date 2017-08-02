# create the virtualenv and start
virtualenv phile --python=python3.5
source phile/bin/activate

# create the dumby config file
echo '{"key":"api_key"}' > config.sh

pip3 install -r requirements.txt 

mkdir static

export PHILE_HOME=~/Audiophile

gunicorn app:app

