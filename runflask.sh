#!/bin/bash

CONFIGFILE="./configs/uwsgihttpdev.ini"

uwsgi --ini $CONFIGFILE $*
