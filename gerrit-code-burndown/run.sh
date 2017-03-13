#!/usr/bin/env bash

REPO_DIRECTORY=/home/macsz/repos/nova

function log {
    echo \[`date`\] - $1
}

if [ ! -d "$REPO_DIRECTORY" ]; then
  log "Code repository does not exist. Cloning..."
  git clone git://git.openstack.org/openstack/nova
  log "Repository has beed cloned."
else
  log "Code repository exists. Pulling newest version."
  pushd .
  cd $REPO_DIRECTORY
  git checkout master
  git pull --rebase
  popd
  log "Repository has been updated."
fi

log "Starting gathering data."

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHONPATH=$PYTHONPATH:$DIR
source $DIR/../.venv/bin/activate

log "Running python scripts..."
python $DIR/main.py
