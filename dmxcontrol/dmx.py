from dmxpy import DmxPy

serialport = input("Please enter Device Serial port (eg 'COM4') >> ")     ##Ask user for COM port of DMX adapter
serialinit = DmxPy.DmxPy(serialport)
