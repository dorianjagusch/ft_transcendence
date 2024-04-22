FROM nginx:latest

COPY ./nginx.conf /etc/nginx/nginx.conf

COPY ./index.html /usr/share/nginx/html/index.html
COPY ./pages /usr/share/nginx/html/pages/
COPY ./static /usr/share/nginx/html/static/

CMD ["nginx", "-g", "daemon off;"]