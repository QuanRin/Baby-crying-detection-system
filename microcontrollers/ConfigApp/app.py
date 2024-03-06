import serial
import serial.tools.list_ports as list_ports
import time

def scan():
    ports = list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print("Checking {}: {} [{}]".format(port, desc, hwid))
        try:
            with serial.Serial(port, 115200, timeout=1) as ser:
                ser.write(b'DEVICE')
                lines = ser.read_all()
                print(lines)
        except:
            pass

with serial.Serial('COM4', 115200, timeout=2) as ser:
    line = ser.readall()
    print(line)

