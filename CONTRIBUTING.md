# Contributing

Thank you for helping improve SmartTraffic. Contributions should keep this a clear, reproducible educational experiment.

## Report a bug or suggest an improvement

Open a GitHub issue with a concise title, steps to reproduce, expected and observed behavior, the MakeCode editor/target version if known, and whether the result came from the simulator or physical boards. Include relevant packet examples or wiring details, but do not include personal data.

## Submit a change

1. Fork the repository or create a topic branch.
2. Make a focused change and update relevant documentation.
3. Check both device programs and their protocol/state-machine documentation together.
4. Validate the source in the MakeCode Python editor/simulator when possible. For hardware checks, describe the boards and exact setup; never imply that an unrun test passed.
5. Open a pull request describing purpose, implementation, verification performed and remaining limitations.

## Documentation and code standards

- Use clear English, named constants and comments that explain design choices.
- Keep radio callbacks short and timing non-blocking.
- Keep pin assignments P0 red, P1 yellow, P2 green and radio group 138 consistent.
- Document packet/schema changes and recovery behavior.
- Do not introduce external components as required hardware without updating the wiring and README.
- Avoid claims of reliability, certification or real-world suitability.

## Safety expectations

SmartTraffic must remain explicitly educational. Do not propose connecting it to real traffic infrastructure or use it to direct people or vehicles. Every LED requires an appropriate series resistor. Safety concerns should be raised promptly in an issue or pull request.

## License

No license has been selected or added. Ask the repository owner to choose one before copying, redistributing or contributing under assumed licensing terms.
