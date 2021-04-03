# Tension-inflation_GI


----------------------------------------------------

Work done by Joseph Brunet (Ecole des Mines de Saint-Etienne, CIS)
Mail: jo.brunet73@gmail.com

----------------------------------------------------

This graphical interface was developped to be used with the tension-inflation device based at Ecole des Mines de Saint-Etienne (France).

The project organisation is the following one:

```
── GUI_main.py                       #Main script to execute to start the GUI
├── Arduino_script                   #Folder with the Arduino script uploaded on the card (written in C++)
├── modules
│   ├── mainwindow_modules
│   │   ├── Left_panel.py            # Left panel of the mainwindow
│   │   └── Right_panel.py           # Right panel of the mainwindow
│   ├── sensors_dialogs
│   │   ├── Arduino.py               # Script for the dialog with the Arduino
│   │   ├── MotorPI.py               # Script for the dialog with the Motor
│   │   ├── Pump_seringe.py          # Script for the dialog with the Pump
│   │   └── PumpWM.py                # Script for the dialog with the Watson Marlow pump (not useful)
│   ├── initialisation.py            # GUI of the step 1
│   └── mainwindow.py                # GUI of the step 2 composed in right and left panels
├── ressources                       # Folder with the images
├── results                          # Folder containing the output from the software
└── Software&Drivers                 # Folder with the packages to install
```


After executing `GUI_main.py` (and if all the python packages and drivers were installed on the computer) the GUI will 

the initialisation will be launched (code in initialisation.py). 




----------------------------------------------------

Python packages required :

* pyqt                 ==>  (https://anaconda.org/anaconda/pyqt)
* pyserial             ==>  (https://anaconda.org/anaconda/pyserial)
* pyqtgraph            ==>  (https://anaconda.org/anaconda/pyqtgraph)
* simple-pid           ==>  (https://anaconda.org/esrf-bcu/simple-pid)
* PIPython             ==>  (install from the PI cd - `https://drive.google.com/file/d/1h9WOYUCOherfxR1k2YsRopm3UeD3EEEO/view?usp=sharing`, try first version 'PIPython-1.3.2.24', if it does not work try version 'PIPython-1.3.4.17')


Drivers required :

* Driver PI C663 (install from the PI cd - `https://drive.google.com/file/d/1h9WOYUCOherfxR1k2YsRopm3UeD3EEEO/view?usp=sharing`)
	* Folder linux if linux os
	* .exe if Windows os
* Driver RS485 (CP210x USB to UART Bridge VCP) - Instruction to install it below - 

----------------------------------------------------
Command to install the RS485 drivers

Window:
https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers

Ubuntu:
.../Software&Drivers/Linux_3.x.x_4.x.x_VCP_Driver_Source/
or
https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers

Puis suivez ces instructions
```
$ cd .../Software&Drivers/Linux_3.x.x_4.x.x_VCP_Driver_Source/ # change directory to the cp210x folder, adjust name if necessary
$ make #compile the source code
$ sudo cp cp210x.ko /lib/modules/"$(uname -r)"/kernel/drivers/usb/serial/ # copy the file to the system area
$ sudo modprobe usbserial # load this kernel module
$ sudo modprobe cp210x # load this kernel module
```
----------------------------------------------------
