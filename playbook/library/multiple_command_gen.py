#!/usr/bin/python3

import sys

def generate_config():
    
    if len(sys.argv) != 3:
        print("Usage: {} start end".format(sys.argv[0]))
        print("Example: {} 3501 3600".format(sys.argv[0]))
        exit(1)

    start = sys.argv[1]
    end = sys.argv[2]

    for i in range(int(start), int(end) + 1):
#    	print("run show evpn mac-ip-table instance evpn_l3_aa_{:d} | match 10".format(i))
#    	print("run show mac-vrf forwarding instance evpn_l3_aa_{:d} | match 10".format(i))
#        print("run show evpn mac-table instance evpn_elan_aa_{:d}".format(i))
        print("set groups EVPN-ELAN routing-instances evpn_elan_aa_{:d} protocols evpn interface ae29.{:d} interface-mac-limit 5000".format(i,i))

# execute
if __name__ == "__main__":
    generate_config()
else:
    pass