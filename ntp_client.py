import socket
import struct
import time
import logging

log_file = "ntp_client.log"
logging.basicConfig(filename = log_file, level=logging.INFO, format='%(asctime)s.%(msecs)03d - %(message)s', 
                            datefmt='%Y-%m-%d %H:%M:%S')

def get_ntp_data_packet():
    leap_indicator = 0
    version = 4
    mode = 3
    stratum = 0
    poll = 0
    precision = 0
    root_delay = 0
    root_dispersion = 0
    reference_identifier = 0
    reference_timestamp = 0
    originate_timestamp = int(time.time()) + 2208988800
    receive_timestamp = 0
    transmit_timestamp = 0

    packet = struct.pack("!BBBbIIIQQQQ", leap_indicator << 6 | version << 3 | mode, stratum,
                            poll, precision, root_delay, root_dispersion, reference_identifier, 
                             reference_timestamp, originate_timestamp, receive_timestamp, transmit_timestamp)

    return packet

def ntp_client(server_address, port):
    print(f"Server Address: {server_address}")
    print(f"Port: {port}")
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # message = '\x1b' + 47 * '\0'
    send_packet = get_ntp_data_packet()
    try:
        # client.sendto(message.encode('utf-8'), (server_address, port))
        client.sendto(send_packet, (server_address, port))
        client.settimeout(5.0) #value in seconds
        try:
            data, _ = client.recvfrom(1024)
            client_receive_time = int(time.time()) + 2208988800
            if data:
                # unpacked_data = struct.unpack('!12I', data)
                # transmit_timestamp = unpacked_data[10] - 2208988800  # Convert from NTP epoch
                _, _, _, _, _, _, _, reference_timestamp, originate_timestamp, receive_timestamp, transmit_timestamp = struct.unpack("!BBBbIIIQQQQ", data)
                logging.info(f"Originate Timestamp (T1): {originate_timestamp}")
                logging.info(f"Receive Timestamp (T2): {receive_timestamp}")
                logging.info(f"Transmit Timestamp (T3): {transmit_timestamp}")
                logging.info(f"Destination Timestamp (T4): {client_receive_time}")
                # print(f"Server time: {time.ctime(transmit_timestamp)}")
                # local_time = time.time()
                # print(f"Local time : {time.ctime(local_time)}")
            else:
                print("Failed to receive the data from server")
        except socket.timeout:
            logging.error("Request timed out")
    except Exception as e:
        print("Client error:", e)
    finally:
        client.close()

if __name__ == "__main__":
    ntp_client('pool.ntp.org', 123)


