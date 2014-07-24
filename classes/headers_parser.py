__author__ = 'Aria'
import linecache


class UDPReceive:
    def __init__(self, text, path, conn, db, headers_db, fields_db):
        self.headers = ['Experiment:',
                        'Run:',
                        'Local beacon:',
                        'Local beacon hostname:',
                        'Local IP:',
                        'Local beacon software version:',
                        'Configured local port:',
                        'Remote beacon:',
                        'Remote IP:',
                        'Configured remote port:',
                        'Actual remote port observed on last packet:',
                        'Start:',
                        'Mode:',
                        'Socket listening time (seconds):',
                        'Packets received:'
        ]
        self.text = text
        self.path = path
        self.conn = conn
        self.db = db
        self.headers_db = headers_db
        self.fields_db = fields_db
        self.headers_len = len(self.headers)
        self.a_header_len = None
        self.position = None
        self.header_holder = []
        self.s = None
        self.line = None
        self.line_no = None
        self.a_line = None
        self.field_value = None
        self.field_line = None
        self.min_line_len = 8
        self.field = None
        self.fields_id = None

    def header_extractor(self):
        for i in range(0, self.headers_len):
            self.position = self.text.index(self.headers[i])
            self.a_header_len = len(self.headers[i])
            self.line_no = self.text.count("\n", 0, self.position + self.a_header_len)+1
            self.line = linecache.getline(self.path, self.line_no)
            self.s = self.line.split(self.headers[i], 1)
            self.header_holder.append(str(self.s[1][1:].replace('\n', '')))
        UDPReceive.insert_headers(self)
        UDPReceive.field_extractor(self)

    def insert_headers(self):
        header = {'experiment': self.header_holder[0],
                  'run': self.header_holder[1],
                  'local_beacon': self.header_holder[2],
                  'local_beacon_hostname': self.header_holder[3],
                  'local_IP':self.header_holder[4],
                  'software_ver': self.header_holder[5],
                  'configured_local_port': self.header_holder[6],
                  'remote_beacon': self.header_holder[7],
                  'remote_IP': self.header_holder[8],
                  'configured_remote_port': self.header_holder[9],
                  'actual_remote_port_observed': self.header_holder[10],
                  'start': self.header_holder[11],
                  'mode': self.header_holder[12],
                  'socket_listening_time': self.header_holder[13],
                  'packets_received': self.header_holder[14]
        }
        headers_id = self.headers_db.insert(header)
        print('headers are:', '\n', self.headers_db.find_one(), '\n', 'Header ID:', headers_id, '\n\n')

    def field_extractor(self):
        for i in range(1, self.text.count("\n")):
            self.field_line = linecache.getline(self.path, i)
            if len(self.field_line) > self.min_line_len and self.field_line[0].isdigit():
                self.field_value = self.field_line.split(',')
                #print(self.field_value)
                UDPReceive.insert_fields(self)
        for self.field in self.fields_db.find():
            print(self.field)

    def insert_fields(self):
        self.field = {'packet_number': self.field_value[0],
                 'rx_sequence_number': self.field_value[1],
                  'tx_timestamp': self.field_value[2],
                  'rx_timestamp': self.field_value[3],
                  'rx_ttl': self.field_value[4],
                  'rx_size': self.field_value[5],
                  'Seen_by_raw_socket': self.field_value[6],
                  'seen_by_protocol_socket': self.field_value[7]
    }
        self.fields_id = self.fields_db.insert(self.field)
        print('\n', self.fields_id)


