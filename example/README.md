# Basic Example to use IVTS Encoder

## Hardware Setup

This example assumes that a CAN bus is configured and enabled and is using the
name `can0`. For the typical RPi setup with MCP2515 board that has correct
boot drivers installed, you can enable the CAN interface with:

    sudo ip link set can0 up type can bitrate 500000

## Example

This is a simple example to show how to use the ivts.Encoder module to encode
CAN messages that can be sent to an IVTS on a CAN bus.

This example only shows how to send messages, not receive or decode. That is
TBD.

To run this test you should use a python virtual environment to set up
the requirements.

    python3 -m venv venv
    . venv/bin/activate

    # at this point make sure that venv was actually create and that you
    # activated the virtual environment with no error messages

    # this will install everything needed for the example
    pip install -r requirements.txt

    # run the example
    python3 example.py

    # use some means to confirm the commands were sent (CAN analyzer etc)

    # now you can delete the venv
    deactivate
    rm -rf venv

## Viewing IVTS Output (temporary)

Until a proper decoder is added, you can use the cantools `monitor` program
to capture and display the IVTS CAN messages.

Assuming you have a CAN interface up and running and is named `can0` you can
use this:

    python3 -m cantools monitor -c can0 IVT-S_12082020.dbc

You can run this in a separate window from the example program above.
