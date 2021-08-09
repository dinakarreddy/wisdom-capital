#!/usr/bin/env bash

POSTGRES_CONTAINER_NAME="assessment_engine_postgres"
PG_ISREADY="pg_isready -d nse -h localhost -p 5432"
PG_ISREADY_RESPONSE="localhost:5432 - accepting connections"

is_service_started() {
	CMD_RESPONSE=$(docker exec ${1} ${2})
	echo "$CMD_RESPONSE"
	if [ "$CMD_RESPONSE" == "$3" ]
	then
		return 0
	fi
	return 1
}

until is_service_started "$POSTGRES_CONTAINER_NAME" "$PG_ISREADY" "$PG_ISREADY_RESPONSE"; do
	echo "waiting for dependent services like postgres to start"
	sleep 2
done

echo "Started dependent services"
exit 0
