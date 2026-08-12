#!/bin/bash
COLORS="$HOME/.cache/wal/colors"

color0=$(sed -n '1p' "$COLORS")
color4=$(sed -n '5p' "$COLORS")
color5=$(sed -n '6p' "$COLORS")
foreground=$(sed -n '8p' "$COLORS")

sed \
    -e "s/{color0}/$color0/g" \
    -e "s/{color4}/$color4/g" \
    -e "s/{color5}/$color5/g" \
    -e "s/{foreground}/$foreground/g" \
    "$HOME/.config/dunst/dunstrc.template" > "$HOME/.config/dunst/dunstrc"

pkill -KILL dunst
sleep 0.3
dunst &
disown
