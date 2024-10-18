@start
run pyuic5  -x UiFiles\\interface.ui -o src\\Ui_interface.py
run pyrcc5 resources\\resources.qrc -o resources_rc.py
run python -B dashboard_desktop.py