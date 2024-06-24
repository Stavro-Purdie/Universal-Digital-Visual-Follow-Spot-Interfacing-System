from dmxpy import DmxPy
import dmx
serialport = input("Please enter Device Serial port (eg 'COM4') >> ")     ##Ask user for COM port of DMX adapter
serialinit = DmxPy.DmxPy(serialport)                                      ##Init DmxPy

flag = True
while flag == True:                                                                          ## Forever
    dmxchan = input('Input DMX channel to change (1-512) (enter space to quit) >> ')         ## Ask user for DMX channel to change
    if dmxchan == '':                                                                        ## If nothing entered quit
        quit()
    chanval = input('Input DMX Value to Change (0-255) >> ')                                 ## Ask user for Channel Value
    serialport.setChannel(dmxchan, chanval)                                                  ## Set to render
    serialport.render()                                                                      ## Render to serial device
