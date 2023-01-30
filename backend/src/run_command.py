import logging

import click

from settings import settings


@click.group()
def root():
    pass


@root.command()
def init_views():
    from database import db

    logging.info("Initializing views")
    with open("init.sql", "r") as f:
        db.execute_sql(f.read())

    logging.info("Views initialized")


if __name__ == "__main__":
    logging.basicConfig(level=settings.log_level, format=settings.log_format)
    root()
