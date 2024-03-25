#!/bin/sh

OPENCART_PORT=8081 PHPADMIN_PORT=8888 LOCAL_IP=opencart docker-compose down
#LOCAL_IP=$(hostname -I | grep -o "^[0-9.]*") docker-compose down
