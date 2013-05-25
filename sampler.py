import serial
import time
from datetime import datetime
import sqlite3


def initdb():
    #open the dbo
    conn = sqlite3.connect('temperatures.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    #create the table
    c.execute('''CREATE TABLE temperatures
                    (ts timestamp, scale text, temperature real)''')
    conn.commit()
    conn.close()


def sample(samples):
    #get the data
    temp = 0
    for ii in range(samples):
        ser.write("f")
        temp_sample, scale = ser.readline().strip().split(" ")
        temp += float(temp_sample)
    temp = temp / samples
    #write it to the database
    conn = sqlite3.connect('temperatures.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute("INSERT INTO temperatures VALUES (?,?,?)",
              (datetime.now(), scale, temp))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    #open the com port
    ser = serial.Serial("COM4", 9600, timeout=1)
    time.sleep(2)
    try:
        initdb()
    except:
        pass
    while 1:
        sample(10)
        time.sleep(1)
