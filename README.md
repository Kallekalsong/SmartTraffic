# SmartTraffic

**An educational, two-device traffic-light simulation for BBC micro:bit and Microsoft MakeCode Python.**

SmartTraffic uses two micro:bits, three external LEDs per device and the built-in radio to explore embedded programming, state machines, distributed systems and unreliable communication. One device coordinates timing; the other follows its phase messages. Either device can request start, stop or lights-off.

> **Safety:** This is a classroom experiment, not traffic-control equipment. Radio delivery is not guaranteed; the design is not certified or safety-validated. Never connect it to a real road or use it to direct people or vehicles. See [Safety](docs/SAFETY.md).

## Features

- Six-phase alternating sequence with non-blocking elapsed-time transitions.
- P0 red, P1 yellow, P2 green on both devices.
- Radio group **138**, with validated phase, heartbeat, command, status and acknowledgement messages.
- Four-digit rolling sequence numbers; duplicate command handling and bounded command retries.
- Follower red fallback after communication loss; coordinator remains the sole timing authority.
- A, B and A+B controls on both devices.

## Hardware

Two BBC micro:bit devices, two red LEDs, two yellow LEDs, two green LEDs, six suitable current-limiting resistors, wires and a common reference (GND). Each micro:bit uses the same pin assignments:

| Pin | LED |
| --- | --- |
| P0 | Red |
| P1 | Yellow |
| P2 | Green |
| GND | Common ground |

Use one resistor in series with each LED. Check polarity and board limits before powering the circuit. See [Wiring](docs/WIRING.md).

## Architecture

- **Micro:bit 1 (coordinator):** owns the phase clock, changes phases, drives its LEDs, processes commands and broadcasts the current phase/heartbeat.
- **Micro:bit 2 (follower):** drives its LEDs from the coordinator's latest valid phase, sends control requests and periodic status messages, and shows red if the coordinator becomes silent.

Both devices accept local buttons. The follower sends requests; it never advances the phase clock independently. This avoids two competing timing authorities. See [Architecture](docs/ARCHITECTURE.md).

## Traffic sequence

| Phase | Direction 1 | Direction 2 | Duration |
| --- | --- | --- | ---: |
| G1 | Green | Red | 8 s |
| Y1 | Yellow | Red | 2 s |
| AR1 | Red | Red | 1 s |
| G2 | Red | Green | 8 s |
| Y2 | Red | Yellow | 2 s |
| AR2 | Red | Red | 1 s |

The two all-red intervals use the shared protocol state `AR`. The sequence repeats until stopped. Durations are experimental defaults, not engineering recommendations. See [State machine](docs/STATE_MACHINE.md).

## Controls

| Input (on either device) | Effect |
| --- | --- |
| A | Start or request start; begins at G1 if stopped |
| B | Stop or request stop; both outputs show red |
| A+B | Switch off all six external LEDs |

Stopping leaves red LEDs on. Switching off extinguishes every external LED; it does not remove power from either micro:bit. A+B is handled as a distinct chord. See [State machine](docs/STATE_MACHINE.md).

## Getting Started

The repository provides two **MakeCode Python source files**. They are not precompiled `.hex` downloads. MakeCode compiles each program when you click **Download**; the resulting `.hex` file is what gets flashed to a micro:bit. A raw `.py` file is source text, not a ready-to-flash program.

1. [Download Micro:bit 1 source](https://raw.githubusercontent.com/Kallekalsong/SmartTraffic/codex/smarttraffic-protocol-docs/src/microbit_1.py).
2. Open [Microsoft MakeCode for micro:bit](https://makecode.microbit.org/) and create a project.
3. Switch the editor to **Python**, then paste the downloaded source into the editor. These files use MakeCode Python; they are not standard MicroPython files or MakeCode `.hex` project imports.
4. Click **Download** and let MakeCode compile the project to a `.hex` file.
5. Connect the first micro:bit over USB and flash that `.hex` file using the [official transfer instructions](https://makecode.microbit.org/device/usb).
6. Repeat steps 2–5 with [Micro:bit 2 source](https://raw.githubusercontent.com/Kallekalsong/SmartTraffic/codex/smarttraffic-protocol-docs/src/microbit_2.py) and the second micro:bit. Build the LED circuit using [Wiring](docs/WIRING.md), power both devices, then press A on either one. Use B to stop or A+B to switch the LEDs off.

MakeCode also supports direct browser transfer on compatible browsers; see its [USB transfer guide](https://makecode.microbit.org/device/usb). For editing and validation details, see [Development](docs/DEVELOPMENT.md).

## Repository layout

- `src/microbit_1.py` — coordinator firmware.
- `src/microbit_2.py` — follower firmware.
- `docs/ARCHITECTURE.md` — roles and data flow.
- `docs/RADIO_PROTOCOL.md` — packet format and recovery behavior.
- `docs/STATE_MACHINE.md` — phases, timings and transitions.
- `docs/WIRING.md` — component and pin guidance.
- `docs/SAFETY.md` — limitations and safe use.
- `docs/DEVELOPMENT.md` — workflow for contributors.
- `CHANGELOG.md`, `CONTRIBUTING.md` — project history and contribution process.

## Status and license

Version **0.1.0** is an initial development release; this is not a claim of a tested or production-ready system. No license file is present. The project remains unlicensed until its owner chooses a license; see [Contributing](CONTRIBUTING.md) before reusing or redistributing it.
