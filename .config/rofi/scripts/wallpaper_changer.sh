#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/wallpaper_common.sh"

wallpaper_setup "wallpaper_changer.sh"
require_command rofi

if [[ -r "$HOME/.cache/wal/colors.sh" ]]; then
    set +u
    source "$HOME/.cache/wal/colors.sh" >/dev/null 2>&1 || true
    set -u
fi
BG="${background:-#11121a}"
FG="${foreground:-#e8e8e8}"
AC="${color4:-${color5:-#7aa2f7}}"

ROFI_THEME="
* {
    bg: ${BG}E6;
    fg: ${FG};
    ac: ${AC};
    background-color: transparent;
    text-color: @fg;
}
window {
    background-color: @bg;
    border: 2px;
    border-color: @ac;
    border-radius: 16px;
    padding: 16px;
    width: 62%;
}
mainbox { children: [ listview ]; background-color: transparent; }
listview {
    columns: 3;
    lines: 2;
    spacing: 16px;
    fixed-height: false;
    background-color: transparent;
}
element,
element normal.normal,
element alternate.normal,
element normal.urgent,
element alternate.urgent,
element normal.active,
element alternate.active {
    background-color: transparent;
    text-color: ${FG}B3;
    orientation: vertical;
    padding: 6px;
    border: 2px;
    border-color: transparent;
    border-radius: 12px;
}
element selected.normal,
element selected.urgent,
element selected.active {
    background-color: ${AC}33;
    text-color: @fg;
    border-color: @ac;
}
element-icon {
    size: 15em;
    horizontal-align: 0.5;
    background-color: transparent;
}
element-text {
    enabled: false;
}
"

if ! WALLPAPER="$(wallpaper_print_menu_entries | rofi -dmenu \
        -show-icons -no-custom -p "" \
        -kb-move-char-back "" \
        -kb-move-char-forward "" \
        -kb-row-left  "h,Left" \
        -kb-row-down  "j,Down" \
        -kb-row-up    "k,Up" \
        -kb-row-right "l,Right" \
        -kb-accept-entry "Return,KP_Enter,space" \
        -kb-cancel "Escape,q,Control+g" \
        -kb-remove-char-back "BackSpace" \
        -kb-element-next "" \
        -kb-element-prev "" \
        -kb-mode-next "" \
        -kb-mode-previous "" \
        -theme-str "$ROFI_THEME")"; then
    exit 0
fi

[[ -n "$WALLPAPER" ]] || exit 0

wallpaper_apply "$WALLPAPER" "random"
