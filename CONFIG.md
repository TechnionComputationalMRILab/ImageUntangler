# Configuration

## Folders
**Need to use absolute paths, no need to escape backslashes**

    [folders]
    default-folder = C:/Users/ang.a/OneDrive - Technion/Documents/MRI_Data/Filename_test
    default-save-to-folder = C:/Users/ang.a/OneDrive - Technion


## Display
    [display]
    start-maximized = off
    horizontal-number-of-panels = 2
    vertical-number-of-panels = 1
    display-width = 1920
    display-height = 1080

## Length display style
    [length-display-style]
    color = yellow
    size = 5
    marker = circle
    line-thickness = 5
    line-style = dotted
    measurement-style = none

`line-style` options: `dashed`, `dotted`, `solid`, `none`

`measurement-style` options:
* `none` displays nothing
* `overlay` displays the length as an overlay on the panel
* `mbox` shows the length as a message box
* `panel` shows the length as a panel on the same window

## MPR display style
    [mpr-display-style]
    color = white
    size = 5
    marker = circle
    line-thickness = 5
    line-style = line


## Testing    
    [testing]
    all-testing-features = on
    points-loading = on
    draw-connecting-lines = on
    reader-reimplementation = on
