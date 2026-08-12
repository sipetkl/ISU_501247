#!/bin/bash
brightnessctl set "$1"
CURRENT=$(brightnessctl g)
MAX=$(brightnessctl m)
PERCENT=$((100 * CURRENT / MAX))

dunstify -h string:x-dunst-stack-tag:brightness \
         -h int:value:"$PERCENT" \
         -t 1500 \
         "Яркость: $PERCENT%"
