# Safety and limitations

SmartTraffic is an educational bench simulation for learning about micro:bit programming, state machines and radio messages.

- **Not real traffic control:** Never install or use this project on a road, vehicle, crossing, or public/private traffic facility. It must not direct drivers, cyclists or pedestrians.
- **Not certified:** The project is not certified, redundant, fail-operational or formally safety validated.
- **Radio is unreliable:** Interference, range, packet loss, collisions, resets and power problems can cause stale or inconsistent displays. A heartbeat timeout and red fallback reduce some confusion but cannot guarantee a safe output.
- **Hardware is limited:** The code assumes working micro:bit pins and LEDs. It does not detect broken LEDs, short circuits, current overload, battery failure or wiring mistakes.
- **Software is experimental:** Timing and protocol logic have not undergone formal verification. A reset or unknown fault can disrupt operation.
- **Use resistors:** Every external LED needs a suitable series current-limiting resistor. Check the micro:bit electrical limits and have wiring inspected before applying power.
- **Fallback is only a display behavior:** “Red on error” describes the firmware's intended response; it is not a certified fail-safe and does not ensure other outputs or both devices are red simultaneously.
- **No guaranteed delivery or authentication:** Group 138 is not a security boundary. Packets can be lost, observed or spoofed by another device using that group.

Use only under supervision in a controlled classroom or lab. Keep outputs disconnected from any equipment that could affect people or traffic.
