#!/usr/bin/env bash
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
export PYTHONPATH=$SCRIPTPATH:$PYTHONPATH
cd $SCRIPTPATH/devops
python spawn_server.py
sleep 5
ansible-playbook -i hosts setup_server.yml
ansible-playbook -i hosts deploy.yml
