#!/usr/bin/env python3

# This example shows how to encode some messages and send to IVTS.
# It does not show how to decode messages.

import ivts
import can

# create the encoder
enc = ivts.Encoder()

# set up CAN bus
bus = can.Bus(interface="socketcan", channel="can0")

# first the IVTS has to be stopped before config can be changed
encmsg = enc.set_run_mode(False)  # stops immediate run mode
arbid = encmsg[0]
msgbytes = encmsg[1]

# msg is encoded, create CAN message and send it
msg = can.Message(arbitration_id=arbid, is_extended_id=False, data=msgbytes)
bus.send(msg)

# create config message to cause temp reading to generate every 1000 ms
encmsg = enc.set_config(ivts.MeasureType.T, ivts.TriggerMode.CYCLIC, 1000)
arbid = encmsg[0]
msgbytes = encmsg[1]

# msg is encoded, create CAN message and send it
msg = can.Message(arbitration_id=arbid, is_extended_id=False, data=msgbytes)
bus.send(msg)

# set IVTS run mode on
encmsg = enc.set_run_mode(True)  # starts immediate run mode
arbid = encmsg[0]
msgbytes = encmsg[1]

# msg is encoded, create CAN message and send it
msg = can.Message(arbitration_id=arbid, is_extended_id=False, data=msgbytes)
bus.send(msg)
