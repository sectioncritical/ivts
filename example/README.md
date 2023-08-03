# Basic Example to use IVTS Encoder

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

