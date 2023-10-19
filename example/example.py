#!/usr/bin/env python3

# This example shows how to encode some messages and send to IVTS.
# It does not show how to decode messages.

import time
import ivts
import can

# create the encoder
enc = ivts.Encoder()

# set up CAN bus
bus = can.Bus(interface="socketcan", channel="can0")

# most of the encoder methods return a tuple of arbitration ID
# and CAN message payload. So you can call them with:
#  arbid, msgbytes = enc.some_method()

# first the IVTS has to be stopped before config can be changed
arbid, msgbytes = enc.set_run_mode(False)  # stops immediate run mode
# msg is encoded, create CAN message and send it
msg = can.Message(arbitration_id=arbid, is_extended_id=False, data=msgbytes)
bus.send(msg)

time.sleep(0.5)  # delay to let system stop

# create config message to cause temp reading to generate every 100 ms
arbid, msgbytes = enc.set_config(ivts.MeasureType.T, ivts.TriggerMode.CYCLIC, 100)
msg = can.Message(arbitration_id=arbid, is_extended_id=False, data=msgbytes)
bus.send(msg)

time.sleep(0.5)  # delay to let command take effect

# set IVTS run mode on
arbid, msgbytes = enc.set_run_mode(True)  # starts immediate run mode
msg = can.Message(arbitration_id=arbid, is_extended_id=False, data=msgbytes)
bus.send(msg)

time.sleep(0.5)  # delay to let system start

# request total A-h (As)
arbid, msgbytes = enc.get_logdata_item(ivts.LogItem.As_TOTAL, is_persistent=True)
msg = can.Message(arbitration_id=arbid, is_extended_id=False, data=msgbytes)
bus.send(msg)

bus.shutdown()
