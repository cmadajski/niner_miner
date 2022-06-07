#!/bin/sh
# stop supervisord process for niner miner app
sudo supervisord stop niner_miner
# pull most recent changes from the repo
git pull origin main
# restart supervisord process for niner miner app
sudo supervisord start niner_miner