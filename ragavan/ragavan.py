"""Ragavan - MTG limited analysis"""
from logging import INFO, basicConfig, getLogger
from os import environ

from ragavan.app import app
from ragavan.ui.layout import layout


def main():
    """Main entrypoint of the program"""
    debug = bool(environ.get("RAGAVAN_DEBUG"))
    basicConfig(level=INFO)
    log = getLogger("ragavan")
    log.info("Ragavan starting")
    app.layout = layout()
    app.run(host="0.0.0.0", port=8050, debug=debug)
