#!/usr/bin/env python3

# This example shows how to encode some messages and send to IVTS.
# It does not show how to decode messages.

import time
import ivts
import can

def send_msg(canbus, encresult):
    arbid = encresult[0]
    msgbytes = encresult[1]
    msg = can.Message(arbitration_id=arbid, is_extended_id=False, data=msgbytes)
    canbus.send(msg)
    time.sleep(0.1)

# create the encoder
enc = ivts.Encoder()

# set up CAN bus
bus = can.Bus(interface="socketcan", channel="can0")

# most of the encoder methods return a tuple of arbitration ID
# and CAN message payload. So you can call them with:
#  arbid, msgbytes = enc.some_method()

# get some info first
#send_msg(bus, enc.get_serial_num())
#send_msg(bus, enc.get_version())
#send_msg(bus, enc.get_device_id())

# first the IVTS has to be stopped before config can be changed
send_msg(bus, enc.set_run_mode(False))  # stops immediate run mode

# create config message to cause temp reading to generate every 100 ms
send_msg(bus, enc.set_config(ivts.MeasureType.T, ivts.TriggerMode.CYCLIC, 311))

send_msg(bus, enc.set_config(ivts.MeasureType.I, ivts.TriggerMode.CYCLIC, 7))
send_msg(bus, enc.set_config(ivts.MeasureType.U1, ivts.TriggerMode.CYCLIC, 7))

# turn off the U2 and U3 reporting to reduce clutter on the output
send_msg(bus, enc.set_config(ivts.MeasureType.U2, ivts.TriggerMode.DISABLED, 60))
send_msg(bus, enc.set_config(ivts.MeasureType.U3, ivts.TriggerMode.DISABLED, 60))

send_msg(bus, enc.set_config(ivts.MeasureType.As, ivts.TriggerMode.CYCLIC, 499))
send_msg(bus, enc.set_config(ivts.MeasureType.W, ivts.TriggerMode.CYCLIC, 47))
send_msg(bus, enc.set_config(ivts.MeasureType.Wh, ivts.TriggerMode.CYCLIC, 991))

# reset the log data
#send_msg(bus, enc.reset_logdata(ivts.LogItem.As_TOTAL, 18022594))

# store the config
send_msg(bus, enc.store())
time.sleep(2)

# set IVTS run mode on
encoded = enc.set_run_mode(True)  # starts immediate run mode
send_msg(bus, encoded)

# request total A-h (As)
#send_msg(bus, enc.get_logdata_item(ivts.LogItem.As_TOTAL, is_persistent=False))

# request max U1
#send_msg(bus, enc.get_logdata_item(ivts.LogItem.U1_MAX))

bus.shutdown()
