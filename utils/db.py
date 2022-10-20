import time
import sys

from django.db import OperationalError, connections


def write(message):
    sys.stderr.write(message + "\n")
    sys.stderr.flush()


def database_ready(database: str = 'default', maximum_wait: int = 15) -> bool:
    write('Connecting to the database >>>')
    connected = False
    start = time.time()
    while not connected and time.time() - start < maximum_wait:
        try:
            connections[database].cursor().execute('SELECT 1')
            connected = True
        except OperationalError:
            time.sleep(maximum_wait // 3)
            write('Waiting for database...')
    if time.time() - start > maximum_wait:
        raise OperationalError(
            f'Could not connect to database after {maximum_wait} seconds.')
    return connected
