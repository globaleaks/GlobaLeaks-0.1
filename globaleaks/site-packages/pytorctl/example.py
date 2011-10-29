"""
The following is a simple example of TorCtl usage. This attaches a listener
that prints the amount of traffic going over tor each second.
"""

import time
import TorCtl

class BandwidthListener(TorCtl.PostEventListener):
  def __init__(self):
    TorCtl.PostEventListener.__init__(self)

  def bandwidth_event(self, event):
    print "tor read %i bytes and wrote %i bytes" % (event.read, event.written)

# constructs a listener that prints BW events
myListener = BandwidthListener()

# initiates a TorCtl connection, returning None if it was unsuccessful
conn = TorCtl.connect()

if conn:
  # tells tor to send us BW events
  conn.set_events(["BW"])

  # attaches the listener so it'll receive BW events
  conn.add_event_listener(myListener)

  # run until we get a keyboard interrupt
  try:
    while True:
      time.sleep(10)
  except KeyboardInterrupt: pass

