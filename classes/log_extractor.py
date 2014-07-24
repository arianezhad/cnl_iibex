__author__ = 'Aria'
import linecache


class Parent(object):

    def __init__(self, file_name, text, path, conn, db, headers_db, fields_db, template_no):
        self.file_name = file_name
        self.text = text
        self.path = path
        self.conn = conn
        self.db = db
        self.headers_db = headers_db
        self.fields_db = fields_db
        self.template_no = template_no

    def insert_headers(self):
        log_headers = {'local_beacon': self.file_name[0],
                       'remote_beacon': self.file_name[1],
                       'experiment': self.file_name[2],
                       'time_stamp': self.file_name[4],
                       'receive_mode': self.file_name[5],
                       'mode': self.file_name[6],
                       'protocol': self.file_name[7],
                       }
        log_headers_id = self.headers_db.insert(log_headers)
        print(self.headers_db.find_one(), '\n', log_headers_id, '\n\n')

    def extract_fields(self):
        for i in range(1, self.text.count('\n') + 1):
            fields_line = linecache.getline(self.path, i)
            if ',' in fields_line and fields_line[0].isdigit() and len(fields_line) > 8:
                fields_list = fields_line.split(',')
                Parent.log_select(self, fields_list)
                print(fields_list)

    def log_select(self, temp01):
        if self.template_no == 'UDPR':
            UDPReceive.test(self, temp01)
        if self.template_no == 'UDPT':
            UDPTransmit.test(self, temp01)
        if self.template_no == 'TCPR':
            TCPReceive.test(self, temp01)
        if self.template_no == 'RAWR':
            RAWReceive.test(self, temp01)


class UDPReceive(Parent):
    print('THIS IS THE UDPReceive CHILD OBJECT')

    def test(self, udpr_temp):
        log_fields_udpr = {'packet_number': udpr_temp[0],
                           'rx_sequence_number': udpr_temp[1],
                           'tx_timestamp': udpr_temp[2],
                           'rx_timestamp': udpr_temp[3],
                           'rx_ttl': udpr_temp[4],
                           'rx_size': udpr_temp[5],
                           'Seen_by_raw_socket': udpr_temp[6],
                           'seen_by_protocol_socket': udpr_temp[7]
        }
        print(log_fields_udpr)
        log_fields_id = self.fields_db.insert(log_fields_udpr)
        print(self.fields_db.find_one(), '\n', log_fields_id, '\n\n')


class UDPTransmit(Parent):
    print('THIS IS THE UDPTransmit CHILD')

    def test(self, udpt_temp):
        log_fields_udpt = {'packet_number': udpt_temp[0],
                           'bytes': udpt_temp[1],
                           'tx_timestamp_1': udpt_temp[2],
                           'TX timestamp 2': udpt_temp[3],
                           'loop_iterations': udpt_temp[4]
        }
        log_fields_id = self.fields_db.insert(log_fields_udpt)
        print(self.fields_db.find_one(), '\n', log_fields_id, '\n\n')


class TCPReceive(Parent):
    print('THIS IS THE TCPReceive CHILD')

    def test(self, tcpr_temp):
        log_fields_tcpr = {'rx_sequence_number': tcpr_temp[0],
                           'rx_timestamp': tcpr_temp[1],
                           'rx_size': tcpr_temp[2],
                           }
        log_fields_id = self.fields_db.insert(log_fields_tcpr)
        print(self.fields_db.find_one(), '\n', log_fields_id, '\n\n')


class RAWReceive(Parent):
    print('THIS IS THE RAWReceive CHILD')

    def test(self, rawr_temp):
        print(rawr_temp)
        log_fields_rawr = {'rx_sequence_number': rawr_temp[0],
                           'rx_timestamp': rawr_temp[1],
                           'rx_size': rawr_temp[2],
                           'ttl': rawr_temp[3],
                           }
        log_fields_id = self.fields_db.insert(log_fields_rawr)
        print(self.fields_db.find_one(), '\n', log_fields_id, '\n\n')


