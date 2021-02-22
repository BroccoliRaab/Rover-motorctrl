# import curses and GPIO
import time
import serial
import numpy

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys

#Initialize
ser = serial.Serial("/dev/ttyACM0", 9600)
dur = 0
while dur != -1:   
    fl = int(input("\nEnter Front Left Wheel's speed range [-255, 255]: "))
    fr= int(input("\nEnter Front Right Wheel's speed range [-255, 255]: "))
    rl = int(input("\nEnter Rear Left Wheel's speed range [-255, 255]: "))
    rr= int(input("\nEnter Rear Right Wheel's speed range [-255, 255]: "))
    dur = float(input ("\nEnter Duration: "))

    fl_forward = 0
    rl_forward = 0
    fr_forward = 0
    rr_forward = 0

    if fl >= 0 :
        fl_forward = 0b0001
    if fr >= 0 :
        fr_forward = 0b0010
    if rl >= 0 :
        rl_forward = 0b0100
    if rr >= 0 :
        rr_forward = 0b1000

    
    packetlist = [numpy.uint8(fl_forward+fr_forward+rl_forward+rr_forward), 
                  numpy.uint8(abs(fl)),
                  numpy.uint8(abs(fr)),
                  numpy.uint8(abs(rl)),
                  numpy.uint8(abs(rr)) ]

    print(packetlist)
    ser.write(bytearray(packetlist))
    time.sleep(dur)
    stoppacket = [numpy.uint8(0b00001111), numpy.uint8(0), numpy.uint8(0), numpy.uint8(0), numpy.uint8(0)]
    print(stoppacket)
    ser.write(bytearray(stoppacket))    



