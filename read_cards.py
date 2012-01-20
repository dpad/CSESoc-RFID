import serial
rfid = serial.Serial('/dev/ttyUSB0', 115200) # Possibly need a timeout as well
while 1:
    line = rfid.readline()
    if line.startswith("UID: "):
        print line[5:]
    # Do some processing on line
    # For example, open the database and look for the UID in the line
    # Add to a counter
    # etc.
