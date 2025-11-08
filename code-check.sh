#!/bin/bash
set -e

ruff check .
mypy .
pytest .