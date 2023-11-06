#!/bin/bash
psql postgres -c "CREATE DATABASE btcrate_dbase WITH ENCODING 'UTF8'"
psql postgres -c "CREATE USER btcrate_user WITH PASSWORD 'btcrate_pass'"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE btcrate_dbase TO btcrate_user"

psql postgres -c "ALTER SCHEMA public OWNER TO btcrate_user"
psql postgres -c "GRANT ALL ON SCHEMA public TO btcrate_user"
psql postgres -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO btcrate_user"
psql postgres -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO btcrate_user"
psql postgres -c "GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO btcrate_user"
psql postgres -c "GRANT USAGE ON SCHEMA public TO btcrate_user"


psql postgres -c "ALTER DATABASE btcrate_dbase OWNER TO btcrate_user"