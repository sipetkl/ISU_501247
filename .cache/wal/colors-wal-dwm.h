static const char norm_fg[] = "#c5c5c4";
static const char norm_bg[] = "#181716";
static const char norm_border[] = "#71715d";

static const char sel_fg[] = "#c5c5c4";
static const char sel_bg[] = "#719571";
static const char sel_border[] = "#c5c5c4";

static const char *colors[][3]      = {
    /*               fg           bg         border                         */
    [SchemeNorm] = { norm_fg,     norm_bg,   norm_border }, // unfocused wins
    [SchemeSel]  = { sel_fg,      sel_bg,    sel_border },  // the focused win
};
