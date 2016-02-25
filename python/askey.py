import base64
import intcodecs
import asn1key
import sshkey

class Asymmetric_Key:

    def __init__(self, filename):
        self.__parse_file(filename)

    def __parse_file(self, filename):
        key_file = open(filename, 'r')
        firstline = key_file.next()
        if firstline[0] == '-':
            self.__parse_lines(filename)
        else:
            self.__parse_single(filename)

    def __parse_lines(self, filename):
        key_file = open(filename, 'r')
        key_lines = key_file.readlines()
        self.header = key_lines[0][:-1]
        base64_data = ""
        for line in key_lines[1:-1]:
            base64_data += line[:-1]
        self.footer = key_lines[-1]
        self.__parse_bytes(bytearray(base64.b64decode(base64_data)))

    def __parse_single(self, filename):
        key_file = open(filename, 'r')
        key_split = key_file.read().split(' ')
        self.header = key_split[0]
        base64_data = key_split[1]
        self.footer = key_split[-1]
        binary_data = bytearray(base64.b64decode(base64_data))
        self.value = sshkey.parse_key(binary_data)

    def __parse_bytes(self, key_bytes):
        maintype = key_bytes[0]
        cur_len = key_bytes[1]
        if cur_len < 0x80:
            parsed_len = cur_len
            data_start = 2
            data_stop = data_start + parsed_len + 1
        else:
            len_start = 1
            len_stop = len_start + cur_len - 0x80 + 1
            parsed_len = intcodecs.defdecode(key_bytes[len_start :
                                                       len_stop])
            data_start = len_stop
            data_stop = data_start + parsed_len + 1
        self.value = asn1key.make_object(maintype,
                                         key_bytes[data_start : data_stop])
    
class KeyError(Exception):
    pass

