# import curses and GPIO
import time
import serial
import numpy

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys

#Initialize
ser = serial.Serial("/dev/ttyACM0", 9600)
dur = 0

stoppacket = [numpy.uint8(0b00001111), numpy.uint8(0), numpy.uint8(0), numpy.uint8(0), numpy.uint8(0)]

#ser.write(bytearray(stoppacket))    

while dur != -1:


    speed = int(input ( "\nEnter Motor Speed (Int 0-255)" ))
    dur = float(input ("\nEnter Duration(floating point seconds): "))
    direction = int(input("\n Enter Direction in numpad notation (5=rotate clockwise, 0=rotate counterclockwise)"))

    assert(speed > 255 or speed <0, "Speed out of range (int 0-255)")
    assert(direction > 9 or speed <0, "Direction out of range (int 0-9)")

    intPacket =[]

    if direction == 1:
        intPacket= [0, speed, 0, 0, speed] 
    elif direction == 2:
        intPacket= [0] + [speed]*4
    elif direction == 3:
        intPacket= [0, 0, speed, speed, 0] 
    elif direction == 4:
        intPacket= [0b0110] + [speed]*4 
    elif direction == 5:
        intPacket= [0b1010] + [speed]*4 
    elif direction == 6:
        intPacket= [0b1001] + [speed]*4 
    elif direction == 7:
        intPacket= [0b1111, 0, speed, speed, 0] 
    elif direction == 8:
        intPacket= [0b1111] + [speed]*4
    elif direction == 9:
        intPacket= [0b1111, speed, 0, 0, speed] 
    elif direction == 0:
        intPacket= [0b0101] + [speed]*4 

    speed = numpy.uint8(speed)

    packetlist = list(map(numpy.uint8, intPacket)) 

    print(packetlist)
    ser.write(bytearray(packetlist))
    time.sleep(dur)
    ser.write(bytearray(stoppacket))


