#!/usr/bin/python3

import sys
import ipaddress
import math

import re

def __bytes(value, num_bytes):
    for i in reversed(range(num_bytes)):
        yield value >> (8 * i) & 255

def __addr_to_int(addr, base, delimiter):
    segments = list(reversed(addr.split(delimiter)))
    result = 0
    for i in range(len(segments)):
        result += int(segments[i], base=base) * 256 ** i
    return result

def __addr_from_int(value, num_bytes, delimiter, formatter=lambda x: str(x)):
    return delimiter.join(map(formatter, __bytes(value, num_bytes)))

def esi_to_int(esi):
    return __addr_to_int(esi, base=16, delimiter=':')

def esi_from_int(value):
    return __addr_from_int(value, delimiter=':', num_bytes=10,
            formatter=lambda x: '{:02x}'.format(x))

#def esi_to_int(esi):
#    return int(esi.replace(":", ""), 16)

#def int_to_esi(esiint):
#    return  ":".join(re.findall("..", "%020x"%esiint))


def generate_config():
    
    if len(sys.argv) != 9:
        print("Usage: {} router_id interface esi_base local_id remote_id site_id vlan_id_start vlan_id_end".format(sys.argv[0]))
        print("Example: {} 1.1.0.7 ae17 00:17:00:00:00:00:00:00:01:00 1 2 1 100 200".format(sys.argv[0]))
        exit(1)

    group = "EVPN-VPWS"
    router_id = sys.argv[1]
    interface = sys.argv[2]
#    esi = esi_to_int(sys.argv[3])
    esi = sys.argv[3]
    local_id = sys.argv[4]
    remote_id = sys.argv[5]
    site_id = int(sys.argv[6])
    vlan_start = sys.argv[7]
    vlan_end = sys.argv[8]

    rt_prefix = 10000

    print("delete groups {}".format(group))

# ESI Per IFD
#    print("set groups {} interfaces {} esi all-active".format(group,interface))
#    print("set groups {} interfaces {} esi {}".format(group,interface,esi))

    for i in range(int(vlan_start), int(vlan_end)+1):
        print("set groups {} routing-instances evpn_vpws_{:d} instance-type evpn-vpws".format(group,i))
        print("set groups {} routing-instances evpn_vpws_{:d} protocols evpn interface {}.{:d} vpws-service-id local {}".format(group,i,interface,i,local_id))
        print("set groups {} routing-instances evpn_vpws_{:d} protocols evpn interface {}.{:d} vpws-service-id remote {}".format(group,i,interface,i,remote_id))
        print("set groups {} routing-instances evpn_vpws_{:d} protocols evpn no-control-word".format(group,i))
        print("set groups {} routing-instances evpn_vpws_{:d} interface {}.{:d}".format(group,i,interface,i))
        print("set groups {} routing-instances evpn_vpws_{:d} route-distinguisher {}:{:d}{:d}".format(group,i,router_id,round(rt_prefix/10000),i))
        print("set groups {} routing-instances evpn_vpws_{:d} vrf-target target:65100:{:d}{:d}".format(group,i,rt_prefix + site_id,i))

        print("set groups {} interfaces {} unit {:d} encapsulation vlan-ccc".format(group,interface,i))
        print("set groups {} interfaces {} unit {:d} vlan-id {:d}".format(group,interface,i,i))
 
 #      ESI per IFL       
 #       print("set groups {} interfaces {} unit {:d} esi all-active".format(group,interface,i))       
 #       print("set groups {} interfaces {} unit {:d} esi {}".format(group,interface,i,esi_from_int(esi)))
 #       esi = esi + 1

    print("set apply-groups {}".format(group))

# execute
if __name__ == "__main__":
    generate_config()
else:
    pass