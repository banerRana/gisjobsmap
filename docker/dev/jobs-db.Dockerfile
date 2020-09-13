FROM postgis/postgis:12-master

ADD ./init-test-db.sh /docker-entrypoint-initdb.d/init-test-db.sh