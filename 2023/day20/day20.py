#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Modules communicate using pulses. Each pulse is either a high pulse or a low pulse.
LOW  = 0
HIGH = 1

OFF = 0
ON  = 1

FLIP_FLOP   = '%'
CONJUNCTION = '&'
BROADCAST   = 'broadcaster'
UNKNOWN     = 'unknown'

class Module:
    def __init__(self, _name, _type, _outputs):
        self.name = _name
        self.type = _type
        self.outputs = _outputs

        if _type == FLIP_FLOP:
            # Flip-flop modules (prefix %) are either on or off; they are initially off.
            self.state = OFF
        elif _type == CONJUNCTION:
            # Conjunction modules (prefix &) remember the type of the most recent pulse received
            # from each of their connected input modules; they initially default to remembering a
            # low pulse for each input. 
            self.inputs = {}

    def connect(self, input_module):
        # Conjunction modules (prefix &) remember the type of the most recent pulse received
        # from each of their connected input modules; they initially default to remembering a
        # low pulse for each input. 
        if self.type == CONJUNCTION: self.inputs[input_module] = LOW

    def pulse(self, originator, pulse_type):
        if self.type == FLIP_FLOP:
            # If a flip-flop module receives a high pulse, it is ignored and nothing happens.
            # However, if a flip-flop module receives a low pulse, it flips between on and off.
            # If it was off, it turns on and sends a high pulse. If it was on, it turns off and
            # sends a low pulse.
            if pulse_type == LOW:
                self.state ^= 1
                for o in self.outputs:
                    pulse_queue.append((self.name, self.state, o))
        elif self.type == CONJUNCTION:
            # When a pulse is received, the conjunction module first updates
            # its memory for that input. Then, if it remembers high pulses for all inputs, it sends a
            # low pulse; otherwise, it sends a high pulse.
            self.inputs[originator] = pulse_type
            all_inputs = sum([self.inputs[x] for x in self.inputs])
            for o in self.outputs:
                if all_inputs == len(self.inputs):
                    pulse_queue.append((self.name, LOW, o))
                else:
                    pulse_queue.append((self.name, HIGH, o))
        elif self.type == BROADCAST:
            # There is a single broadcast module (named broadcaster). When it receives a pulse,
            # it sends the same pulse to all of its destination modules.
            for o in self.outputs:
                pulse_queue.append((self.name, pulse_type, o))

        return

# Parse the workflows and part ratings.
with open('day20_input.txt') as f:
    lines = [line.rstrip('\n').split(' -> ') for line in f]

    modules = {}
    for line in lines:
        module_id = line[0]
        outputs = line[1].replace(' ', '').split(',')
        if module_id[0] == FLIP_FLOP:
            module_type = FLIP_FLOP
            module_name = module_id[1:]
        elif module_id[0] == CONJUNCTION:
            module_type = CONJUNCTION
            module_name = module_id[1:]
        elif module_id == BROADCAST:
            module_type = BROADCAST
            module_name = module_id

        modules[module_name] = Module(module_name, module_type, outputs)

    # Make a second pass now that the objects have been created.
    # Connect each module to its inputs.
    # There's probably a better way to do this.
    for line in lines:
        module_id = line[0]
        outputs = line[1].replace(' ', '').split(',')
        if module_id[0] == FLIP_FLOP:
            module_type = FLIP_FLOP
            module_name = module_id[1:]
        elif module_id[0] == CONJUNCTION:
            module_type = CONJUNCTION
            module_name = module_id[1:]
        else:
            module_type = BROADCAST
            module_name = module_id
        for o in outputs:
            if o not in modules: modules[o] = Module(module_name, UNKNOWN, [])
            modules[o].connect(module_name)


# By inspection: module 'rx' is fed by a conjunction (aka NAND) module, 'lg', which in turn
# is fed by four modules: 'ls', 'nb', 'vc', 'vg'.
button_presses_for_rx = 1
period_targets = ['ls', 'nb', 'vc', 'vg']

# To get the cables warmed up, the Elves have pushed the button 1000 times.
# How many pulses got sent as a result (including the pulses sent by the button itself)?
pulse_count = {LOW: 0, HIGH: 0}
button_presses = 0

while len(period_targets) > 0:
    pulse_queue = []

    # Here at Desert Machine Headquarters, there is a module with a single button on it called,
    # aptly, the button module. When you push the button, a single low pulse is sent directly
    # to the broadcaster module.
    pulse_queue.append(('button', LOW, BROADCAST))
    button_presses += 1

    while len(pulse_queue) > 0:
        (tx, pulse_type, rx) = pulse_queue.pop(0)
        modules[rx].pulse(tx, pulse_type)
        if button_presses <= 1000: pulse_count[pulse_type] += 1

        # The four modules that feed 'lg' send high pulses at regular intervals, a few thousand button
        # presses apart, and all different to each other. Therefore the minimum number of button presses
        # before 'rx' receives a low pulse is Least Common Multiple (LCM) of the periods of these pulses.
        # These periods are all prime for my input, so a more straightforward (but possibly incorrect)
        # solution is just to be to find the product of all periods.
        m = modules['lg']
        periods = []
        all_inputs = sum([m.inputs[x] for x in m.inputs])
        if rx == 'lg' and tx in period_targets and pulse_type == HIGH:
            period_targets.remove(tx)
            button_presses_for_rx *= button_presses

# Consult your module configuration; determine the number of low pulses and high pulses that
# would be sent after pushing the button 1000 times, waiting for all pulses to be fully handled
# after each push of the button. What do you get if you multiply the total number of low pulses
# sent by the total number of high pulses sent?
print('Part One: Product of low pulses and high pulses is {0}.'.format(pulse_count[LOW] * pulse_count[HIGH]))

# Reset all modules to their default states. Waiting for all pulses to be fully handled after each
# button press, what is the fewest number of button presses required to deliver a single low pulse
# to the module named rx?
print('Part Two: Fewest number of button presses for a low pulse to rx is {0}.'.format(button_presses_for_rx))