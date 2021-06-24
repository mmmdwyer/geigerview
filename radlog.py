#!/usr/bin/python3

import serial
import rrdtool
import os.path

def createrrd():
    # 600 samples of 5 minutes  (2 days and 2 hours)
    # 700 samples of 30 minutes (2 days and 2 hours, plus 12.5 days)
    # 775 samples of 2 hours    (above + 50 days)
    # 797 samples of 1 day      (above + 732 days, rounded up to 797)
    if os.path.exists("rads.rrd"):
        print("Using existing RRD...")
    else:
        rrdtool.create("rads.rrd",
                "--start", "now",
                "--step", "300",
                "DS:cps:GAUGE:600:U:U",
                "DS:cpm:GAUGE:600:U:U",
                "RRA:AVERAGE:0.5:1:600",
                "RRA:AVERAGE:0.5:6:700",
                "RRA:AVERAGE:0.5:24:775",
                "RRA:AVERAGE:0.5:288:797",
                "RRA:MAX:0.5:1:600",
                "RRA:MAX:0.5:6:700",
                "RRA:MAX:0.5:24:775",
                "RRA:MAX:0.5:288:797")

ser = serial.Serial('/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AB0KPLG7-if00-port0',baudrate=9600, bytesize=8,parity='N',stopbits=1, timeout=3, xonxoff=0, rtscts=0)

print(ser.baudrate)
print(ser.name)

createrrd()

while (1):
    # b'CPS, 0, CPM, 13, uSv/hr, 0.07, SLOW\r\n'
    line = ser.readline()
    string = line.decode()
    chunks = string.split(',')
    if (len(chunks) == 7):
        cps = chunks[1]
        cpm = chunks[3]
        print("Logging N:"+cps+":"+cpm)
        rrdtool.update("rads.rrd","N:"+cps+":"+cpm)
    else:
        print("Bad read:", line)

