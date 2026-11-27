# SmartTraffic
A distributed traffic-light simulation built with two BBC micro:bits, LED indicators, wireless radio communication and a timed state machine using MakeCode Python
# SmartTraffic

### A distributed micro:bit traffic-light simulation

SmartTraffic is an experimental distributed traffic-light simulation built using two BBC micro:bit devices, external LED indicators and wireless radio communication.

The project explores distributed state machines, embedded programming, communication protocols, timing systems, event-driven programming and fault-handling concepts using the MakeCode Python environment.

---

## Overview

SmartTraffic consists of two communicating micro:bit units representing two traffic signal directions in a simplified intersection simulation.

The devices communicate wirelessly using the micro:bit radio system. A coordination unit manages the simulated traffic phases while the second unit follows the transmitted phase information.

Both devices have local controls for starting, stopping and switching off the LED simulation.

### Project goals

- Build a distributed embedded system using micro:bit.
- Implement a traffic-light state machine.
- Explore wireless communication between micro:bit devices.
- Use event-driven programming.
- Implement timed state transitions.
- Investigate synchronization and communication failures.
- Create a modular and documented MakeCode Python project.
- Learn about embedded systems architecture.

---

## Hardware

### Required components

| Component | Quantity |
|---|---:|
| BBC micro:bit | 2 |
| Red LED | 2 |
| Yellow LED | 2 |
| Green LED | 2 |
| Suitable LED resistors | 6 |
| Connecting wires | As required |

The LEDs should be connected using suitable current-limiting resistors.

### Pin configuration

| Pin | Function |
|---|---|
| P0 | Red LED |
| P1 | Yellow LED |
| P2 | Green LED |
| GND | Common ground |

Each micro:bit uses the same pin configuration.

---

## Architecture

SmartTraffic uses a two-device architecture.

### Micro:bit 1

Micro:bit 1 is responsible for coordinating the simulated traffic phases.

Responsibilities:

- Manage the traffic phase state machine.
- Control its local LEDs.
- Broadcast phase changes.
- Process local control inputs.
- Receive remote commands.
- Maintain phase timing.

### Micro:bit 2

Micro:bit 2 follows the transmitted phase information.

Responsibilities:

- Receive radio messages.
- Interpret phase commands.
- Update local LEDs.
- Send start and stop requests.
- Monitor incoming communication.

The devices share a common radio group.

---

## Communication

### Radio configuration

- Radio group: 138
- Communication method: Radio string messages
- Platform: BBC micro:bit
- Environment: Microsoft MakeCode Python

### Protocol messages

| Message | Purpose |
|---|---|
| CMD_START | Request a system start |
| CMD_STOP | Request a system stop |
| CMD_OFF | Request LED shutdown |
| PHASE_G1 | Direction 1 simulated green phase |
| PHASE_Y1 | Direction 1 simulated yellow phase |
| PHASE_G2 | Direction 2 simulated green phase |
| PHASE_Y2 | Direction 2 simulated yellow phase |
| PHASE_ALLRED | Simulated all-red phase |
| PHASE_STOP | Stop signal |

This protocol is a prototype and does not implement a fully reliable delivery or acknowledgement system.

---

## Traffic phases

The simulation uses the following conceptual sequence:

1. Direction 1 green.
2. Direction 1 yellow.
3. All-red simulation.
4. Direction 2 green.
5. Direction 2 yellow.
6. All-red simulation.
7. Repeat.

The sequence is controlled using a timed state machine.

---

## Controls

| Input | Action |
|---|---|
| Button A | Request start |
| Button B | Request stop |
| Buttons A+B | Switch off LEDs |

Controls can be activated on either micro:bit.

---

## Software

The project uses:

- Microsoft MakeCode
- MakeCode Python
- BBC micro:bit radio
- Digital pin control
- Event handlers
- Timer-based state transitions

---

## Installation

1. Open Microsoft MakeCode for micro:bit.
2. Create a new project.
3. Open the Python editor.
4. Copy the Micro:bit 1 source code.
5. Flash it to the first micro:bit.
6. Create a second project.
7. Copy the Micro:bit 2 source code.
8. Flash it to the second micro:bit.
9. Connect the LED circuits using the documented pin configuration.
10. Test the simulation in a controlled environment.

---

## Limitations

This project is an educational prototype.

It does not include:

- Certified traffic signal hardware.
- Guaranteed radio delivery.
- Verified fail-safe control.
- Redundant communication.
- Formal safety verification.
- Real-world traffic control functionality.

The simulation is not designed or approved for controlling real traffic, roads, vehicles or pedestrians.

---

## Future development

Potential improvements:

- Message acknowledgements.
- Sequence numbers.
- Heartbeat protocol.
- State recovery.
- Radio diagnostics.
- Fault simulation.
- Event logging.
- Configurable phase durations.
- Better synchronization.
- Modular protocol design.
- Automated testing.
- More traffic signal units.
- Central monitoring interface.

---

## Project status

Experimental prototype.

Version: 1.0.0

Platform: BBC micro:bit

Language: MakeCode Python

---

## License

This project is intended for educational experimentation and learning.

See LICENSE for license information.
