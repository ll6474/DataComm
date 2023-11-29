"""
Author: Lu Li
Email: ll6474@g.rit.edu
"""


def processRTTB(rtgTable,destination_ip):
    """
    This function process the
    :param rtgTable: Processed routing table
    :param destination_ip: destination ip address
    :return:
    """

    if not checkValidInput(destination_ip):
        print("Invalid IP address. Please enter a valid IP.")
        return

    destination_ip_int = list(map(int,destination_ip.split('.')))

    for i, entries in enumerate(rtgTable,start=1):
        network,netmask,gateway,interface = entries
        network_parts = list(map(int,network.split('.')))
        netmask_parts = list(map(int,netmask.split('.')))

        print(f'Processing entry {i} : {[entries]}')

        result_table = []
        result_input = []
        for j in range(len(destination_ip_int)):
            table_and = network_parts[j] & netmask_parts[j]
            table_result = convertToBinary(table_and)
            result_table.append(table_result)
            destination_and = destination_ip_int[j] & netmask_parts[j]
            destination_result = convertToBinary(destination_and)
            result_input.append(destination_result)
        print(f"ANDing result of network and mask from table: {result_table}")
        print(f"ANDing result of input destination and mask: {result_input}")

        match = all((network_parts[i] & netmask_parts[i]) == (destination_ip_int[i] & netmask_parts[i]) for i in range(4))


        if match:
            print(f'Entry Found: {i} : {[entries]}')
            print(f"Gateway: {gateway}, Interface: {interface}")

            if destination_ip == gateway:
                print("ARP for the destination IP address.")
            elif gateway == '0.0.0.0':
                print("ARP for the default gateway")
            else:
                print("No APR needed")

            return
    print("No matching entry found in the routing table.")


def checkValidInput(destination_ip):
    """
    This function checks for a valid user input ip address
    :param destination_ip: user input
    :return: true/false
    """
    try:
        ips = list(map(int,destination_ip.split('.')))
        return len(ips) == 4 and all(0 <= part <= 255 for part in ips)
    except ValueError:
        return False


def convertToBinary(ip):
    """
    Converts the ip address to binary
    :param ip: ip address
    :return: binary
    """
    return "{0:b}".format(int(ip))


def op_file(filenames):
    """
    Parse the ip address from the file and store them as a list in reversed order
    :param filenames: routing table file name
    :return: lists stored the host table ip address
    """

    try:
        f = open(filenames)
        lines = reversed(f.readlines())
        data = []

        for line in lines:
            dt = line.strip().split(',')
            data.append(dt)
        return data
    except FileNotFoundError:
        print("File not found. Please enter a valid file name.")
        return None


def main():
    filename = "routing_table.txt"
    routing_table = op_file(filename)

    if routing_table:
        while True:
            des_ip = input("Please enter destination IP address or quit to exit: ")

            if des_ip.lower() == 'quit':
                break

            processRTTB(routing_table, des_ip)


if __name__ == '__main__':
    main()

