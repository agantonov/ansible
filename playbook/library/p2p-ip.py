#!/usr/bin/python3

import yaml
import sys
import ipaddress as ip
import array as ar
import os
import glob

def generate_config():
    
    if len(sys.argv) != 2:
        print("Usage: {} file_name".format(sys.argv[0]))
        print("Example: {} interconnect.yaml".format(sys.argv[0]))
        exit(1)

    file = sys.argv[1]

    with open(file, 'r') as f:
       input_data = yaml.safe_load(f)

    ipv4 = input_data['ipv4_base']
    ipv6 = input_data['ipv6_base']

    output_data = []

    for i in input_data['interlink']:
        ipv4 = str(ip.IPv4Address(ipv4) + 1)
        ipv6 = str(ip.IPv6Address(ipv6) + 1)
        output_data.append([i['router1'], i['iface1'], ipv4 + '/31', ipv6 + '/127', 'to_' + i['router2'] + '_' + i['iface2']])

        ipv4 = str(ip.IPv4Address(ipv4) + 1)
        ipv6 = str(ip.IPv6Address(ipv6) + 1)
        output_data.append([i['router2'], i['iface2'], ipv4 + '/31', ipv6 + '/127', 'to_' + i['router1'] + '_' + i['iface1']])

    f.close()

#    print("current working directory {}".format(os.getcwd()))
    files = glob.glob('playbook/tmp/p2p/*.conf')
    
    for i in files:
        os.remove(i)

    for i in output_data:
        with open('playbook/tmp/p2p/' + i[0] + '.conf', 'a') as f:
            f.write('set interfaces {} description {}\n'.format(i[1],i[4]))
            f.write('set interfaces {} unit 0 family inet address {}\n'.format(i[1],i[2]))
            f.write('set interfaces {} unit 0 family inet6 address {}\n'.format(i[1],i[3]))

# execute
if __name__ == "__main__":
    generate_config()
else:
    pass