class UDPTransmit:
    def __init__(self, text, path, conn, db, headers_db, fields_db):
        self.headers = ['Experiment:',
                        'Run:',
                        'Local beacon:',
                        'Local beacon hostname:',
                        'Local IP:',
                        'Local port:',
                        'Local beacon software version:',
                        'Remote beacon:',
                        'Remote IP:',
                        'Remote port:',
                        'Start:',
                        'Mode:',
                        'Socket timeout',
                        'Stuffing file used:',
                        'Nominal intertransmission time:',
                        'Number of packets transmitted:',
                        'UDP payload size:'
        ]
        self.text = text
        self.path = path
        self.conn = conn
        self.db = db
        self.headers_db = headers_db
        self.fields_db = fields_db
        self.headers_len = len(self.headers)
        self.a_header_len = None
        self.position = None
        self.header_holder = []
        self.s = None
        self.line = None
        self.line_no = None
        self.a_line = None
        self.field_value = None
        self.field_line = None
        self.min_line_len = 8

    def header_extractor(self):
        for i in range(0, self.headers_len):
            self.position = self.text.index(self.headers[i])
            self.a_header_len = len(self.headers[i])
            self.line_no = self.text.count("\n", 0, self.position + self.a_header_len)+1
            self.line = linecache.getline(self.path, self.line_no)
            self.s = self.line.split(self.headers[i], 1)
            self.header_holder.append(str(self.s[1][1:].replace('\n', '')))
        UDPTransmit.insert_headers(self)
        UDPTransmit.field_extractor(self)

    def insert_headers(self):
        header = {'experiment': self.header_holder[0],
                  'run': self.header_holder[1],
                  'local_beacon': self.header_holder[2],
                  'local_beacon_hostname': self.header_holder[3],
                  'local_IP':self.header_holder[4],
                  'local_port':self.header_holder[5],
                  'software_ver': self.header_holder[6],
                  'remote_beacon': self.header_holder[7],
                  'remote_IP': self.header_holder[8],
                  'remote_port': self.header_holder[9],
                  'start': self.header_holder[10],
                  'mode': self.header_holder[11],
                  'socket_timeout': self.header_holder[12],
                  'stuffing_file': self.header_holder[13],
                  'nominal_intertransmission_time': self.header_holder[14],
                  'number_packets_transmitted': self.header_holder[15],
                  'UDP_payload_size:': self.header_holder[16]
        }
        headers_id = self.headers_db.insert(header)
        print('headers are:', '\n', self.headers_db.find_one(), '\n', 'Header ID:', headers_id, '\n\n')

    def field_extractor(self):
        for i in range(1, self.text.count("\n")):
            self.field_line = linecache.getline(self.path, i)
            if len(self.field_line) > self.min_line_len and self.field_line[0].isdigit():
                self.field_value = self.field_line.split(',')
                #print(self.field_value)
                UDPTransmit.insert_fields(self)
        for self.field in self.fields_db.find():
            print(self.field)

    def insert_fields(self):
        self.field = {'packet_number': self.field_value[0],
                  'bytes': self.field_value[1],
                  'tx_timestamp_1': self.field_value[2],
                  'TX timestamp 2': self.field_value[3],
                  'loop_iterations': self.field_value[4]
    }
        self.fields_id = self.fields_db.insert(self.field)
        print('\n', self.fields_id)


class TCPReceive:
    def __init__(self, text, path, conn, db, headers_db, fields_db):
        self.headers = ['Experiment:',
                        'Run:',
                        'Local beacon:',
                        'Local beacon hostname:',
                        'Local IP:',
                        'Local port:',
                        'Local beacon software version:',
                        'Remote beacon:',
                        'Remote IP:',
                        'Configured remote port:',
                        'Actual remote port:',
                        'Start:',
                        'Mode:',
                        'Socket listening time',
                        'Packets received:'
        ]
        self.text = text
        self.path = path
        self.conn = conn
        self.db = db
        self.headers_db = headers_db
        self.fields_db = fields_db
        self.headers_len = len(self.headers)
        self.a_header_len = None
        self.position = None
        self.header_holder = []
        self.s = None
        self.line = None
        self.line_no = None
        self.a_line = None
        self.field_value = None
        self.field_line = None
        self.min_line_len = 8

    def header_extractor(self):
        for i in range(0, self.headers_len):
            self.position = self.text.index(self.headers[i])
            self.a_header_len = len(self.headers[i])
            self.line_no = self.text.count("\n", 0, self.position + self.a_header_len)+1
            self.line = linecache.getline(self.path, self.line_no)
            self.s = self.line.split(self.headers[i], 1)
            self.header_holder.append(str(self.s[1][1:].replace('\n', '')))
        TCPReceive.insert_headers(self)
        TCPReceive.field_extractor(self)

    def insert_headers(self):
        header = {'experiment': self.header_holder[0],
                  'run': self.header_holder[1],
                  'local_beacon': self.header_holder[2],
                  'local_beacon_hostname': self.header_holder[3],
                  'local_IP':self.header_holder[4],
                  'local_port':self.header_holder[5],
                  'software_ver': self.header_holder[6],
                  'remote_beacon': self.header_holder[7],
                  'remote_IP': self.header_holder[8],
                  'configured_remote_port': self.header_holder[9],
                  'actual_remote_port': self.header_holder[10],
                  'start': self.header_holder[11],
                  'mode': self.header_holder[12],
                  'socket_listening_time': self.header_holder[13],
                  'packets_received': self.header_holder[14]
        }
        headers_id = self.headers_db.insert(header)
        print('headers are:', '\n', self.headers_db.find_one(), '\n', 'Header ID:', headers_id, '\n\n')

    def field_extractor(self):
        for i in range(1, self.text.count("\n")):
            self.field_line = linecache.getline(self.path, i)
            if len(self.field_line) > self.min_line_len and self.field_line[0].isdigit():
                self.field_value = self.field_line.split(',')
                #print(self.field_value)
                TCPReceive.insert_fields(self)
        for self.field in self.fields_db.find():
            print(self.field)

    def insert_fields(self):
        self.field = {'rx_sequence_number': self.field_value[0],
                  'rX_timestamp': self.field_value[1],
                  'rx_size': self.field_value[2]
    }
        self.fields_id = self.fields_db.insert(self.field)
        print('\n', self.fields_id)


