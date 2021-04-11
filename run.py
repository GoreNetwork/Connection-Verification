from functions import *
from pprint import pprint
import socket
from ipaddress import ip_address, ip_network
import ssl


port_groups_file = 'port_groups.yml'
server_groups_file = 'server_groups.yml'
connection_rules_file = 'connection_rules.yml'
port_map_file = 'port_map.yml'

this_host_tmp = socket.gethostbyname_ex(socket.gethostname())[-1]
this_host = []
for ip in this_host_tmp:
    this_host.append(ip_address(ip))

this_host.append(socket.gethostname())

connection_rules = read_in_yaml_file(connection_rules_file)
server_groups = read_in_yaml_file(server_groups_file)
port_groups = read_in_yaml_file(port_groups_file)
port_map = read_in_yaml_file(port_map_file)


def determine_if_dns_ip_subnet(item):
    item_data = {}
    # Hopefully it never runs into www.192.168.0.1.com or something like that
    if len(get_ip(item)) == 0:
        item_data['item'] = item
        item_data['type'] = 'dns'
        return item_data
    if '/' in item:
        item_data['item'] = ip_network(item)
        item_data['type'] = 'network'
        return item_data
    else:
        item_data['item'] = ip_address(item)
        item_data['type'] = 'ip_address'
        return item_data


def determine_if_host_is_in_group(this_host, item_data):
    if item_data['type'] == 'dns' or item_data['type'] == 'ip_address':
        for each in this_host:
            if each == item_data['item']:
                return True
    if item_data['type'] == 'network':
        for each in this_host:
            if each in item_data['item']:
                return True
    return False


def create_server_groups_info_dict(connection_rules, server_groups, port_groups, this_host):
    groups_this_server_is_in = []
    final_server_groups = {}
    for server_group_name, group_list in server_groups.items():
        final_server_groups[server_group_name] = []
        for group_name in server_groups:
            if group_name in group_list:
                print("Found a group in group, which currently isn't supported")
        for item in group_list:
            item_data = determine_if_dns_ip_subnet(item)
            if determine_if_host_is_in_group(this_host, item_data) == True:
                groups_this_server_is_in.append(server_group_name)
            final_server_groups[server_group_name].append(item_data)

    return [final_server_groups, groups_this_server_is_in]


def expand_out_port_range(port_range):
    port_range = port_range.replace(' ', '')
    start, end = port_range.split('-')
    start = int(start)
    end = int(end)
    end = end+1
    ports = range(start, end)
    port_list = [port for port in ports]
    return port_list


def expand_port_map(port_map):
    final_map = {}
    for key, value in port_map.items():
        final_map[key] = []
        if type(value) == int:
            final_map[key].append(value)
        if type(value) == list:
            final_map[key] = value
        if type(value) == str:
            final_map[key] = expand_out_port_range(value)
    return final_map


def expand_port_groups(port_groups, port_map):
    final_map = {}
    for key, port_list in port_groups.items():
        final_map[key] = []
        for list_item in port_list:
            if type(list_item) == int:
                final_map[key].append(list_item)
            else:
                for port in port_map[list_item]:
                    final_map[key].append(port)
    return final_map


def build_connection_rules(connection_rules, groups_this_server_is_in, server_groups):
    all_connections = []
    for key, connections in connection_rules.items():
        for connection in connections:
            # pprint(connection)
            if connection['source'] not in groups_this_server_is_in:
                continue
            connection_data = {
                'servers': server_groups[connection['dest']],
                'ports': port_groups[connection['ports']]
            }
            all_connections.append(connection_data)
    return all_connections


# def config_ssl():
#     sslContext = ssl.SSLContext()
#     clientSocket = socket.socket()
#     secureClientSocket = sslContext.wrap_socket(
#         clientSocket, do_handshake_on_connect=True)
#     secureClientSocket.settimeout(2)
#     return secureClientSocket


def test_handshake(tmp_list):
    # secureClientSocket = config_ssl()
    site = tmp_list[0]
    port = tmp_list[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    # pprint(dir(s))
    try:
        s.connect((site, port))
        print("Success:  ", tmp_list)
    except:
        print("Failed:   ", tmp_list)
    # try:
    #     secureClientSocket.connect((site, port))
    #     secureClientSocket.close()
    #     print("Success: ", tmp_list)
    # except:
    #     print('failed: ', tmp_list)
    # secureClientSocket.connect((site, port))
    # secureClientSocket.close()


def check_connections(all_connections):
    # secureClientSocket = config_ssl()
    for connection in all_connections:
        for server in connection['servers']:
            server_to_check = server['item']
            for port in connection['ports']:
                check_list = [server_to_check, port]
                # pprint(check_list)
                test_handshake(check_list)


server_groups, groups_this_server_is_in = create_server_groups_info_dict(
    connection_rules, server_groups, port_groups, this_host)

# pprint(groups_this_server_is_in)

port_map = expand_port_map(port_map)

port_groups = expand_port_groups(port_groups, port_map)

all_connections = build_connection_rules(
    connection_rules, groups_this_server_is_in, server_groups)

check_connections(all_connections)
