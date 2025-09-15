#!/bin/bash
git pull origin main
docker-compose down
docker-compose up -d --build
sudo systemctl restart nginx
