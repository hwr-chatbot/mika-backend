#!/bin/bash
exec poetry run rasa run actions --cors "http://mika.lehre.hwr-berlin.de:5173"
