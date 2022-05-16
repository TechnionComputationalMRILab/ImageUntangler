# Maintenance Notes

## Adding functions to toolbar

* Add button to `gui.display.toolbar.py` with a `clicked.connect(lambda: function(model))`
* Create function in `gui.display.toolbar_connect.py` that refers to the desired functionality in `app.gui_data_handling.case_model.py`
* If the function also needs to interact with the centerline, check if `self.centerline_model` exists in `case_model.py` and add the function in `app.gui_data_handling.centerline_model.py`
