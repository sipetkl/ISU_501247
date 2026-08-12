#!/bin/bash
# общая библиотека для set_wallpaper.sh и wallpaper_changer.sh

WALLPAPER_DIR="${WALLPAPER_DIR:-$HOME/Images/wallpapers}"
WALLPAPER_STATE="$HOME/.cache/current_wallpaper"
WALLPAPER_THUMBS="$HOME/.cache/wallpaper_thumbs"
WALLPAPER_THUMB_SIZE="500x500"

if command -v swww >/dev/null 2>&1; then
    WALLPAPER_BIN=swww; WALLPAPER_DAEMON=swww-daemon
elif command -v awww >/dev/null 2>&1; then
    WALLPAPER_BIN=awww; WALLPAPER_DAEMON=awww-daemon
else
    WALLPAPER_BIN=""; WALLPAPER_DAEMON=""
fi

if command -v magick >/dev/null 2>&1; then
    MAGICK=(magick)
elif command -v convert >/dev/null 2>&1; then
    MAGICK=(convert)
else
    MAGICK=()
fi

die() {
    echo "${WALLPAPER_CALLER:-wallpaper}: $*" >&2
    command -v notify-send >/dev/null 2>&1 && notify-send "Обои" "$*"
    exit 1
}

require_command() {
    local c
    for c in "$@"; do
        command -v "$c" >/dev/null 2>&1 || die "не найдена команда: $c"
    done
}

wallpaper_list_images() {
    find -L "$WALLPAPER_DIR" -type f \
        \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \
           -o -iname '*.webp' -o -iname '*.gif' -o -iname '*.bmp' \) | sort
}

# путь к миниатюре, создаётся при первом обращении
wallpaper_thumb() {
    local src="$1" hash thumb
    [[ ${#MAGICK[@]} -gt 0 ]] || return 1
    mkdir -p "$WALLPAPER_THUMBS"
    hash="$(printf '%s|%s' "$src" "$WALLPAPER_THUMB_SIZE" | md5sum | cut -d' ' -f1)"
    thumb="$WALLPAPER_THUMBS/$hash.png"
    if [[ ! -f "$thumb" || "$src" -nt "$thumb" ]]; then
        "${MAGICK[@]}" "${src}[0]" -auto-orient \
            -thumbnail "${WALLPAPER_THUMB_SIZE}^" \
            -gravity center -extent "$WALLPAPER_THUMB_SIZE" \
            "$thumb" >/dev/null 2>&1 || return 1
    fi
    printf '%s\n' "$thumb"
}

wallpaper_print_menu_entries() {
    local f name thumb
    while read -r f; do
        name="$(basename "$f")"
        if thumb="$(wallpaper_thumb "$f")"; then
            printf '%s\0icon\x1f%s\n' "$name" "$thumb"
        else
            printf '%s\n' "$name"
        fi
    done < <(wallpaper_list_images)
}

wallpaper_resolve() {
    [[ -f "$1" ]] && { printf '%s\n' "$1"; return 0; }
    [[ -f "$WALLPAPER_DIR/$1" ]] && { printf '%s\n' "$WALLPAPER_DIR/$1"; return 0; }
    return 1
}

wallpaper_setup() {
    WALLPAPER_CALLER="${1:-wallpaper}"
    [[ -d "$WALLPAPER_DIR" ]] || die "нет папки $WALLPAPER_DIR"
    [[ -n "$WALLPAPER_BIN" ]] || die "не найден ни swww, ни awww"

    if ! pgrep -x "$WALLPAPER_DAEMON" >/dev/null 2>&1; then
        setsid "$WALLPAPER_DAEMON" >/dev/null 2>&1 &
        local i
        for i in $(seq 1 40); do
            "$WALLPAPER_BIN" query >/dev/null 2>&1 && break
            sleep 0.1
        done
    fi
}

wallpaper_select_random_image() {
    WALLPAPER_IMAGE="$(wallpaper_list_images | shuf -n1)"
    [[ -n "$WALLPAPER_IMAGE" ]] || die "в $WALLPAPER_DIR нет картинок"
}

wallpaper_apply() {
    local img trans
    img="$(wallpaper_resolve "$1")" || die "не найден файл: $1"
    trans="${2:-none}"

    "$WALLPAPER_BIN" img "$img" \
        --transition-type "$trans" \
        --transition-duration 1.5 \
        --transition-fps 60 || die "$WALLPAPER_BIN не смог поставить обои"

    printf '%s\n' "$img" > "$WALLPAPER_STATE"

    if command -v wal >/dev/null 2>&1; then
        wal -i "$img" -n -q >/dev/null 2>&1 || true
        # разослать палитру во все живые терминалы
        if [[ -r "$HOME/.cache/wal/sequences" ]]; then
            for t in /dev/pts/*; do
                [[ -w "$t" ]] && cat "$HOME/.cache/wal/sequences" > "$t" 2>/dev/null || true
            done
        fi
        # пнуть alacritty, чтобы перечитал импортированную палитру
        touch "$HOME/.config/alacritty/alacritty.toml" 2>/dev/null || true
        hyprctl reload >/dev/null 2>&1 || true
    fi
}
