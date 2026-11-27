# SmartTraffic — Micro:bit 1 (coordinator)
# Microsoft MakeCode Python. Copy this file into the MakeCode Python editor.
# Educational simulation only; never use as real traffic control.

RADIO_GROUP = 138
GREEN_MS = 8000
YELLOW_MS = 2000
ALL_RED_MS = 1000
HEARTBEAT_MS = 500
LINK_TIMEOUT_MS = 1800
ACK_TIMEOUT_MS = 600
MAX_COMMAND_SENDS = 4
SEQUENCE_MODULUS = 10000
SEQUENCE_HALF_RANGE = 5000

# Mutable single-item lists let event callbacks update shared state.
phase = ["STOP"]
running = [False]
phase_started_at = [0]
all_red_next = ["G2"]
next_heartbeat_at = [0]
tx_sequence = [0]
last_follower_sequence = [-1]
last_command_sequence = [-1]
last_follower_status_at = [-1]
follower_connected = [False]
pending_action = [""]
incoming_packet = [""]

def write_lights(red, yellow, green):
    pins.digital_write_pin(DigitalPin.P0, red)
    pins.digital_write_pin(DigitalPin.P1, yellow)
    pins.digital_write_pin(DigitalPin.P2, green)

def show_phase(name):
    # This board represents direction 1; direction 2 phases stay red here.
    if name == "G1":
        write_lights(0, 0, 1)
    elif name == "Y1":
        write_lights(0, 1, 0)
    elif name == "OFF":
        write_lights(0, 0, 0)
    else:
        # AR, G2, Y2, STOP and unknown states are red for direction 1.
        write_lights(1, 0, 0)

def valid_phase(name):
    return (name == "G1" or name == "Y1" or name == "AR" or
            name == "G2" or name == "Y2" or name == "STOP" or
            name == "OFF")

def next_sequence():
    tx_sequence[0] = (tx_sequence[0] + 1) % SEQUENCE_MODULUS
    return ("0000" + str(tx_sequence[0]))[-4:]

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

def broadcast_phase(name):
    phase[0] = name
    show_phase(name)
    phase_started_at[0] = control.millis()
    number = next_sequence()
    radio.send_string(make_packet("P", number, name))

def start_simulation():
    if not running[0]:
        running[0] = True
        broadcast_phase("G1")

def stop_simulation():
    running[0] = False
    broadcast_phase("STOP")

def switch_lights_off():
    running[0] = False
    broadcast_phase("OFF")

def send_ack(request_number, result):
    number = next_sequence()
    request_text = ("0000" + str(request_number))[-4:]
    radio.send_string(make_packet("A", number, request_text + ":" + result))

def handle_command(packet):
    request_number = packet[1]
    command = packet[2]

    # Re-acknowledge a retry of the last accepted command without applying it twice.
    if request_number == last_command_sequence[0]:
        send_ack(request_number, "OK")
        return

    if not sequence_is_newer(request_number, last_follower_sequence[0]):
        return

    last_command_sequence[0] = request_number
    last_follower_sequence[0] = request_number
    if command == "START":
        start_simulation()
        send_ack(request_number, "OK")
    elif command == "STOP":
        stop_simulation()
        send_ack(request_number, "OK")
    elif command == "OFF":
        switch_lights_off()
        send_ack(request_number, "OK")
    else:
        send_ack(request_number, "REJECT")

def process_packet(message):
    packet = parse_packet(message)
    if len(packet) == 0:
        return

    kind = packet[0]
    number = packet[1]
    payload = packet[2]

    if kind == "C":
        handle_command(packet)
    elif kind == "S":
        if payload != "OK":
            return
        if sequence_is_newer(number, last_follower_sequence[0]):
            last_follower_sequence[0] = number
            last_follower_status_at[0] = control.millis()
            follower_connected[0] = True

def on_radio_received(message):
    # Keep the radio event short; the main loop validates and handles the latest packet.
    incoming_packet[0] = message

def on_button_a():
    pending_action[0] = "START"

def on_button_b():
    pending_action[0] = "STOP"

def on_button_ab():
    pending_action[0] = "OFF"

def advance_phase(now):
    elapsed = now - phase_started_at[0]
    if phase[0] == "G1" and elapsed >= GREEN_MS:
        broadcast_phase("Y1")
    elif phase[0] == "Y1" and elapsed >= YELLOW_MS:
        all_red_next[0] = "G2"
        broadcast_phase("AR")
    elif phase[0] == "AR" and elapsed >= ALL_RED_MS and all_red_next[0] == "G2":
        broadcast_phase("G2")
    elif phase[0] == "G2" and elapsed >= GREEN_MS:
        broadcast_phase("Y2")
    elif phase[0] == "Y2" and elapsed >= YELLOW_MS:
        all_red_next[0] = "G1"
        broadcast_phase("AR")
    elif phase[0] == "AR" and elapsed >= ALL_RED_MS and all_red_next[0] == "G1":
        broadcast_phase("G1")

def main_loop():
    action = pending_action[0]
    if action != "":
        pending_action[0] = ""
        if action == "START":
            start_simulation()
        elif action == "STOP":
            stop_simulation()
        elif action == "OFF":
            switch_lights_off()

    message = incoming_packet[0]
    if message != "":
        incoming_packet[0] = ""
        process_packet(message)

    now = control.millis()
    if running[0]:
        advance_phase(now)

    if now - next_heartbeat_at[0] >= HEARTBEAT_MS:
        next_heartbeat_at[0] = now
        number = next_sequence()
        radio.send_string(make_packet("H", number, phase[0]))

    if last_follower_status_at[0] >= 0:
        follower_connected[0] = (now - last_follower_status_at[0] <= LINK_TIMEOUT_MS)

    basic.pause(20)

# Explicit startup: all outputs are red; the simulation starts only on request.
radio.set_group(RADIO_GROUP)
radio.set_transmit_power(6)
write_lights(1, 0, 0)
radio.on_received_string(on_radio_received)
input.on_button_pressed(Button.A, on_button_a)
input.on_button_pressed(Button.B, on_button_b)
input.on_button_pressed(Button.AB, on_button_ab)
basic.forever(main_loop)
