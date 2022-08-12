import serial
import time
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1.0)


def value():
    x = 10
    for i in range(x):
        rcv = port.readline()

        if len(rcv) > 4:
            a = True
            break
    else:
        x = x + 1
    while a:
        value = rcv.split(',')
        # print value

        ph = value[0]
        w = value[1]
        l = value[2]
        t = value[3]
        __, ph = ph.split(':')
        __, w = w.split(':')
        __, l = l.split(':')
        __, t = t.split(':')
        ph = float(ph)
        w = float(w)
        l = float(l)
        t = float(t)
        a = False
        return ph, w, l, t
while True:
    print(value())
    time.sleep(2)