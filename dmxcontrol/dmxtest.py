from dmxpy import DmxPy
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()                                     ## Get serial ports using pyserial
for port, desc, hwid in sorted(ports):                                         ## For port, desc, hwid in the sorted list of ports
    print("{}: {} [{}]".format(port, desc, hwid))                              ## Print using some nice formatting (table to come...)

serialport = input("Please enter desired Device Serial port (eg 'COM4') >> ")     ##Ask user for COM port of DMX adapter
serialinit = DmxPy.DmxPy(serialport)                                      ##Init DmxPy

flag = True
while flag == True:                                                                          ## Forever
    dmxchan = input('Input DMX channel to change (1-512) (enter space to quit) >> ')         ## Ask user for DMX channel to change
    if dmxchan == '':                                                                        ## If nothing entered quit
        quit()
    chanval = input('Input DMX Value to Change (0-255) >> ')                                 ## Ask user for Channel Value
    serialport.setChannel(dmxchan, chanval)                                                  ## Set to render
    serialport.render()                                                                      ## Render to serial device