class RAWReceive:
    def __init__(self, text, path, conn, db, headers_db, fields_db):
        self.headers = ['Experiment:',
                        'Run:',
                        'Local beacon:',
                        'Local beacon hostname:',
                        'Local IP:',
                        'Local port:',
                        'Local beacon software version:',
                        'Remote beacon:',
                        'Remote IP:',
                        'Configured remote port:',
                        'Actual remote port:',
                        'TCP rate mode:',
                        'Start:',
                        'Mode:',
                        'Socket listening time',
                        'Packets received:'
        ]
        self.text = text
        self.path = path
        self.conn = conn
        self.db = db
        self.headers_db = headers_db
        self.fields_db = fields_db
        self.headers_len = len(self.headers)
        self.a_header_len = None
        self.position = None
        self.header_holder = []
        self.s = None
        self.line = None
        self.line_no = None
        self.a_line = None
        self.field_value = None
        self.field_line = None
        self.min_line_len = 8

    def header_extractor(self):
        for i in range(0, self.headers_len):
            self.position = self.text.index(self.headers[i])
            self.a_header_len = len(self.headers[i])
            self.line_no = self.text.count("\n", 0, self.position + self.a_header_len)+1
            self.line = linecache.getline(self.path, self.line_no)
            self.s = self.line.split(self.headers[i], 1)
            self.header_holder.append(str(self.s[1][1:].replace('\n', '')))
        RAWReceive.insert_headers(self)
        RAWReceive.field_extractor(self)

    def insert_headers(self):
        header = {'experiment': self.header_holder[0],
                  'run': self.header_holder[1],
                  'local_beacon': self.header_holder[2],
                  'local_beacon_hostname': self.header_holder[3],
                  'local_IP': self.header_holder[4],
                  'local_port': self.header_holder[5],
                  'software_ver': self.header_holder[6],
                  'remote_beacon': self.header_holder[7],
                  'remote_IP': self.header_holder[8],
                  'configured_remote_port': self.header_holder[9],
                  'actual_remote_port': self.header_holder[10],
                  'tcp_rate_mode': self.header_holder[11],
                  'start': self.header_holder[12],
                  'mode': self.header_holder[13],
                  'socket_listening_time': self.header_holder[14],
                  'packets_received': self.header_holder[15]
        }
        headers_id = self.headers_db.insert(header)
        print('headers are:', '\n', self.headers_db.find_one(), '\n', 'Header ID:', headers_id, '\n\n')

    def field_extractor(self):
        for i in range(1, self.text.count("\n")):
            self.field_line = linecache.getline(self.path, i)
            if len(self.field_line) > self.min_line_len and self.field_line[0].isdigit():
                self.field_value = self.field_line.split(',')
                #print(self.field_value)
                RAWReceive.insert_fields(self)
        for self.field in self.fields_db.find():
            print(self.field)

    def insert_fields(self):
        self.field = {'rx_sequence_number': self.field_value[0],
                  'rX_timestamp': self.field_value[1],
                  'rx_size': self.field_value[2],
                  'ttl': self.field_value[3]
    }
        self.fields_id = self.fields_db.insert(self.field)
        print('\n', self.fields_id)
