#!/bin/bash
exec poetry run rasa run --enable-api --cors "http://mika.lehre.hwr-berlin.de:5173"
