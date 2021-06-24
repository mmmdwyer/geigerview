# GeigerView

## Hardware
The core hardware is the MightyOhm Geiger Counter kit. Its home is at
https://mightyohm.com/blog/products/geiger-counter/ but it may be purchased
at other locations, like Amazon https://www.amazon.com/dp/B08L8FM1H6/ or 
Sparkfun.
The interface is plain old 3v3 TTL Serial. But I recommend the DSD TECH
SH-U09C. http://www.dsdtech-global.com but most easily found at Amazon: 
https://www.amazon.com/gp/product/B07BBPX8B8/
What you want is a device that can do 3v3 serial with a reliable converter
(The DSD one uses a genuine FTDI), and also outputs a +3v3 line. The TX/RX
leds help immensely. The DSD also includes the needed Dupont wires.
Note that some serial converters output 3v3 logic, but the power pin is 
still 5v. The MightyOhm device might handle 5v okay, but I am not sure.

## Putting it together
Assemble the geiger counter as described in its kit. Once you have built
and tested it, you're ready to add the serial. 

Remove the batteries. Or, at least turn the switch OFF. If you don't, you
might back-charge the batteries and they might explode.

You will need just four wires -- and maybe just three.  Note the VCC, GND,
TXD, and RXD pins on the serial converter. On the geiger counter you will 
see a 6-pin inline header called SERIAL and a 3-pin header called PULSE.
You will use these two. You'll connect the two with dupont wils like this:

```
| Serial | Geiger            |
| VCC    | PULSE Pin 1       |
| GND    | PULSE Pin 3       |
| TXD    | SERIAL Pin 5 (RX) |
| RXD    | SERIAL Pin 4 (TX) |
``` 
 
Be very carefully with your wires, and don't trust the colors; mine ended
up making the red wire GND.

When you plug the serial port into power, the geiger counter should turn on,
regardless of the power switch.  You should see the RXD LED on the serial
converter flash once a second.

You can start a terminal program and connect at 9600-N-8-1 and you should
see reports once per second that look like this:

```
CPS, 0, CPM, 13, uSv/hr, 0.07, SLOW
```

## Collecting Data

Using pyserial (python3-serial) and rrdtool (python3-rrdtool & rrdtool), I
wrote a quick script call 'radlog' that just sits in a loop and listens to
the one-a-second reports and stuffs them into a database.

The first trick is the RRD database. It's pretty arcane, but what I asked
it to do was to record a 2-year loop of results in 5-min, 30-min, 2-hr, and
one day increments. I am only really using the CPM number. If a database
isn't found, it will create it.

Next is the serial connection.  I use the /dev/serial/by-id/ path in Linux,
because it makes it MUCH easier to reliably find a USB serial device, even if 
it is unplugged and plugged back in somewhere else.

Now, I just wait on a readline(), split apart the line, and send the data 
to rrd tool.

## Making Pictures
Right now, I'm just using a shell script to make static PNGs. You specify 
how far back in history you want to read, and which data to use and it 
will dump out little graphs.


```
rrdtool graph radsday.png --start -86400\
            DEF:cpm=rads.rrd:cpm:MAX \
            LINE1:cpm#FF00FF:"Clicks/Min"
```

Build a graph called radsday.png, start at now-1day, (end at now). Use
the CPM max data from rads.rrd as 'cpm', finally graph that using a line
of width 1 in magenta and label it "Clicks/Min".

## The Future
- Might want to modify the code on the geiger counter to default the speaker to OFF.
- The logger isn't hardened against ANYTHING, and dies too easily
- The pictures could be generated live from a webpage pretty easily.
- The logger could also be emitting MQTT or alerting.
- Maybe Graphite would be better to work with?
