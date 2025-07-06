FROM harbor.pg.innopolis.university/docker-hub-cache/ubuntu

RUN apt update && apt install --no-install-recommends -y nginx && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["nginx", "-g", "daemon off;"]
