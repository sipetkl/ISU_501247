const char *colorname[] = {

  /* 8 normal colors */
  [0] = "#181716", /* black   */
  [1] = "#719571", /* red     */
  [2] = "#A39565", /* green   */
  [3] = "#D4A85E", /* yellow  */
  [4] = "#DFBE63", /* blue    */
  [5] = "#2D6E8F", /* magenta */
  [6] = "#8A7182", /* cyan    */
  [7] = "#c5c5c4", /* white   */

  /* 8 bright colors */
  [8]  = "#71715d",  /* black   */
  [9]  = "#719571",  /* red     */
  [10] = "#A39565", /* green   */
  [11] = "#D4A85E", /* yellow  */
  [12] = "#DFBE63", /* blue    */
  [13] = "#2D6E8F", /* magenta */
  [14] = "#8A7182", /* cyan    */
  [15] = "#c5c5c4", /* white   */

  /* special colors */
  [256] = "#181716", /* background */
  [257] = "#c5c5c4", /* foreground */
  [258] = "#c5c5c4",     /* cursor */
};

/* Default colors (colorname index)
 * foreground, background, cursor */
 unsigned int defaultbg = 0;
 unsigned int defaultfg = 257;
 unsigned int defaultcs = 258;
 unsigned int defaultrcs= 258;
