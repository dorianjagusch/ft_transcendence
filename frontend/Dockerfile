FROM nginx:1.25.5

COPY ./nginx.conf /etc/nginx/nginx.conf

COPY ./index.html /usr/share/nginx/html/index.html
COPY ./privacypolicy.html /usr/share/nginx/html/privacypolicy.html
COPY ./static /usr/share/nginx/html/static/

CMD ["nginx", "-g", "daemon off;"]