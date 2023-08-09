"""
Script for checking that a database server is available.
Essentially a cross-platform, database agnostic mysqladmin.
"""
import time

from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy import pool

from CTFd.config import Config

url = make_url(Config.DATABASE_URL)

# Ignore sqlite databases
if url.drivername.startswith("sqlite"):
    exit(0)

# Null out the database so raw_connection doesnt error if it doesnt exist
# CTFd will create the database if it doesnt exist
url = url._replace(database=None)

# Wait for the database server to be available
engine = create_engine(url, convert_unicode=True, connect_args=dict(use_unicode=True), poolclass=pool.NullPool)
print(f"Waiting for {url.host} to be ready")
while True:
    try:
        engine.raw_connection()
        break
    except Exception as e:
        print(f". (Error: {e})", end="", flush=True)
        print(".", end="", flush=True)
        time.sleep(1)

print(f"{url.host} is ready")
time.sleep(1)
