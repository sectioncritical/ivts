#!/usr/bin/env python3
#
# SPDX-License-Identifier: MIT
#
# Copyright 2023 Joseph Kroesche
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

from enum import Enum

class MeasureType(Enum):
    I = 0
    U1 = 1
    U2 = 2
    U3 = 3
    T = 4
    W = 5
    As = 6
    Wh = 7

class TriggerMode(Enum):
    DISABLED = 0
    TRIGGERED = 1
    CYCLIC = 2


class Encoder(object):
    def set_config(self, measure_type: MeasureType,
                   trigger_mode: TriggerMode, delay_ms: int=0, flags: int=0):
        """Set reporting configuration for a measurement.

        :param measure_type: specifies which measurement to configure
        :type  measure_type: ivts.MeasureType
        :param trigger_mode: specifies the reporting trigger mode (cyclic, etc)
        :type  trigger_mode: ivts.TriggerMode
        :param delay_ms: reporting delay or cycle time in milliseconds
        :type  delay_ms: int
        :param flags: special config flags, not needed (see IVTS data sheet)
        :type  flags: int
        :return: tuple consisting of CAN ID and bytes-like CAN payload of len 8
        """
        payload = bytearray(8)
        payload[0] = 0x20 + measure_type.value
        payload[1] = (flags * 16) + trigger_mode.value
        payload[2] = int(delay_ms / 256)
        payload[3] = delay_ms & 0xFF
        return (0x411, payload)

    def reset_error_and_logdata(self):
        raise NotImplementedError

    def trigger(self, trig_list):
        """Trigger a measurement cycle.

        Use this to cause a one time measurement of one or more parameters.
        The item being measured must have previously been set up for trigger
        mode. The parameter trig_list is a list of one or more measurement
        items of type MeasureType.

        :param trig_list: list of measurements of type MeasureType
        :return: tuple consisting of CAN ID and bytes-like CAN payload of len 8
        """
        mask = 0
        for trig in trig_list:
            bits = 1 << trig.value
            mask |= bits
        payload = bytearray(8)
        payload[0] = 0x31
        payload[1] = mask >> 8
        payload[2] = mask & 0xFF
        return (0x411, payload)

    def store(self):
        """Save all configured items to non-volatile memory."""
        payload = bytearray(8)
        payload[0] = 0x32
        return (0x411, payload)

    def set_run_mode(self, immed_is_run: bool, startup_is_run: bool=True):
        """Set the run mode for immediate and startup conditions.

        :param immed_is_run: run mode to take effect immediately. If True then
            run mode is started. If False the it is halted.
        :type  immed_is_run: bool
        :param restart_is_run: run mode after a startup (STORE operation is
            required). True for IVTS to enter run mode at startup (default)
        :type  restart_is_run: bool
        :return: tuple consisting of CAN ID and bytes-like CAN payload of len 8
        """
        payload = bytearray(8)
        payload[0] = 0x34
        payload[1] = 1 if immed_is_run else 0
        payload[2] = 1 if startup_is_run else 0
        # payload 3 and 4 are 0 for "user mode"
        return (0x411, payload)

    def set_oc_pos_threshold(self, set_thresh: int, reset_thresh: int):
        raise NotImplementedError

    def set_oc_neg_threshold(self, set_thresh: int, reset_thresh: int):
        raise NotImplementedError

    def restart(self):
        """Restart the IVTS.

        :return: tuple consisting of CAN ID and bytes-like CAN payload of len 8
        """
        payload = bytearray(8)
        payload[0] = 0x3F
        return(0x411, payload)
