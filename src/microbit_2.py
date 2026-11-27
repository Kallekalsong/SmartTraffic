# SmartTraffic — Micro:bit 2 (follower)
# Microsoft MakeCode Python. Copy this file into the MakeCode Python editor.
# Educational simulation only; never use as real traffic control.

RADIO_GROUP = 138
HEARTBEAT_MS = 500
LINK_TIMEOUT_MS = 1800
ACK_TIMEOUT_MS = 600
STATUS_MS = 500
MAX_COMMAND_SENDS = 4
SEQUENCE_MODULUS = 10000
SEQUENCE_HALF_RANGE = 5000

phase = ["STOP"]
last_coordinator_sequence = [-1]
last_coordinator_packet_at = [-1]
next_status_at = [0]
tx_sequence = [0]
pending_action = [""]
incoming_packet = [""]
pending_packet = [""]
pending_sequence = [""]
pending_attempts = [0]
pending_sent_at = [0]
link_ok = [False]

def write_lights(red, yellow, green):
    pins.digital_write_pin(DigitalPin.P0, red)
    pins.digital_write_pin(DigitalPin.P1, yellow)
    pins.digital_write_pin(DigitalPin.P2, green)

def show_phase(name):
    # This board represents direction 2; direction 1 phases stay red here.
    if name == "G2":
        write_lights(0, 0, 1)
    elif name == "Y2":
        write_lights(0, 1, 0)
    elif name == "OFF":
        write_lights(0, 0, 0)
    else:
        # AR, G1, Y1, STOP and unknown states are red for direction 2.
        write_lights(1, 0, 0)

def valid_phase(name):
    return (name == "G1" or name == "Y1" or name == "AR" or
            name == "G2" or name == "Y2" or name == "STOP" or
            name == "OFF")

def next_sequence():
    tx_sequence[0] = (tx_sequence[0] + 1) % SEQUENCE_MODULUS
    number = str(tx_sequence[0])
    while len(number) < 4:
        number = "0" + number
    return number

def sequence_is_newer(value, previous):
    if previous < 0:
        return True
    distance = (value - previous + SEQUENCE_MODULUS) % SEQUENCE_MODULUS
    return distance > 0 and distance < SEQUENCE_HALF_RANGE

def make_packet(kind, number, payload):
    return "ST1|" + kind + "|" + number + "|" + payload

def parse_packet(message):
    if len(message) < 13 or message[0:4] != "ST1|":
        return []
    if message[5:6] != "|" or message[10:11] != "|":
        return []
    number = message[6:10]
    for index in range(0, 4):
        character = number[index:index + 1]
        if character < "0" or character > "9":
            return []
    return [message[4:5], int(number), message[11:]]

def send_command(command):
    number = next_sequence()
    packet = make_packet("C", number, command)
    radio.send_string(packet)
    pending_packet[0] = packet
    pending_sequence[0] = number
    pending_attempts[0] = 1
    pending_sent_at[0] = control.millis()

def handle_ack(payload):
    if pending_sequence[0] == "" or len(payload) < 7:
        return
    if payload[0:4] != pending_sequence[0] or payload[4:5] != ":":
        return
    result = payload[5:]
    if result != "OK" and result != "REJECT":
        return
    pending_packet[0] = ""
    pending_sequence[0] = ""
    pending_attempts[0] = 0
    if result == "REJECT":
        phase[0] = "STOP"
        show_phase("STOP")

def process_packet(message):
    packet = parse_packet(message)
    if len(packet) == 0:
        return

    kind = packet[0]
    number = packet[1]
    payload = packet[2]

    if kind != "P" and kind != "H" and kind != "A":
        return
    now = control.millis()
    if last_coordinator_packet_at[0] >= 0 and now - last_coordinator_packet_at[0] > LINK_TIMEOUT_MS:
        # A quiet coordinator may have restarted with its sequence counter at zero.
        last_coordinator_sequence[0] = -1
    if not sequence_is_newer(number, last_coordinator_sequence[0]):
        return
    last_coordinator_sequence[0] = number
    last_coordinator_packet_at[0] = now
    link_ok[0] = True

    if kind == "A":
        handle_ack(payload)
    elif valid_phase(payload):
        phase[0] = payload
        show_phase(payload)
    else:
        # Invalid state from the coordinator is treated as a fault.
        phase[0] = "STOP"
        show_phase("STOP")

def on_radio_received(message):
    incoming_packet[0] = message

def on_button_a():
    pending_action[0] = "START"

def on_button_b():
    pending_action[0] = "STOP"

def on_button_ab():
    pending_action[0] = "OFF"

def handle_local_action(action):
    # A new deliberate action supersedes an unacknowledged older request.
    send_command(action)

def main_loop():
    action = pending_action[0]
    if action != "":
        pending_action[0] = ""
        handle_local_action(action)

    message = incoming_packet[0]
    if message != "":
        incoming_packet[0] = ""
        process_packet(message)

    now = control.millis()
    if pending_packet[0] != "" and now - pending_sent_at[0] >= ACK_TIMEOUT_MS:
        if pending_attempts[0] < MAX_COMMAND_SENDS:
            radio.send_string(pending_packet[0])
            pending_attempts[0] = pending_attempts[0] + 1
            pending_sent_at[0] = now
        else:
            # A request that cannot be confirmed leaves this unit showing red.
            pending_packet[0] = ""
            pending_sequence[0] = ""
            phase[0] = "STOP"
            show_phase("STOP")

    if now - next_status_at[0] >= STATUS_MS:
        next_status_at[0] = now
        # Avoid advancing this device's sequence between command retries.
        if pending_packet[0] == "":
            number = next_sequence()
            radio.send_string(make_packet("S", number, "OK"))

    if last_coordinator_packet_at[0] >= 0:
        if now - last_coordinator_packet_at[0] > LINK_TIMEOUT_MS and link_ok[0]:
            link_ok[0] = False
            last_coordinator_sequence[0] = -1
            phase[0] = "STOP"
            show_phase("STOP")

    basic.pause(20)

# Explicit startup: red until a valid coordinator packet arrives.
radio.set_group(RADIO_GROUP)
radio.set_transmit_power(6)
write_lights(1, 0, 0)
radio.on_received_string(on_radio_received)
input.on_button_pressed(Button.A, on_button_a)
input.on_button_pressed(Button.B, on_button_b)
input.on_button_pressed(Button.AB, on_button_ab)
basic.forever(main_loop)
