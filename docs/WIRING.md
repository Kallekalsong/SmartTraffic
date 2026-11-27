# Wiring

Build the same circuit for each micro:bit. Use external LEDs with one suitable current-limiting resistor in series with each LED.

| micro:bit pin | Connect through | LED connection | Function |
| --- | --- | --- | --- |
| P0 | Current-limiting resistor | LED anode (long leg) | Red |
| P1 | Current-limiting resistor | LED anode (long leg) | Yellow |
| P2 | Current-limiting resistor | LED anode (long leg) | Green |
| GND | Direct wire | Each LED cathode (short leg/flat side) | Common return |

This describes a pin-to-resistor-to-LED-to-GND arrangement. Do not connect an LED directly to a micro:bit pin. Select resistor values appropriate to the LED forward voltage and the board's electrical limits; verify the circuit and current before connecting power. A qualified instructor should check student wiring.

## Repeat for both devices

1. Connect P0, P1 and P2 to separate LED/resistor branches.
2. Connect the cathode side of all three branches to that device's GND.
3. Keep each micro:bit's LED circuit on its own board. Radio is the only inter-device link in this project.
4. Check polarity, resistor placement and short circuits before powering up.

The radio protocol does not depend on electrical connections between the two boards. Do not connect the two boards' GPIO pins together. The LED outputs are indicators for a simulation only. The micro:bit's built-in LED matrix is not used by this wiring guide.
