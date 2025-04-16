set -eu

export PYTHONUNBUFFERED=true

VIRTUALENV=./venv

if [ ! -d $VIRTUALENV ]; then
  python3 -m venv $VIRTUALENV
fi

if [ ! -f $VIRTUALENV/bin/pip ]; then
  curl --silent --show-error --retry 5 https://bootstrap.pypa.io/pip/3.7/get-pip.py | $VIRTUALENV/bin/python
fi

$VIRTUALENV/bin/pip install -r requirements.txt

# Run your glorious application
$VIRTUALENV/bin/python3 alise.py