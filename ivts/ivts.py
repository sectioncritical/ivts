#!/usr/bin/env python3

import can
import time
from enum import Enum

class IVTS(object):
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

    class LogData(Enum):
        AS_TOTAL = 1
        AS_CHARGING = 2
        AS_DISCHARGING = 3
        WH_TOTAL = 4
        WH_CHARGING = 5
        WH_DISCHARGING = 6
        RUNTIME_TOTAL = 0x10
        RUNTIME_I_INLIMITS = 0x11
        RUNTIME_I_OVERLIMITS = 0x12
        RUNTIME_U1_INLIMTS = 0x13
        RUNTIME_U1_OVERLIMITS = 0x14
        RUNTIME_U2_INLIMTS = 0x15
        RUNTIME_U2_OVERLIMITS = 0x16
        RUNTIME_U3_INLIMTS = 0x17
        RUNTIME_U3_OVERLIMITS = 0x18
        RUNTIME_T_INLIMTS = 0x19
        RUNTIME_T_OVERLIMITS = 0x1A
        RUNTIME_OC_POS = 0x1B
        RUNTIME_OC_NEG = 0x1C
        I_MAX = 0x21
        I_MIN = 0x22
        U1_MAX = 0x23
        U1_MIN = 0x24
        U2_MAX = 0x25
        U2_MIN = 0x26
        U3_MAX = 0x27
        U3_MIN = 0x28
        T_MAX = 0x29
        T_MIN = 0x2A

    class InfoItem(Enum):
        OC_TESTTIME = 0x73
        MODE = 0x74
        OC_LIMIT_POS = 0x75
        OC_LIMIT_NEG = 0x76
        DEVICE_ID = 0x79
        SW_VERSION = 0x7A
        SER_NUMBER = 0x7B
        ARTICLE_NUMBER = 0x7C

    def __init__(self, canbus=None):
        self._bus = canbus
        # all results [value, counter, flags, fresh]
        self._results = [(0, 0, 0, False)] * 8

    def get_measure_property(self, measure_type: MeasureType):
        result = self._results[measure_type.value]
        if result[3]:
            result[3] = False
            return result[0]
        return None

    @property
    def I(self):
        """The current measurement in mV.

        Returns the last received value for current or None if the value was
        not updated since last read."""
        return self.get_measure_property(self.MeasureType.I)

    @property
    def U1(self):
        return self.get_measure_property(self.MeasureType.U1)

    @property
    def U2(self):
        return self.get_measure_property(MeasureType.U2)

    @property
    def U3(self):
        return self.get_measure_property(MeasureType.U3)

    def get_result(self, measure_type: MeasureType):
        """Get saved measurement result as tuple.

        Returns the result that was cached from the last result message
        received from IVTS. The returned value is a tuple including the
        value, the counter, and flags.

        :param measure_type: which measurement to return (see MeasureType Enum)
        :returns: tuple of (value, counter, flags)

        The format of the returned data is:

        * value - the 32-bit signed integer value of the measurement. Units
          depend on which value is measured. Current is in milliamps and
          voltage is in millivolts.
        * counter - the 4-bit cyclic counter from the result message. This can
          be used to detect if the value is changed
        * flags - 4-bit flags from result message. Not used at this time.
        """
        return self._results[measure_type.value]

    def send_cmd(self, payload):
        print(f"send_cmd({payload})")
        if len(payload) > 8:
            raise ValueError("IVT-S command: bad payload size")

        cmddata = [0] * 8
        cmddata[:len(payload)] = payload
        print(f"cmddata: {cmddata}")
        msg = can.Message(arbitration_id=0x411, is_extended_id=False,
                data=cmddata)
        self._bus.send(msg)

    def set_config(self, measure_type: MeasureType,
                   trigger_mode: TriggerMode, delay_ms: int=0,
                   flags=0):
        payload = [0] * 8
        payload[0] = 0x20 + measure_type.value
        payload[1] = (flags * 16) + trigger_mode.value
        payload[2] = int(delay_ms / 256)
        payload[3] = delay_ms & 0xFF
        self.send_cmd(payload)

    def reset_error_and_logs(self):
        raise NotImplementedError

    def store(self):
        self.send_cmd([0x32])
        time.sleep(1)   # time for storage to complete

    def set_run_mode(self, is_run: bool):
        self.send_cmd([0x34, 1 if is_run else 0, 1, 0, 0])

    def restart(self):
        self.send_cmd([0x3f])

    def get_perm_logdata(self, logitem: LogData):
        self.send_cmd([0x42, logitem.value])

    def get_temp_logdata(self, logitem: LogData):
        self.send_cmd([0x43, logitem.value])

    def get_info(self, infoitem: InfoItem):
        self.send_cmd([infoitem.value])

    def decode_result_val(self, payload):
        counter = payload[1] & 0x0F
        flags = int(payload[1] / 16)
        val = int.from_bytes(payload[2:6], byteorder='big', signed=True)
        return [val, counter, flags, True]

    def decode_result(self, msg: can.Message):
        if len(msg.data) < 6:
            return msg
        if msg.data[0] > 7:
            return msg
        result = self.decode_result_val(msg.data)
        self._results[msg.data[0]] = result
        return None

    def decode_response(self, msg: can.Message):
        if len(msg.data) != 8:
            return msg
        print(msg)
        return None

    def decode(self, msg: can.Message):
        arbid = msg.arbitration_id
        if arbid == 0x511:
            return self.decode_response(msg)
        elif arbid >= 0x521 and arbid <= 0x528:
            return self.decode_result(msg)

if __name__ == "__main__":
    bus = can.Bus(interface="socketcan", channel="can0")

    ivts = IVTS(canbus=bus)
    ivts.get_info(ivts.InfoItem.DEVICE_ID)

    while True:
        msg = bus.recv(timeout=0.1)
        if msg:
            ivts.decode(msg)
            u1 = ivts.U1
            if u1:
                print(f"U1: {u1}")

