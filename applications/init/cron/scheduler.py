#!/usr/bin/env python
import time

fp = open("/tmp/test", "w")
fp.write(time.ctime()+"\n")
fp.write(str(dir(db))+"\n")
fp.write(str(dir(gl))+"\n")
fp.close()


#db.
#gl.

