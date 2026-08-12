"""Project Nardole."""

import logging

from nardole.core import Nardole

# Start ArcSearch
if __name__ == "__main__":
    handler = logging.FileHandler("parse.log", "w")
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[handler],
    )
    nardole = Nardole()
    nardole.initialize()
