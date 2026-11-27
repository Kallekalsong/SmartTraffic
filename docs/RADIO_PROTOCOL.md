# Radio protocol

## Radio setup

Both devices call `radio.set_group(138)` and configure transmit power to 6. A group is a filtering setting, not authentication, privacy or a guarantee that only these two devices can transmit.

## Packet format

Packets are ASCII strings with four pipe-separated fields:

```text
ST1|<type>|<sequence>|<payload>
```

| Field | Meaning |
| --- | --- |
| `ST1` | Protocol identifier and version |
| `type` | One uppercase message type listed below |
| `sequence` | Four decimal digits, 0000–9999, rolling modulo 10000 |
| `payload` | Type-specific value |

The firmware checks the prefix, separators and sequence digits before interpreting a packet. Unknown types, invalid states and stale sequence numbers are ignored or handled with the documented red fallback.

### Types and examples

| Type | Direction | Payload | Example |
| --- | --- | --- | --- |
| `P` | Coordinator → follower | Current phase | `ST1|P|0042|G1` |
| `H` | Coordinator → follower | Current phase heartbeat | `ST1|H|0043|G1` |
| `C` | Follower → coordinator | `START`, `STOP` or `OFF` | `ST1|C|0017|START` |
| `A` | Coordinator → follower | Request sequence, colon, `OK` or `REJECT` | `ST1|A|0044|0017:OK` |
| `S` | Follower → coordinator | `OK` status heartbeat | `ST1|S|0018|OK` |

Phase payloads are `G1`, `Y1`, `AR`, `G2`, `Y2`, `STOP` and `OFF`. `AR` represents either of the two all-red intervals; the coordinator's local timer distinguishes their position in the cycle.

## Sequence and duplicate handling

Each sender increments its own sequence for every new packet and wraps from 9999 to 0000. The receiver accepts only a sequence that is forward within half of the 10,000-value range; this handles normal wraparound and rejects duplicates or older packets. A device restart resets its counter, so packets from before a restart can be rejected until the counter advances sufficiently or the receiver restarts. There is no persistent session identifier.

The coordinator remembers the most recent follower command. If the same command is retried, it sends another acknowledgement without applying the action a second time. Older commands are ignored. A new start/stop/off action replaces a pending follower request.

## Acknowledgements, heartbeat and timeout

The follower resends an unacknowledged command every 600 ms, up to four total transmissions. The acknowledgement repeats the command's sequence in its payload. Exhausting retries makes the follower display red. The coordinator sends a phase heartbeat every 500 ms, including while stopped or switched off. The follower considers the link timed out after 1.8 seconds without a newer coordinator packet and displays red. The follower sends a status heartbeat every 500 ms when it has no command retry in progress.

These intervals are configurable implementation values, not measured radio performance guarantees. Heartbeats and acknowledgements reduce uncertainty; they cannot eliminate packet loss, interference, collision, power loss or software faults.

## Recovery and limitations

After a communication timeout, a later valid coordinator packet restores the follower's current displayed phase. A coordinator restart starts in STOP with a fresh sequence counter; the follower may need its own restart if the reset counter is treated as stale. No authentication, checksum beyond the radio layer, persistent boot ID, encryption, or formal delivery guarantee is implemented. The one-item receive buffer can overwrite an earlier packet during a burst. This protocol is for a small educational demonstration only.
