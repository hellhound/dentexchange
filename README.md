Dentexchange
============


Server Requirements
===================
* Ubuntu 12.04 LTS
* Git 1.7+
* Python 2.7
* Pip 1.5+
* virtualenvwrapper 4.2
* Nginx 1.1+
* PostgreSQL 9.1+
* RabbitMQ 2.7+
* Solr 4.9.0+
* GEOS 3.2.2+
* PROJ.4 4.7+
* PostGIS 1.5+
* SpatiaLite 3.0+


System Requirements Instructions
================================

First, we need to create a system acccount that we can use to run the web app
daemon without root priviledges for security reasons:

```sh
sudo adduser --disabled-password select_a_proper_username_matching_projects_name
```

The previous step will create a user, a group with the same name as the user and
the user's home directory. 

Install build essentials and Python header files

```sh
sudo aptitude install build-essential automake autoconf libtool python-dev \
    postgresql-server-dev-9.1 libxml2-dev libxslt1-dev
```

Install git

```sh
sudo aptitude install git-core
```

We need to install the python-pip package to be so that we can be able to
install the virtualenvwrapper afterwards

```sh
sudo aptitude install python-pip
```

Install virtualenvwrapper using the pip command. virtualenvwrapper will
allow us to create several virtualenv environments manageable through practical
commands like `workon`, `mkvirtualenv`, etc; which should be very helpful for
automated deployment scripts

```sh
sudo pip install virtualenvwrapper
``` 

Install nginx

```sh
sudo aptitude install nginx nginx-light
```

Configure nginx so that it remains as a balanced reverse proxy, forwarding
everything relayed through the local port 9000 into the port 80.
To do this, create a file (i.e. example`_com) into
`/etc/nginx/sites-available` with the following configuration:

```nginx
server {
    listen 80;
    listen 443 default ssl;
    include mime.types;
    default_type application/octect-stream;
    sendfile on;
    keepalive_timeout 65;
    #https://github.com/kaleidos/django-validated-file#note-on-dos-attacks
    client_max_body_size 100M;

    root /usr/share/nginx/www;
    index index.html index.htm;

    # Make site accessible from http://localhost/
    server_name put.the.web.app.domain.name.here;

    location /static/ {
        alias /path/to/djangos/static/files/;
        expires 30d;
    }

    location /media/ {
        alias /path/to/djangos/media/files/;
        expires 30d;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass https://127.0.0.1:9000;
        #proxy_pass_header Server;
        proxy_set_header X-Real-IP $remote_addr;
        #proxy_set_header X-Scheme $scheme;
        proxy_connect_timeout 10;
        proxy_read_timeout 10;
        #proxy_set_header SCRIPT_NAME /;
    }

    if ($ssl_protocol = "") {
        # TODO replace 107.170.145.112 with $server_name
        rewrite ^/(.*) https://107.170.145.112/$1 permanent;
    }

    # ssl configuration
    ssl on;
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/key.key;
    ssl_protocols SSLv3 TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers RC4:HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
}
```

Create a symlink to this file inside the `/etc/nginx/sites-enabled`
directory.

```sh
sudo ln -s /etc/nginx/sites-available/your_site_configuration \
    /etc/nginx/sites-enabled
```

Now install postgresql and then configure a user and assign the proper
permissions for it to be able to create databases and access them

```sh
sudo aptitude install postgresql-9.1
sudo su - postgres
psql -c "create role selected_username; \
    alter role selected_username with createdb login;"
exit
```

Install RabbitMQ

```sh
sudo aptitude install rabbitmq-server
```

Add sudoer permissions to allow the project's user to run rabbitmqctl without
inputing a password

```sh
echo "dentexchange ALL=NOPASSWD: /usr/sbin/rabbitmqctl" \
    | sudo tee -a /etc/sudoers
```

Finally, we'll have to configure the system account's home directory to be able
to use virtualenvwrapper, log supervisord and gunicorn outputs, and for storing
the pidfiles for each supervisord job

```sh
sudo su - dentexchange
mkdir -p var/log var/run projects
echo source /usr/local/bin/virtualenvwrapper.sh >> ~/.profile
```

Adding Authentication to Nginx

Follow the instructions described here https://www.digitalocean.com/community/tutorials/how-to-set-up-http-authentication-with-nginx-on-ubuntu-12-10

Install Apache Solr

We need Solr for haystack-based full-text searches. First we need to install
Java's JRE

```sh
sudo aptitude install openjdk-7-jre-headless
```

Download and Install Apache Solr

```sh
sudo su - <projects_username>
mkdir -p projects/solr
cd projects/solr
wget http://archive.apache.org/dist/lucene/solr/4.9.0/solr-4.9.0.tgz
tar xf solr-4.9.0.tgz
rm solr-4.9.0.tgz
ln -s solr-4.9.0 current
cd current/example/solr
mv collection1 <project_name>
rm <project_name>/README.txt
echo "name=<project_name>" > <project_name>/core.properties
rm <project_name>/conf/schema.xml
rm -rf <project_name>/data/*
ln -s ~/projects/<project_dir>/<project_name>/data/schema.xml \
    <project_name>/conf/schema.xml
ln -s <project_name>/conf/stopwords.txt <project_name/conf/stopwords_en.txt
```

Install GEOS, PROJ.4, SpatiaLite and PostGIS

```sh
sudo aptitude install libgeos-c1 libproj0 postgis libspatialite3
```
