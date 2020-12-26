import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help=" -i or --interface to select interface")
    parser.add_option("-m", "--mac", dest="mac", help=" -m or --mac to change mac")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] please specify an interface use --help for more info")
    elif not options.mac:
        parser.error("[-] please specify a mac use --help for more info")
    return options


def mac_changer(interface, mac):
    print("[*] Changing mac address for " + interface + " to " + mac)
    subprocess.call(["ifconfig", interface, "down", ])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac, ])
    subprocess.call(["ifconfig", interface, "up", ])
    print("[*] MAC address changed for " + interface)


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("[-]Current MAC = " + str(current_mac))

mac_changer(options.interface, options.mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.mac:
    print("[*] MAC address was changed.")
else:
    print("[-] MAC address did not changed.:-(")