# Simulated Industrial Control System Hacking Scenario
## A Cyber-Physical Emulation System for Scenario-Based Training

Developed by: $GROUPNAME

![alt text](https://github.com/Jordan-z5214614/IT-Project-GROUPNAME/blob/master/Images%20of%20the%20Parts%20for%20the%20Project/Logo_Design.png)

# Introduction
This repo will hold the University project 'Off The Grid', A Cyber-Physical Emulation System for Scenario-Based Training. 
The system will provide a means to run scenarios that emulate Cyber-Physical Systems to be accessed for a small group of students to interact with as attackers. 

### Aim:

The project aims to allow for a modular framework to enable future ICS simulated hacking scenarios to be built. We have developed a functioning simulated scenario for controlling a powerplant turbine in an industrial control system. We have also created a scenario, using this framework, which emulates a turbine from a nuclear power plant. These scenarios aim to educate and facilitate honing Cyber-Security skills in an Industrial Control System (ICS) context. 

Features supported by this system:
- Hacking a simulated powerplant turbine
- Defining your own scenario
- Creating added systems

### History:

This project expands upon a prototype platform for teaching the hacking of cyber-physical systems (such as power grid devices, traffic lights, and critical infrastructure). The current ICS hacking range in use by UNSW has a running cost too high to facilitate its regular use as a teaching resource, however, it uses the real software and hardware of industrial ICS. UNSW is seeking a more cost-effective solution which does not use the real software or hardware. A previous attempt to create a similar scenario was the construction of a wind power turbine, controlled by ICS. This previous project will be built on. 

[For a full guide see the past projects WIKI](https://github.com/Mikaela199/IT-Project-2/wiki)




# System Components:

- GUI:
The GUI will provide as another attack path for the system. The GUI will give access to be able to change variables of the turbine.
- Database Logger:
A SQL server will be configured in a vulnerable manner to provide an attack path for the system. This sends alerts to the system of unusual behaviour.
- Supervisory Computer:
The supervisory computer is the largest control center of the system and includes the GUI componenet and the Database Logger component.
- Sensors:
Virtual sensors will be configured to add another attack vector for the system.
- PLC's:
The PLC's are set up to control and communicate to the motor and turbine. 
- Modbus emulator:
Pymodbus will be utilised as the main platform for building the ICS components. This will all be run from a set of Raspberry Pi's in a client server relationship.
- Hardware:
A detailed physical system that takes inputs from the emulated system to provide visual and kinetic effects in a scale model of a power plants turbine. Utilising the GPIO pins on the Raspberry Pi to communicate with DC motors using the Adafruit motor control hat. 


</br>


# QuickStart


 ### Physical Requirements:
 - Raspberry Pi 4 x3
 - Raspberry Pi's HDMI connector x3
 - Raspberry Pi's power supply x3
 - SD cards containing micro SD card x3
 - mouse 
 - keyboard
 - Laptop or PC with SD card port
 - Raspberry Pi HATs x2</br>
(We used the Adafruit motor control HATs from the "Adafruit DC & Stepper Motor HAT for Raspberry Pi - Mini Kit". This can be brought from the following link: https://www.adafruit.com/product/2348)

![alt text](https://github.com/Jordan-z5214614/IT-Project-GROUPNAME/blob/master/Images%20of%20the%20Parts%20for%20the%20Project/Raspberry-Pi-Hat.JPG)

![alt text](https://github.com/Jordan-z5214614/IT-Project-GROUPNAME/blob/master/Images%20of%20the%20Parts%20for%20the%20Project/Raspberry-Pi-Hat-in-Use.JPG)

 - lego motor x2 </br>
(We used the motor from the LEGO® Power Functions medium motor and 2 19.6” (50cm) extension wires, officially titled as the "LEGO® Power Functions M-Motor". This can be brought from the following link: https://www.lego.com/en-us/product/lego-power-functions-m-motor-8883)

![alt text](https://github.com/Jordan-z5214614/IT-Project-GROUPNAME/blob/master/Images%20of%20the%20Parts%20for%20the%20Project/Lego-Motor.JPG)

![alt text](https://github.com/Jordan-z5214614/IT-Project-GROUPNAME/blob/master/Images%20of%20the%20Parts%20for%20the%20Project/Lego-Motor-in-Use.JPG)

 - turbine pieces x2
 - Hall Effect Sensor x 1
 - Modified LEGO gearing and connector magnets
 - appropriate connectors and pieces (see diagram below for full picture) 
 
 ![alt text](https://github.com/Jordan-z5214614/IT-Project-GROUPNAME/blob/master/Images%20of%20the%20Parts%20for%20the%20Project/Lego_Setup_Full_1.JPG)
 ![alt text](https://github.com/Jordan-z5214614/IT-Project-GROUPNAME/blob/master/Images%20of%20the%20Parts%20for%20the%20Project/Lego_Setup_Full_2.JPG)
 ![alt text](https://github.com/Jordan-z5214614/IT-Project-GROUPNAME/blob/master/Images%20of%20the%20Parts%20for%20the%20Project/Lego_Setup_Full_3.JPG)
 
 
 - Lego power plant station (optional please view the Lego Design folder for more details)
 - Router/Switch (support equipment)
 - LEGO battery Pack (support equipment)
 
If you wish to add to the design e.g. add extra machines or turbines, then extra physical requirments may be needed. Please view the 'Create Your Own' section of the "README.md" file for more information about extending this project. 
 </br></br>


### Set Up Manually:

#### Hardware

Use the "HOW TO SET UP RASPBERRY PI'S" document for the initial set up your Raspberry Pi's or follow the tutorial on https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/4

We reccomend setting up the Pi using SSH. In order to enable SSH on the Pi you will have to ad a blank file called "ssh" into the root directory of each Pi. 

Each Pi unit can be configured as a different SCADA device during the later setup. At this stage set the hostname as something meaningful for each device. 

#### Software

After the Pi has been set up and the hostname has been set, clone this github into the home directory. Note that you may have to install git onto each Pi. 
 
After the setup has been completed install the requirements listed in the "requirements.txt" from the master or the link:
https://github.com/Jordan-z5214614/IT-Project-GROUPNAME/blob/master/requirements.txt

After all the Raspberry Pi's have the requirements installed, the Raspberry Pi's can be set up. 

There are two main device types that can be set up:

1) The higher level Supervisor device
2) The low level Programmable Logic Controller(s) (PLC)

In the current iteration, the Server service for the Modbus is hosted on the supevisor device. If your setup will not use a supevisor you will need to run an instance of the ModbusServer class somewhere on the local network. 

##### Setting up PLCs

The PLC setup is primarily done using the config file within the PLC folder. Within this config file you will configure what kind of devices are connected and controlled by the PLC. The parameters are:

1) address:             The address that this device will use on Modbus. This can be any 3 digit hexadecimal number

2) device drivers:      The driver files that the PLC will load. By default we have included drivers for a motor and a speed sensor, but                         users can add their own drivers for custom devices they would like to add. Each driver file is mapped to a                               device name, i.e. dev0 = motorDriver tells the system that dev0 is a device that uses the motorDriver class. 

3) parameter addresses: The register addresses and names for each parameter, e.g. RPM, volts, etc that the PLC should listen/broadcast

4) server:              The hostname and port that the modbus server service is running on. In the standard setup this is the supervisor                         Pi. 

Aside from the config file, the only remaining configuration is to load the logic script. By default, the PLC will run the main method in the PLCLogic.py file. Users can either include their own method or class file and update PLCDriver.py accordingly, or write thier own logic in the PLCLogic.py main method. 

The PLCLogic.main method is passed 4 arguments:

1) device_list:        A dictionary of driver objects. The key is the device name (as per the config file) and the value is the driver                          object. The driver object can be referenced by use of device_list.get('\[device name]'). This can be used to                            access methods directly, or, as reccomended the driver object can be mapped to a variable name within PLCLogic                          for readability, i.e, motor0 = device_list.get('\[device name]'). the setRpm method for motor0 is simply                                motor0.setRpm() 

2) param_list:         A dictionary of parameter names and addresses. The key is the parameter name, and the value is the address in                            Modbus. Similar to device_list, i.e. param_list.get('rpm') will return the address (int) of the RPM parameter as                        per the config file. Can also be mapped to a variable name in the PLCLogic class. 
                   
3) writeModbus:        A method for writing to the modbus. It's arguments are writeModbus(target_register, value). It will only ever                            write to the PLC that the logic is being run on. 

4) readModbus:         Similar to writeModbus, but it returns the value of the register passed to it. Can only access registers on the                          PLC it is being run on. 
                    
This should equip the user with all the tools required to write logic programs to simulate a wide variety of ICS devices. 

##### Setting up the supervisor

Similar to the PLCs, the main supervisor setup is done using the config file in the supervisor folder. It contains the addresses and credentials for the PLCs that are being used in the scenario. \[PLC List] contains the hostnames, or the IPs of the PLCs connected. The user can name the PLCs whatever they like. The next entrys are \[PLC Name] which includes the username and password for the SSH connection used to boot the ICS program. 

##### Setting up the GUI

There is a basic GUI included that will load a basic motor control interface for the number of motors connected to the system. This GUI can be modified, or, a new GUI or CLI program can be written by the user. There are two main implementations for an interface:

1) An independent program that has it's own Modbus interface
2) A program that runs on the supervisor that directly interfaces with the SupervisorDriver class

For an independant program, there are included classes that include the relevant methods to get the configurations from the supervisor via SSH.

In the case of a program that interfaces with the supervisor, it can be called from the main method and passed the configurations/modbus methods in the same way as the PLCs. 

Finally, the GUI should call the SupervisorDriver.py main method to launch the program. This will in turn connect to each PLC and pull the config, as well as start the PLCDriver.main method. 

1) Install all the files in the Supervisory Computer onto 1 Raspberry Pi. Then run the Driver file.
2) On the the last two Rasperry Pi's install all the files in the PLC files on each Raspberry Pi. Then run the Drvier file.

## Testing and Red Team Examples:
If you wish to try out some testing of the system or Red Team demonstrations on the attack vectors, please view the 'Red Team Demonstrations and Tutorials' file or click the following link: </br>
https://github.com/Jordan-z5214614/IT-Project-GROUPNAME/tree/master/prototype1/Red%20Team%20Demonstrations%20%26%20Tutorials




 
