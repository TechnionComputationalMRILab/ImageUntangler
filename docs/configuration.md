# Configuration

[//]: # (TODO: Finish me)

A default `config.ini` will be provided if it does not exist at the script directory.

```
[folders]
data-folder = C:/
script-folder = C:/

[display]
start-maximized = on
horizontal-number-of-panels = 1
vertical-number-of-panels = 1
display-width = 1920
display-height = 1080
toolbar-style = icon-and-text
font-size = 30
window-percentile = 90
show-interactor-coords = off
text-color = 0, 34, 158
show-interactor-help = on
help-text-color = 230, 0, 0
show-interactor-debug = off
debug-text-color = 0, 0, 0
show-interactor-cursor = on
cursor-color = 255, 0, 0

[length-display-style]
color = 55, 230, 128
highlighted-color = 55, 230, 230
marker-size = 1
show-line = on
line-thickness = 10
line-style = dotted

[mpr-display-style]
color = 255, 0, 0
highlighted-color = 253, 184, 255
marker-size = 1
line-thickness = 10
line-style = line

[mpr-length-display-style]
color = 255, 255, 0
highlighted-color = 255, 255, 0
marker-size = 1
show-line = on
line-thickness = 10
line-style = line

[testing]
use-slice-location = on
draw-connecting-lines = on
ignore-uneven-slices = off
point-editing = off
show-memory-usage = on
show-fixer-button = on
show-sliders = off
```

## In detail

### folders
* `data-folder` - Where the MRI data is located. The program needs this to build the complete file paths
* `script-folder` - Location of the script. This is filled automatically during runtime

### display
* `start-maximized` - self-explanatory. Recommended to start maximized
* `horizontal-number-of-panels` - option to have multiple panels horizontally. **NOT IMPLEMENTED**
* `vertical-number-of-panels` - option to have multiple panels vertically. **NOT IMPLEMENTED**
* `display-width` = Default: 1920
* `display-height` = Default: 1080
* `toolbar-style` = Default: icon-and-text **NOT IMPLEMENTED**
* `font-size` = Size of the font in the main display interactor. Default: 30 
* `window-percentile` = Default: 90 
* `show-interactor-coords` = Show the coordinates in the main display interactor as the mouse is moved. **May cause slowdown**. Default: off 
* `text-color` = Color of the text in the main display interactor. Default: 0, 34, 158 
* `show-interactor-help` = Shows the help text. Display: on 
* `help-text-color` = Color of the help text. Default: 230, 0, 0 
* `show-interactor-debug` = Debugging purposes only. Default: off 
* `debug-text-color` = Color of debug text. Default: 0, 0, 0 
* `show-interactor-cursor` = Shows a vertical and horizontal line indicating the location of the mouse. **May cause slowdown**. Default: off 
* `cursor-color` = Color of the cursor. Default: 255, 0, 0

### length-display-style and mpr-length-display-style

* color = 55, 230, 128 
* highlighted-color = 55, 230, 230 
* marker-size = 1 
* show-line = on 
* line-thickness = 10 
* line-style = dotted

### mpr-display-style
* color = 255, 255, 0 
* highlighted-color = 255, 255, 0 
* marker-size = 1 
* line-thickness = 10 
* line-style = line

### testing
* `use-slice-location` - Uses the v3 implementation of the slice location calculation.
* draw-connecting-lines 
* ignore-uneven-slices = off 
* point-editing = off 
* show-memory-usage = on 
* show-fixer-button = on 
* show-sliders = off
