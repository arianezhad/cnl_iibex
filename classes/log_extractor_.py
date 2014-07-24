__author__ = 'Aria'
import linecache


class Parent(object):

    def __init__(self, file_name, text, path, conn, db, header_db, field_db, template_no):
        self.file_name = file_name
        self.text = text
        self.path = path
        self.conn = conn
        self.db = db
        self.header_db = header_db
        self.field_db = field_db
        self.template_no = template_no
        self.headers_id = None

    def insert_headers(self):
        log_headers = {
            'local_beacon': self.file_name[0],
            'remote_beacon': self.file_name[1],
            'experiment': self.file_name[2],
            'run': self.file_name[3],
            'time_stamp': self.file_name[4],
            'tr_mode': self.file_name[5],
            'mode_no': self.file_name[6],
            'protocol': self.file_name[7],
            }

        self.headers_id = self.header_db.insert(log_headers)
        print('HEADERS ARE ARE ARE:', self.headers_id)
        #return self.headers_id

    def extract_fields(self):
        for i in range(1, self.text.count('\n') + 1):
            fields_line = linecache.getline(self.path, i)
            if ',' in fields_line and fields_line[0].isdigit() and len(fields_line) > 8:
                fields_list = fields_line.split(',')
                Parent.log_select(self, fields_list, self.headers_id)

    def log_select(self, log_fields, id_headers):
        if self.template_no == 'UDPR':
            UDPReceive.insert_db(self, log_fields, id_headers)
        if self.template_no == 'UDPT':
            UDPTransmit.insert_db(self, log_fields, id_headers)
        if self.template_no == 'TCPR':
            TCPReceive.insert_db(self, log_fields, id_headers)
        if self.template_no == 'RAWR':
            RAWReceive.insert_db(self, log_fields, id_headers)


class UDPReceive(Parent):
    print('THIS IS THE UDPReceive CHILD OBJECT')

    def insert_db(self, f, h):
        print('HEADERS ARE:', h)
        fields_udpr = {
            'packet_number': f[0],
            'rx_sequence_number': f[1],
            'tx_timestamp': f[2],
            'rx_timestamp': f[3],
            'rx_ttl': f[4],
            'rx_size': f[5],
            'Seen_by_raw_socket': f[6],
            'seen_by_protocol_socket': f[7],
            'header_id': h
        }

        print('FIELDS ARE:', fields_udpr)
        fields_id = self.field_db.insert(fields_udpr)


class UDPTransmit(Parent):
    print('THIS IS THE UDPReceive CHILD OBJECT')

    def insert_db(self, f, h):
        print('HEADERS ARE:', h)

        fields_udpt = {
            'packet_number': f[0],
            'bytes': f[1],
            'tx_timestamp_1': f[2],
            'TX timestamp 2': f[3],
            'loop_iterations': f[4],
            'header_id': h
        }

        print('FIELDS ARE:', fields_udpt)

        fields_id = self.field_db.insert(fields_udpt)


class TCPReceive(Parent):
    print('THIS IS THE UDPReceive CHILD OBJECT')

    def insert_db(self, f, h):
        print('HEADERS ARE:', h)

        fields_tcpr = {
            'rx_sequence_number': f[0],
            'rx_timestamp': f[1],
            'rx_size': f[2],
            'header_id': h
            }

        print('FIELDS ARE:', fields_tcpr)

        fields_id = self.field_db.insert(fields_tcpr)


class RAWReceive(Parent):
    print('THIS IS THE UDPReceive CHILD OBJECT')

    def insert_db(self, f, h):
        print('HEADERS ARE:', h)

        fields_rawr = {
            'rx_sequence_number': f[0],
            'rx_timestamp': f[1],
            'rx_size': f[2],
            'header_id': h
            }

        print('FIELDS ARE:', fields_rawr)

        fields_id = self.field_db.insert(fields_rawr)
# class UDPTransmit(Parent):
#     print('THIS IS THE UDPTransmit CHILD')
#
#     def insert_db(self, f, h):
#         log_udpt = {
#             'local_beacon': h[0],
#             'remote_beacon': h[1],
#             'experiment': h[2],
#             'run': h[3],
#             'time_stamp': h[4],
#             'tr_mode': h[5],
#             'mode_no': h[6],
#             'protocol': h[7],
#             'packet_number': f[0],
#             'bytes': f[1],
#             'tx_timestamp_1': f[2],
#             'TX timestamp 2': f[3],
#             'loop_iterations': f[4]
#         }
#         logs_id = self.logs_db.insert(log_udpt)
#         print(self.logs_db.find_one(), '\n', logs_id, '\n\n')
#
#
# class TCPReceive(Parent):
#     print('THIS IS THE TCPReceive CHILD')
#
#     def insert_db(self, f, h):
#         log_tcpr = {
#             'local_beacon': h[0],
#             'remote_beacon': h[1],
#             'experiment': h[2],
#             'run': h[3],
#             'time_stamp': h[4],
#             'tr_mode': h[5],
#             'mode_no': h[6],
#             'protocol': h[7],
#             'rx_sequence_number': f[0],
#             'rx_timestamp': f[1],
#             'rx_size': f[2],
#             }
#         logs_id = self.logs_db.insert(log_tcpr)
#         print(self.logs_db.find_one(), '\n', logs_id, '\n\n')
#
#
# class RAWReceive(Parent):
#     print('THIS IS THE RAWReceive CHILD')
#
#     def insert_db(self, f, h):
#         log_rawr = {
#             'local_beacon': h[0],
#             'remote_beacon': h[1],
#             'experiment': h[2],
#             'run': h[3],
#             'time_stamp': h[4],
#             'tr_mode': h[5],
#             'mode_no': h[6],
#             'protocol': h[7],
#             'rx_sequence_number': f[0],
#             'rx_timestamp': f[1],
#             'rx_size': f[2],
#             'ttl': f[3],
#             }
#         logs_id = self.logs_db.insert(log_rawr)
#         print(self.logs_db.find_one(), '\n', logs_id, '\n\n')


