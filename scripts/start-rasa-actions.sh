#!/bin/bash
exec poetry run rasa run actions --cors "http://localhost:5173"
