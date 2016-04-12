#
# mostly from
#   http://bioportal.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/socket/multicast.html
#
import json
import socket
import struct
import sys
import time
import datetime

multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

devices = {}

# Receive/respond loop
while True:
    #print >>sys.stderr, '\nwaiting to receive message'
    data, address = sock.recvfrom(1024)
    try:
        #print json.loads (data)

        stamp = datetime.datetime.now()

        parsedData = json.loads (data)

        devices[parsedData["hostname"]] = { 'lastSeen': stamp }

        print 'Timestamp: ', stamp, '\n'
        #sender = data['hostname']
        print >>sys.stdout, devices
    except:
        #print >> sys.stderr, "Error decode failure"
        print 'Failed to decode from %s' %(address, )
        stamp2 = datetime.datetime.now()
        print stamp2
    #print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    print data


