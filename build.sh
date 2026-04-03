#!/bin/bash
# Local build/preview for the course site
cd "$(dirname "$0")"
rm -rf docs/lessons
cp -r lessons docs/lessons
mkdocs serve
