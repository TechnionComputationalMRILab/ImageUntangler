# ImageUntangler
Project to aid Gastroenterologists and biologists to analyze MRI images of the Small Bowel.
The main benefit the project hopes to add is MPR for Small Bowel MRI images
Currently under development in TCML under Professor Moti Freiman. Current Developer: Avraham Kahan, Angeleene Ang. Project Founder: Yael Zaffrani

----

## Current issues:

### Somewhat major

* Crashes without warning if no points are selected when Calculate MPR is clicked
  
error raised:

    Traceback (most recent call last):
      File "/mnt/ssd/TCML/ImageUntangler/src/Interfaces/SequenceViewerInterface.py", line 115, in calculateMPR
        MPRproperties = PointsToPlaneVectors(self.view.MPRpoints.getCoordinatesArray(), self.view.imageData, Plot=0, height=40, viewAngle=180)
      File "/mnt/ssd/TCML/ImageUntangler/src/Model/getMPR.py", line 28, in __init__
        allPoints = self.Org_points[:, 0:3] # should be replaceable by [:, :]
    IndexError: too many indices for array: array is 1-dimensional, but 2 were indexed
    
    Process finished with exit code 134 (interrupted by signal 6: SIGABRT)

* Adding MPR points randomly sometimes raises "TypeError: m > k must hold"
* Calculate Length in the main window doesn't seem to do anything?
* If there's one tab, closing the tab causes the program to crash. Ideally, it should pop you back to the "Add images" screen

the error raised is 
  
      QXcbConnection: XCB error: 3 (BadWindow), sequence: 670, resource id: 18921706, major code: 40 (TranslateCoords), minor code: 0

* For DICOM images: the images work, but slice index does not.

* MPR window: changing the height/angle and clicking save file makes the program crash

        Traceback (most recent call last):
          File "/mnt/ssd/TCML/ImageUntangler/src/MPRwindow/MPRWindow.py", line 192, in <lambda>
            self.updateButton.clicked.connect(lambda: self.HeightChanged())
          File "/mnt/ssd/TCML/ImageUntangler/src/MPRwindow/MPRWindow.py", line 143, in HeightChanged
            self.GetMPR = getMPR.PointsToPlaneVectors(self.MPRViewerProperties.ConvViewerProperties, self.MPRViewerProperties.originalPoints, self.MPRViewerProperties.ConvViewMode, height=self.MPRViewerProperties.MPRHeight,
        AttributeError: 'viewerLogic' object has no attribute 'ConvViewerProperties'

### Minor

* You can't close a tab you're currently on
* MPR window has no title and icon
* There should be a way to turn off "add ____ points" and return to the level/window scrolling

  (this seems to work in Windows but not in Ubuntu)

* Confirmation when closing a tab would probably be useful?
* Having similar window/level sliders on the MPR window for the sake of similarity might be nice