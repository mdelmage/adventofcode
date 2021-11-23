#!/usr/bin/env python
# -*- coding: utf-8 -*-

CMD_SEND = 'snd'
CMD_SET = 'set'
CMD_ADD = 'add'
CMD_MULTIPLY = 'mul'
CMD_MODULO = 'mod'
CMD_RECEIVE = 'rcv'
CMD_JUMP_IF_GREATER_THAN_ZERO = 'jgz'

class Program(object):
    def __init__(self, instructions, pid):
        self.pc = 0
        self.peer = None
        self.queue = []
        self.blocked = False
        self.send_count = 0
        self.registers = {}
        self.registers['p'] = pid
        self.instructions = instructions

    def link(self, peer):
        self.peer = peer
        peer.peer = self

    def val(self, s):
        if s.isalpha():
            return self.registers.get(s, 0)
        else:
            return int(s)

    def can_run(self):
        return (len(self.queue) > 0) or (not self.blocked)

    def run(self):
        # See if we were blocked and have then received something (and thus can wake up)
        if self.blocked and len(self.queue) > 0:
            self.blocked = False

        while True:
            cmd = self.instructions[self.pc][0]
            arg1 = self.instructions[self.pc][1]
            if len(self.instructions[self.pc]) == 3: arg2 = self.instructions[self.pc][2]

            if cmd == CMD_SEND:
                self.peer.queue.append(self.val(arg1))
                self.send_count += 1
            elif cmd == CMD_SET:
                self.registers[arg1] = self.val(arg2)
            elif cmd == CMD_ADD:
                self.registers[arg1] = self.val(arg1) + self.val(arg2)
            elif cmd == CMD_MULTIPLY:
                self.registers[arg1] = self.val(arg1) * self.val(arg2)
            elif cmd == CMD_MODULO:
                self.registers[arg1] = self.val(arg1) % self.val(arg2)
            elif cmd == CMD_RECEIVE:
                # For single-program tests, end execution at the first rcv encountered.
                if self.peer == self: return

                if len(self.queue) > 0:
                    self.registers[arg1] = self.queue.pop(0)
                else:
                    self.blocked = True
                    return
            elif cmd == CMD_JUMP_IF_GREATER_THAN_ZERO:
                if self.val(arg1) > 0:
                    self.pc += self.val(arg2) - 1
            self.pc += 1

# Parse the program file
with open('day18_input.txt') as f:
    instructions = [line.rstrip('\n').split() for line in f]

# What is the value of the recovered frequency (the value of the most recently played sound)
# the first time a rcv instruction is executed with a non-zero value?
p = Program(instructions, 0)
p.link(p)
p.run()
print 'Part One: Recovered frequency is {0}.'.format(p.queue.pop(-1))

# As you congratulate yourself for a job well done, you notice that the documentation has been
# on the back of the tablet this entire time. While you actually got most of the instructions
# correct, there are a few key differences. This assembly code isn't about sound at all -
# it's meant to be run twice at the same time.
pid0 = Program(instructions, 0)
pid1 = Program(instructions, 1)
pid0.link(pid1)

while pid0.can_run() or pid1.can_run():
    pid0.run()
    pid1.run()

print 'Part Two: program 1 sent a value {0} times.'.format(pid1.send_count)