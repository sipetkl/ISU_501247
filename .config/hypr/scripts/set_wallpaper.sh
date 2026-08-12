#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

source "${SCRIPT_DIR}/wallpaper_common.sh"

wallpaper_setup "set_wallpaper.sh"
wallpaper_select_random_image
wallpaper_apply "$WALLPAPER_IMAGE" "none"
