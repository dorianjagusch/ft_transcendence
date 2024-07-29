#!/bin/sh

mkdir -p /etc/nginx/ssl

openssl req -newkey rsa:2048 -x509 -sha256 -days 365 -nodes \
	-out /etc/nginx/ssl/certificate.crt \
	-keyout /etc/nginx/ssl/certificate.key \
	-subj "/C=FI/ST=Helsinki/L=Helsinki/O=Hive/OU=transcendence/CN=transcendence.42.fi"