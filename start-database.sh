mkdir -p /var/moisture-db-files
docker run --name moisture-mysql \
    -v /var/moisture-db-files:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=changeme \
    -e MYSQL_DATABASE=moisture-db \
    -e MYSQL_USER=moisture_db_admin \
    -e MYSQL_PASSWORD=changeme \
    -p 3306:3306 \
    -d hypriot/rpi-mysql