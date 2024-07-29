#!/bin/sh

SSL_KEY_PATH="/app/ssl/certificate.key"
SSL_CERT_PATH="/app/ssl/certificate.crt"

mkdir -p /etc/ssl

openssl req -newkey rsa:2048 -x509 -sha256 -days 365 -nodes \
	-out  ${SSL_CERT_PATH}\
	-keyout ${SSL_KEY_PATH}\
	-subj "/C=FI/ST=Helsinki/L=Helsinki/O=Hive/OU=transcendence/CN=transcendence.42.fi"