# Development

## Open and flash

1. Open [MakeCode for micro:bit](https://makecode.microbit.org/) and create a Python project.
2. Copy `src/microbit_1.py` into the coordinator project and download it to device 1.
3. Create another project, copy `src/microbit_2.py` and download it to device 2.
4. Use the wiring in [Wiring](WIRING.md), then test on a bench with both devices powered.

The repository contains standalone source text rather than MakeCode `.hex` or project-export files. The firmware has not been physically tested as part of this repository update. Use the MakeCode editor's Python view and simulator/compiler before flashing, then verify behavior with the actual boards.

## Change phase timing

Edit the named constants near the top of `src/microbit_1.py`:

- `GREEN_MS` (default 8000)
- `YELLOW_MS` (default 2000)
- `ALL_RED_MS` (default 1000)

The follower does not need matching duration values because it follows phase broadcasts. Keep values positive and preserve all-red transitions between directions.

## Change the protocol

Read [Radio Protocol](RADIO_PROTOCOL.md) before changing packet fields, message types, sequence handling or timing. Keep both firmware files and the protocol documentation in sync. Preserve input validation and duplicate handling. Do not treat group number as authentication.

## Add behavior

- Keep radio callbacks short; update the one-item packet buffer and handle work in the main loop.
- Avoid blocking phase-duration delays; use elapsed time and short pauses.
- Keep both devices' P0/P1/P2 assignments consistent.
- Add documentation for new states, button behavior, errors and packets.
- Treat any changed output or recovery behavior as educational simulation behavior only.

## Review checklist

Before proposing a change, check both firmware files against the protocol and state diagram, verify pin and button descriptions, inspect MakeCode Python compatibility in the editor, and test on physical devices only in a supervised bench setup. Record exactly which checks were run; do not claim simulator or hardware results that were not observed. Bug reports and contributions are described in [Contributing](../CONTRIBUTING.md).
