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
    
    if len(sys.argv) != 10:
        print("Usage: {} router_id interface esi_base address_base_v4 address_base_v6 step site_id vlan_id_start vlan_id_end".format(sys.argv[0]))
        print("Example: {} 1.1.0.7 ae17 00:17:00:00:00:00:00:00:01:00 19.0.0.1 2001:19::1 1 12 100 200".format(sys.argv[0]))
        exit(1)

    group = "L3VPN"
    router_id = sys.argv[1]
    interface = sys.argv[2]
    esi = esi_to_int(sys.argv[3])
    address_v4 = int(ipaddress.ip_address(sys.argv[4]))
    address_v6 = int(ipaddress.IPv6Address(sys.argv[5]))
    step = int(sys.argv[6])
    site_id = int(sys.argv[7])
    vlan_start = sys.argv[8]
    vlan_end = sys.argv[9]

    rt_prefix = 30000

    print("delete groups {}".format(group))

    for i in range(int(vlan_start), int(vlan_end) + 1):
        print("set groups {} routing-instances l3vpn_irb_{:d} instance-type vrf".format(group,i))
        print("set groups {} routing-instances l3vpn_irb_{:d} routing-options auto-export".format(group,i))
        print("set groups {} routing-instances l3vpn_irb_{:d} routing-options router-id {}".format(group,i,router_id))
        print("set groups {} routing-instances l3vpn_irb_{:d} routing-options multipath".format(group,i))
        print("set groups {} routing-instances l3vpn_irb_{:d} routing-options protect core".format(group,i))
        print("set groups {} routing-instances l3vpn_irb_{:d} routing-options rib l3vpn_irb_{:d}.inet6.0 multipath".format(group,i,i))
        print("set groups {} routing-instances l3vpn_irb_{:d} routing-options rib l3vpn_irb_{:d}.inet6.0 protect core".format(group,i,i))
        print("set groups {} routing-instances l3vpn_irb_{:d} route-distinguisher {}:{:d}{:d}".format(group,i,router_id,round(rt_prefix/10000),i))
        print("set groups {} routing-instances l3vpn_irb_{:d} vrf-target target:65100:{:d}{:d}".format(group,i,rt_prefix,i))
        print("set groups {} routing-instances l3vpn_irb_{:d} interface irb.{:d}".format(group,i,i))
        print("set groups {} routing-instances l3vpn_irb_{:d} vrf-table-label".format(group,i))

        print("set groups {} routing-instances evpn_irb_{:d} instance-type evpn".format(group,i))
        print("set groups {} routing-instances evpn_irb_{:d} protocols evpn".format(group,i))
        print("set groups {} routing-instances evpn_irb_{:d} vlan-id none".format(group,i))
        print("set groups {} routing-instances evpn_irb_{:d} no-normalization".format(group,i))
        print("set groups {} routing-instances evpn_irb_{:d} route-distinguisher {}:{:d}{:d}".format(group,i,router_id,round(rt_prefix/10000) + 1,i))
        print("set groups {} routing-instances evpn_irb_{:d} vrf-target target:65100:{:d}{:d}".format(group,i,rt_prefix + site_id,i))
        print("set groups {} routing-instances evpn_irb_{:d} interface {}.{:d}".format(group,i,interface,i))
        print("set groups {} routing-instances evpn_irb_{:d} routing-interface irb.{:d}".format(group,i,i))

        print("set groups {} interfaces {} unit {:d} encapsulation vlan-bridge".format(group,interface,i))
        print("set groups {} interfaces {} unit {:d} vlan-id {:d}".format(group,interface,i,i))
        print("set groups {} interfaces {} unit {:d} input-vlan-map pop".format(group,interface,i))
        print("set groups {} interfaces {} unit {:d} output-vlan-map push".format(group,interface,i))

#       ESI per IFL  
#        print("set groups {} interfaces {} unit {:d} esi all-active".format(group,interface,i))
#        print("set groups {} interfaces {} unit {:d} esi {}".format(group,interface,i,esi_from_int(esi)))
#        esi = esi + 1

        print("set groups {} interfaces irb unit {:d} virtual-gateway-accept-data".format(group,i))
        print("set groups {} interfaces irb unit {:d} interface-state local".format(group,i))
        print("set groups {} interfaces irb unit {:d} family inet address {}/24 virtual-gateway-address {}".\
            format(group,i,str(ipaddress.ip_address(address_v4 + step)),str(ipaddress.ip_address(address_v4))))
        address_v4 = address_v4 + 256
        print("set groups {} interfaces irb unit {:d} family inet6 address {}/64 virtual-gateway-address {}".\
            format(group,i,str(ipaddress.IPv6Address(address_v6 + step)),str(ipaddress.IPv6Address(address_v6))))
#        address_v6 = address_v6 + 65536

    print("set apply-groups {}".format(group))

# execute
if __name__ == "__main__":
    generate_config()
else:
    pass