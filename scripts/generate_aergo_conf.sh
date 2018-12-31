#!/usr/bin/env bash

AERGO_SRC_PATH=$GOPATH/src/github.com/aergoio/aergo
python generate_aergo_conf.py $AERGO_SRC_PATH/config/types.go > ../aergo/herapy/obj/aergo_conf.py

