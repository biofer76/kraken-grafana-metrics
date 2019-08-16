#!/usr/bin/env bash
docker run --rm -t --name "kraken-grafana-metrics" \
    -v $PWD:/app \
    --network=grafana-influxdb-docker_grafana-influxdb \
    --env-file .env \
    kraken-grafana-metrics python app.py