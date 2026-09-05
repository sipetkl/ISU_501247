const char *colorname[] = {

  /* 8 normal colors */
  [0] = "#140808", /* black   */
  [1] = "#B3BA3B", /* red     */
  [2] = "#EBA729", /* green   */
  [3] = "#FAE70E", /* yellow  */
  [4] = "#F3CC20", /* blue    */
  [5] = "#EC9B69", /* magenta */
  [6] = "#D272CA", /* cyan    */
  [7] = "#c4c1c1", /* white   */

  /* 8 bright colors */
  [8]  = "#6b5858",  /* black   */
  [9]  = "#B3BA3B",  /* red     */
  [10] = "#EBA729", /* green   */
  [11] = "#FAE70E", /* yellow  */
  [12] = "#F3CC20", /* blue    */
  [13] = "#EC9B69", /* magenta */
  [14] = "#D272CA", /* cyan    */
  [15] = "#c4c1c1", /* white   */

  /* special colors */
  [256] = "#140808", /* background */
  [257] = "#c4c1c1", /* foreground */
  [258] = "#c4c1c1",     /* cursor */
};

/* Default colors (colorname index)
 * foreground, background, cursor */
 unsigned int defaultbg = 0;
 unsigned int defaultfg = 257;
 unsigned int defaultcs = 258;
 unsigned int defaultrcs= 258;
