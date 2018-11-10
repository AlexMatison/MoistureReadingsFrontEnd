docker run --name moisture-web-container \
    -p 5000:5000 \
    --link moisture-mysql \
    -d moisture-web:latest