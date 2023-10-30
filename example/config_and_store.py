#!/usr/bin/env python3

# This example shows how to configure the IVTS and store the configuragtion
# so that it will be retained after a power cycle.

import time
import ivts
import can

# A function to roll up all the steps for sending a CAN message.
#  * canbus - an opened can.Bus
#  * encresult - the result from most ivts.Encoder methods)
#
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
#
# Using the send_msg() function, this can be simplified to:
#  send_msg(bus, enc.some_method())
#
# Which will encode the desired CAN message and pass it directly to send_msg()
# for transmitting on the CAN bus

# first the IVTS has to be stopped before config can be changed
send_msg(bus, enc.set_run_mode(False))  # stops immediate run mode

# send messages to configure each of the cyclic values to our desired rate
send_msg(bus, enc.set_config(ivts.MeasureType.T, ivts.TriggerMode.CYCLIC, 311))
send_msg(bus, enc.set_config(ivts.MeasureType.I, ivts.TriggerMode.CYCLIC, 7))
send_msg(bus, enc.set_config(ivts.MeasureType.U1, ivts.TriggerMode.CYCLIC, 7))
send_msg(bus, enc.set_config(ivts.MeasureType.As, ivts.TriggerMode.CYCLIC, 499))
send_msg(bus, enc.set_config(ivts.MeasureType.W, ivts.TriggerMode.CYCLIC, 47))
send_msg(bus, enc.set_config(ivts.MeasureType.Wh, ivts.TriggerMode.CYCLIC, 991))

# turn off the U2 and U3 reporting to reduce clutter on the output
# note: the time argument must have some non-zero value to avoid message error
send_msg(bus, enc.set_config(ivts.MeasureType.U2, ivts.TriggerMode.DISABLED, 60))
send_msg(bus, enc.set_config(ivts.MeasureType.U3, ivts.TriggerMode.DISABLED, 60))

# store the config
send_msg(bus, enc.store())
time.sleep(2)  # give it plenty of time to complete the store operation

# set IVTS run mode on
encoded = enc.set_run_mode(True)  # starts immediate run mode
send_msg(bus, encoded)

bus.shutdown()
