#!/usr/bin/env bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER nse WITH PASSWORD 'nse';
    CREATE DATABASE nse;
    GRANT ALL PRIVILEGES ON DATABASE nse TO nse;
EOSQL
