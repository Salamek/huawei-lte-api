#!/bin/bash
set -e

ruff check .
ruff format --check .
mypy .
pytest .
