Designed for use with RFIDv3 by Aaron Carroll, Dan Padilha, and Stephen Sherratt.
Contact Dan Padilha on <ddp@cse.unsw.edu.au> for more information.

How it works
------------

You plug in the board with a USB->microUSB cable. As soon as it's plugged in it's working,
so it'll be writing card IDs over the serial port. It writes to */dev/ttyUSB0* (or USBx, where x
is normally 0 if you have no other serial USB devices running, which you shouldn't). You can
watch the output live by using either minicom or picocom, as:
*sudo picocom -b 115200 /dev/ttyUSB0*
The 115200 is the baud rate for the device, which is basically how quickly it talks over the
serial port, it's practically equivalent to "frequency" for bits over a line. This value can be
changed but is hardcoded into the board, so if you want to change it you'll need to reflash
the board.

What we need is some sort of database of CSE ID -> card UID, plus whatever other fields
we may want (such as course studying, whether they're a full member, etc.) We can probably
just add this to the csesoc-website database, that way we can access the user database in
the django-admin if we decide to write that in, as well as the possibility of a web interface
for adding new cards (rather than a Python script which is what we'll probably have to begin
with). We'll probably also need some sort of events table so we can record attendance per
event, or we can just have a counter show up on the screen, anything works.

Reader Output
-------------

Each line is either a "---" or "UID: abcdefabcd" (that is, the UID which is a 5-byte hex number).
The "---" signifies one "round" of reading cards. This is because if there are two cards next to
the reader, it'll essentially print out:

    ---
    UID: card1
    UID: card2
    ---
    UID: card2
    UID: card1
    ---

etc.

Also, I made the LEDs on the board flash on a good card read and on a bad checksum. It flashes 
red for card read and yellow on bad checksum. Yes, counter-intuitive, but the red LED is brighter 
and my favourite colour, so leave me alone. We can modify this if required, as well as add things
like speakers to beep on a card (just need to buy some sort of internally driven buzzer and solder
it on) but this requires flashing the reader.

Flashing the Reader
-------------------
The RFIDv3 board is comprised of two main components: the MSP430F249 and the TRF7960.

The MSP430 is the microcontroller and is what is programmed and flashed. rfidv3_msp.tar.gz is 
the version of the code running on the RFID board itself, and also includes the entire
revision history of the board's development.

The TRF7960 controls the RFID aspect, namely the antenna. You can communicate with it using
the MSP, but since all the code is already there and works, you shouldn't need to change it.

Talking to the board is done through microUSB, through an FT232 chip. Data is sent and received
using the set-up UART lines, which if I remember correctly we're using Port 3's ones.

Flashing the MSP, on the other hand, is a much more difficult process. You'll need access to
a compatible JTAG adapter, as well as a connector which can fit the header on the board
(alternatively, solder your own!). There is a 6-pin JTAG header on the board (actually 8-pin, 
but the 3V3 pin should be removed, and there is also a pin floating). Finally, you also need
mspgcc-3.2.3.

Also note: there are two jumpers on the board, which, when in use with the USB (which should
be the only application at this point), should be set to "USB" and "3V3".
