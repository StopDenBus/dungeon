#!/bin/bash

coverage run -m nose
coverage report --omit=env/*,tests/*,python/*
coverage html --omit=env/*,tests/*,python/*
