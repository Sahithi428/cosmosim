import socket
import struct
import time
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'network_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Port scan detection memory: { source_ip: set(destination_ports) }
connection_tracker = {}
SCAN_THRESHOLD = 8  # Flag IP if it hits > 8 distinct ports in a session

def parse_ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return socket.htons(proto), data[14:]

def format_mac(bytes_addr):
    return ':'.join(map('{:02x}'.format, bytes_addr))

def parse_ip_header(data):
    version_header_length = data[0]
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return proto, socket.inet_ntoa(src), socket.inet_ntoa(target), data[header_length:]

def parse_tcp_segment(data):
    src_port, dest_port, sequence, acknowledgment, offset_reserved_flags = struct.unpack('! H H L L H', data[:16])
    return src_port, dest_port

def packet_sniffer():
    # Works on Linux/Mac (ETH_P_ALL = 0x0003). On Windows, use socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP
    try:
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    except AttributeError:
        # Windows Fallback
        conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        conn.bind((socket.gethostbyname(socket.gethostname()), 0))
        conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    while True:
        raw_data, _ = conn.recvfrom(65535)
        eth_proto, ip_data = parse_ethernet_frame(raw_data)

        if eth_proto == 8: # IPv4
            proto, src_ip, dest_ip, transport_data = parse_ip_header(ip_data)
            src_port, dest_port = None, None
            alert = False

            if proto == 6: # TCP
                src_port, dest_port = parse_tcp_segment(transport_data)
                
                # Heuristic Port Scan Detection
                if src_ip not in connection_tracker:
                    connection_tracker[src_ip] = set()
                connection_tracker[src_ip].add(dest_port)

                if len(connection_tracker[src_ip]) > SCAN_THRESHOLD:
                    alert = True

            packet_payload = {
                "timestamp": time.strftime("%H:%M:%S"),
                "src_ip": src_ip,
                "dest_ip": dest_ip,
                "protocol": "TCP" if proto == 6 else ("UDP" if proto == 17 else "OTHER"),
                "dest_port": dest_port if dest_port else "N/A",
                "alert": alert
            }
            
            # Emit live log to connected WebSocket client
            socketio.emit('new_packet', packet_payload)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Start packet sniffer in a background thread via SocketIO
    socketio.start_background_task(target=packet_sniffer)
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)