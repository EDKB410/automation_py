#!/bin/sh

OPENCART_PORT=8080 PHPADMIN_PORT=8888 LOCAL_IP=opencart docker-compose up -d
#LOCAL_IP=$(hostname -I | grep -o "^[0-9.]*") docker-compose up -d
