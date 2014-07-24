__author__ = 'Majid Arianezhad'
import os
import linecache
rootDir = '/Users/Aria/Dropbox/PyCharm_Files/iibex/sample'


class iibex(object):
    def __init__(self, flnm, pth):
        self.filename = flnm                    # Filename
        self.path = pth                         # Path
        self.field_line = None                  # Line of field in string
        self.field_line_list = None             # Line of field in list
        self.flags = None                       # Flag holds the log type -- UDPR, UDPT, TCPR, RAWR
        self.headers_labels = []                # Holds the headers labels in a list
        self.headers_label_pos = []             # Holds the positions for labels in a list
        """
            UDP Receive variables.
        """
        self.headers_udpr = ['Experiment:',
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
        self.udpr_packet_number = None
        self.udpr_rx_sequence_number = None
        self.udpr_tx_timestamp = None
        self.udpr_rx_timestamp = None
        self.udpr_rx_ttl = None
        self.udpr_rx_size = None
        self.udpr_seen_raw_socket = None
        self.udpr_seen_protocol_socket = None
        """
            UDP Transmit variables
        """
        self.headers_udpt = ['Experiment:',
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
        self.udpt_packet_number = None
        self.updt_bytes = None
        self.udpt_tx_timestamp_1 = None
        self.udpt_tx_timestamp_2 = None
        self.udpt_loop_iterations = None
        """
            TCP Receive variables
        """
        self.headers_tcpr = ['Experiment:',
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
        self.tcpr_rx_sequence_number = None
        self.tcpr_rX_timestamp = None
        self.tcpr_rx_size = None
        """
            RAW Receive variables
        """
        self.headers_rawr = ['Experiment:',
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
        self.rawr_rx_sequence_number = None
        self.rawr_rx_timestamp = None
        self.rawr_rx_size = None
        self.rawr_ttl = None

    """ Get the file name and return split in a list """
    def get_filename(self):
        if os.path.splitext(self.filename)[1] == '.txt' and '_' in self.filename:
            l = self.filename.split('.')
            return l[0].split('_')

    """ Open the log file from the path and return the file in fo """
    def get_log_text(self):
        with open(self.path, 'r') as fo:
            return fo.read()

    """ Calculate the total number of lines of the log file """
    def get_total_lines(self):
        return iibex.get_log_text(self).count('\n')

    """ Return the line number where fields start """
    def get_first_field_line(self):
        temp01 = iibex.get_total_lines(self)
        for fl in range(1, temp01 + 1):
            line = linecache.getline(self.path, fl)
            if line[0].isdigit() and ',' in line:
                return fl

    """ Select the log type and return its headers """
    def log_select(self):
        if iibex.get_filename(self)[7] == 'UDP' and iibex.get_filename(self)[5] == 'R':
            self.flags = 'UDPR'
            self.headers_labels = self.headers_udpr
            return self.headers_labels
        elif iibex.get_filename(self)[7] == 'UDP' and iibex.get_filename(self)[5] == 'T':
            self.flags = 'UDPT'
            self.headers_labels = self.headers_udpt
            return self.headers_labels
        elif iibex.get_filename(self)[7] == 'TCP' and iibex.get_filename(self)[5] == 'R':
            self.flags = 'TCPR'
            self.headers_labels = self.headers_tcpr
            return self.headers_labels
        elif iibex.get_filename(self)[7] == 'RAW' and iibex.get_filename(self)[5] == 'R':
            self.flags = 'RAWR'
            self.headers_labels = self.headers_rawr
            return self.headers_labels

    """ Return the line number of headers in a list """
    def log_headers_line_no(self):
        headers_lines = []
        for counter in range(0, len(self.headers_labels)):
            pos = iibex.get_log_text(self).index(self.headers_labels[counter])
            temp02 = iibex.get_log_text(self).count("\n", 0, pos + len(self.headers_labels[counter]))+1
            headers_lines.append(temp02)
        return headers_lines

    """ Return header tiles and values """
    def output_headers(self):
        temp04 = iibex.log_select(self)
        temp03 = iibex.log_headers_line_no(self)
        header_values = []
        for jjj in range(0, len(self.headers_labels)):
            s = linecache.getline(self.path, temp03[jjj]).split(temp04[jjj], 1)
            header_values.append(str(s[1][1:].replace('\n', '')))
        return (header_values)

    """ Extract fields and return fields in a list """
    def field_extract(self):
        ffl = iibex.get_first_field_line(self)
        lfl = iibex.get_total_lines(self)
        for fc in range(ffl, lfl+1):
            field_line = linecache.getline(self.path, fc).replace('\n', '')
            validated_line = iibex.validate_fields(self, field_line)

    """ Validate a line """
    def validate_fields(self, f_l):
        a_line = f_l
        # if iibex.validate_rule03(self, a_line) is True:
        #     field_line_list = a_line.split(',')
        #     iibex.build_dictionary(self, field_line_list)
        #     return field_line_list
        if iibex.validate_rule01(self, a_line) is True:
            if iibex.validate_rule02(self, a_line) is True:
                if iibex.validate_rule03(self, a_line) is True:
                    field_line_list = a_line.split(',')
                    iibex.build_dictionary(self, field_line_list)
                    return field_line_list

    """ Validation rules """
    def validate_rule01(self, a_l):
        v_l = a_l
        if ',' in v_l:
            return True
        else:
            iibex.badline_writer(self, v_l)

    def validate_rule02(self, a_l):
        v_l = a_l
        if len(v_l) > 8:
            return True
        else:
            iibex.badline_writer(self, v_l)

    def validate_rule03(self, v_l):
        if self.flags == 'UDPR':
            if v_l.count(',') == 7:
                return True
            else:
                iibex.badline_writer(self, v_l)

        elif self.flags == 'UDPT':
            if v_l.count(',') == 4:
                return True
            else:
                iibex.badline_writer(self, v_l)

        elif self.flags == 'TCPR':
            if v_l.count(',') == 2:
                return True
            else:
                iibex.badline_writer(self, v_l)

        elif self.flags == 'RAWR':
            if v_l.count(',') == 3:
                return True
            else:
                iibex.badline_writer(self, v_l)

    def badline_writer(self, badline):
        z = badline[0:-1], self.path, iibex.get_filename(self)[4]
        y = str(z)
        with open('badlines.txt', 'a') as x:
            x.write(y)
            x.write('\n')
            x.close()

    def build_dictionary(self, a_field):
        file_name = iibex.get_filename(self)
        if self.flags == 'UDPR':
            iibex.udpr_dic(self, a_field, file_name[4])

        elif self.flags == 'UDPT':
            iibex.updt_dic(self, a_field, file_name[4])

        elif self.flags == 'TCPR':
            iibex.tcpr_dic(self, a_field, file_name[4])

        elif self.flags == 'RAWR':
            iibex.rawr_dic(self, a_field, file_name[4])

    def udpr_dic(self, a_field_dic, time_stamp):
        updr_headers = iibex.output_headers(self)
        total_items = {
            'experiment': updr_headers[0],
            'run': updr_headers[1],
            'local_beacon': updr_headers[2],
            'local_beacon_hostname': updr_headers[3],
            'local_IP':updr_headers[4],
            'software_ver': updr_headers[5],
            'configured_local_port': updr_headers[6],
            'remote_beacon': updr_headers[7],
            'remote_IP': updr_headers[8],
            'configured_remote_port': updr_headers[9],
            'actual_remote_port_observed': updr_headers[10],
            'start': time_stamp,
            'mode': updr_headers[12],
            'socket_listening_time': updr_headers[13],
            'packets_received': updr_headers[14]
        }
        fields_dic = {
            'packet_number': a_field_dic[0],
            'rx_sequence_number': a_field_dic[1],
            'tx_timestamp': a_field_dic[2],
            'rx_timestamp': a_field_dic[3],
            'rx_ttl': a_field_dic[4],
            'rx_size': a_field_dic[5],
            'Seen_by_raw_socket': a_field_dic[6],
            'seen_by_protocol_socket': a_field_dic[7]
        }
        print('UDPR Dictionary is:', fields_dic, total_items)

    def updt_dic(self, a_field_dic, time_stamp):
        updt_headers = iibex.output_headers(self)
        headers_dic = {
            'Experiment': updt_headers[0],
            'Run': updt_headers[1],
            'Local beacon': updt_headers[2],
            'Local beacon hostname': updt_headers[3],
            'Local IP': updt_headers[4],
            'Local port': updt_headers[5],
            'Local beacon software version': updt_headers[6],
            'Remote beacon': updt_headers[7],
            'Remote IP': updt_headers[8],
            'Remote port': updt_headers[9],
            'Start': time_stamp,
            'Mode': updt_headers[11],
            'Socket timeout': updt_headers[12],
            'Stuffing file used': updt_headers[13],
            'Nominal intertransmission time': updt_headers[14],
            'Number of packets transmitted': updt_headers[15],
            'UDP payload size': updt_headers[16]
        }
        fields_dic = {
            'packet_number': a_field_dic[0],
            'bytes': a_field_dic[1],
            'tx_timestamp_1': a_field_dic[2],
            'TX timestamp 2': a_field_dic[3],
            'loop_iterations': a_field_dic[4]
        }
        print('UDPT Dictionary is:', fields_dic, headers_dic)

    def tcpr_dic(self, a_field_dic, time_stamp):
        tcpr_headers = iibex.output_headers(self)
        headers_dic = {
            'experiment': tcpr_headers[0],
            'run': tcpr_headers[1],
            'local_beacon': tcpr_headers[2],
            'local_beacon_hostname': tcpr_headers[3],
            'local_IP':tcpr_headers[4],
            'software_ver': tcpr_headers[5],
            'configured_local_port': tcpr_headers[6],
            'remote_beacon': tcpr_headers[7],
            'remote_IP': tcpr_headers[8],
            'configured_remote_port': tcpr_headers[9],
            'actual_remote_port_observed': tcpr_headers[10],
            'start': time_stamp,
            'mode': tcpr_headers[12],
            'socket_listening_time': tcpr_headers[13],
            'packets_received': tcpr_headers[14]
        }
        fields_dic = {
            'rx_sequence_number': a_field_dic[0],
            'tx_timestamp': a_field_dic[1],
            'rx_size': a_field_dic[2]
        }
        print('TCPR Dictionary is:', fields_dic, headers_dic)

    def rawr_dic(self, a_field_dic, time_stamp):
        rawr_headers = iibex.output_headers(self)
        headers_dic = {
            'experiment': rawr_headers[0],
            'run': rawr_headers[1],
            'local_beacon': rawr_headers[2],
            'local_beacon_hostname': rawr_headers[3],
            'local_IP':rawr_headers[4],
            'local_port': rawr_headers[5],
            'software_ver': rawr_headers[6],
            'remote_beacon': rawr_headers[7],
            'remote_IP': rawr_headers[8],
            'configured_remote_port': rawr_headers[9],
            'actual_remote_port_observed': rawr_headers[10],
            'TCP_rate_mode': rawr_headers[11],
            'start': time_stamp,
            'mode': rawr_headers[13],
            'socket_listening_time': rawr_headers[14],
            'packets_received': rawr_headers[15]
        }
        fields_dic = {
            'rx_sequence_number': a_field_dic[0],
            'tx_timestamp': a_field_dic[1],
            'rx_size': a_field_dic[2]
        }
        print('RAWR Dictionary is:', headers_dic, fields_dic)

for dirName, subdirList, fileList in os.walk(rootDir):
    for f_name in fileList:
        if f_name != '.DS_Store':
            path = dirName + '/' + f_name
            child = iibex(f_name, path)
            child.output_headers()
            child.field_extract()
