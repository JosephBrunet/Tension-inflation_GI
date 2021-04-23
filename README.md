# Tension-inflation graphical interface


---

Work done by Joseph Brunet (Ecole des Mines de Saint-Etienne, CIS)

Mail: jo.brunet73@gmail.com

***

This graphical interface was developped to be used with the tension-inflation device based at Ecole des Mines de Saint-Etienne (France).

## Project organisation:

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

## Software steps:


After executing `GUI_main.py` (and if all the python packages and drivers were installed on the computer), the GUI steps will be:


If you are on linux don't forget to add your user into dialout group for serial access with:
```
$ sudo usermod -a -G dialout YOUR_USERNAME
```
You can verify if the user is present in the dialout group by using the command:
```
$ groups
```

### Step 1 : Initialisation


The initialisation will be launched (code in `initialisation.py`). The objectives of this step are to connected the Arduino, the Pump, and the Motor, and to let the motor find its position. This window will appear:

![Ini step](./ressources/Ini_step.png)



* The button `Pass the initialisation` is to pass to the step 2 directly.
* The result directory is where the output of the test will be printed
* The connection show if the different devices are connected or not (green = connected). The button `Try connection` is to try to establish the connection with the devices
* The button `Start initialisation` is to let the motor find the limit sensor in order to know its displacement position.



### Step 2 : Main window


The main window will be launched (code in `mainwindow.py`). This window will appear:

![Main step](./ressources/Main_step.png)

The main window is divided into two panel: the `Left Panel` and the `Right Panel`.

The `Left Panel`: use to place control the values of the different quantities in real time and to place the sample in the initiale conditions before the beginning of the tension-inflation test.

Once the sample is place in the good conditions (in term of displacement and pressure), one can press the button `Positioning finished =>` to pass to the right panel

The `Right Panel`: use to launch the tension-inflation test.
* The `mode:Volume/Pressure` correspond to the control of the pump in pressure or in volume.
* The `mode:Displacement/Load` correspond to the control of the motor in displacement or in load.
* In `cycle Motor/Pump` you can enter the number of cycles you want before the motor or the pump stop to the final target (nothing enter = no cycles).
* In `Commands` you can enter the target displacement/pressure (nothing enter = no command). 

---

## Requirements:

### Python packages required :

* pyqt                 ==>  (https://anaconda.org/anaconda/pyqt)
* pyserial             ==>  (https://anaconda.org/anaconda/pyserial)
* pyqtgraph            ==>  (https://anaconda.org/anaconda/pyqtgraph)
* simple-pid           ==>  (https://anaconda.org/esrf-bcu/simple-pid)
* PIPython             ==>  (install from the PI cd - https://drive.google.com/file/d/1INRb_eBf8cWNtcjj4KRNG3F7fMPyqX5B/view?usp=sharing)


### Drivers required :

* Driver PI C663 (install from the PI cd - https://drive.google.com/file/d/1INRb_eBf8cWNtcjj4KRNG3F7fMPyqX5B/view?usp=sharing)
	* Folder linux if linux os
	* .exe if Windows os
* Driver RS485 (CP210x USB to UART Bridge VCP) - Instruction to install it below -

---

Command to install the RS485 drivers

Window:
https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers

Ubuntu:
.../Software&Drivers/Linux_3.x.x_4.x.x_VCP_Driver_Source/
or
https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers

Then follow these commands
```
$ cd .../Software&Drivers/Linux_3.x.x_4.x.x_VCP_Driver_Source/ # change directory to the cp210x folder, adjust name if necessary
$ make #compile the source code
$ sudo cp cp210x.ko /lib/modules/"$(uname -r)"/kernel/drivers/usb/serial/ # copy the file to the system area
$ sudo modprobe usbserial # load this kernel module
$ sudo modprobe cp210x # load this kernel module
```
