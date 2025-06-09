#!/bin/bash
exec poetry run rasa run --enable-api --cors "http://localhost:5173"
