#!/usr/bin/env bash

UBUN="backendchallenge"
UBAK="711b8090e84dcb4981e6381b59757ac5c75ebb26"

curl -H "Authorization: ApiKey backendchallenge:711b8090e84dcb4981e6381b59757ac5c75ebb26" \
     -H "Content-Type: application/json" \
     -X GET https://sandbox.unbabel.com/tapi/v2/language_pair/