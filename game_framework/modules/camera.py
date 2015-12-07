# coding=utf-8
"""
Camera module

Moves camera towards where the user is looking.

Author: Tomi Simsiö
"""

from basemodule import BaseModule
import uinput


class Camera(BaseModule):

    left_ticks = 0
    right_ticks = 0
    up_ticks = 0
    down_ticks = 0

    def __init__(self, gameconfig):
        super(Camera, self).__init__()
        self.ticks_needed = gameconfig.getint('Camera', 'ticks_needed')
        self.action_every_ticks = gameconfig.getint('Camera', 'action_every_ticks')
        self.move_method = gameconfig.get('Camera', 'move_method')
        if self.move_method == "wasd":
            self.device = uinput.Device([
                uinput.KEY_A,
                uinput.KEY_D,
                uinput.KEY_W,
                uinput.KEY_S,
            ])
        elif self.move_method == "arrows":
            self.device = uinput.Device([
                uinput.KEY_LEFT,
                uinput.KEY_RIGHT,
                uinput.KEY_UP,
                uinput.KEY_DOWN,
            ])
        else:
            print "Unknown move_method '%s'" % self.move_method
            exit(10)

        self.left_start = gameconfig.getfloat('Camera', 'left_start')
        self.right_start = gameconfig.getfloat('Camera', 'right_start')
        self.up_start = gameconfig.getfloat('Camera', 'up_start')
        self.down_start = gameconfig.getfloat('Camera', 'down_start')

        self.left_margin = gameconfig.getfloat('Camera', 'left_margin')
        self.right_margin = gameconfig.getfloat('Camera', 'right_margin')
        self.up_margin = gameconfig.getfloat('Camera', 'up_margin')
        self.down_margin = gameconfig.getfloat('Camera', 'down_margin')

    def tick(self, event):
        if not event.fixation['valid']:
            # Fixation not valid, reset all counters to avoid unwanted actions
            self.left_ticks = 0
            self.right_ticks = 0
            self.up_ticks = 0
            self.down_ticks = 0
            pass

        self.increment_ticks(event)
        self.do_actions()

    def increment_ticks(self, event):
        # Left
        if self.left_margin < event.fixation['x'] < self.left_start:
            self.left_ticks += 1
        else:
            self.left_ticks = 0
        # Right
        if self.right_margin > event.fixation['x'] > self.right_start:
            self.right_ticks += 1
        else:
            self.right_ticks = 0
        # Up
        if self.up_margin < event.fixation['y'] < self.up_start:
            self.up_ticks += 1
        else:
            self.up_ticks = 0
        # Down
        if self.down_margin > event.fixation['y'] > self.down_start:
            self.down_ticks += 1
        else:
            self.down_ticks = 0

    def do_actions(self):
        if self.left_ticks > self.ticks_needed and self.left_ticks % self.action_every_ticks == 0:
            self.device.emit_click(uinput.KEY_A if self.move_method == "wasd" else uinput.KEY_LEFT)
            print "Action: left"
        if self.right_ticks > self.ticks_needed and self.right_ticks % self.action_every_ticks == 0:
            self.device.emit_click(uinput.KEY_D if self.move_method == "wasd" else uinput.KEY_RIGHT)
            print "Action: right"
        if self.up_ticks > self.ticks_needed and self.up_ticks % self.action_every_ticks == 0:
            self.device.emit_click(uinput.KEY_W if self.move_method == "wasd" else uinput.KEY_UP)
            print "Action: up"
        if self.down_ticks > self.ticks_needed and self.down_ticks % self.action_every_ticks == 0:
            self.device.emit_click(uinput.KEY_S if self.move_method == "wasd" else uinput.KEY_DOWN)
            print "Action: down"
