import base64
import intcodecs
import asn1key

class Asymmetric_Key:

    def __init__(self, filename):
        self.__parse_file(filename)

    def __parse_file(self, filename):
        key_file = open(filename, "r")
        key_lines = key_file.readlines()
        base64key = ""
        if key_lines[0][:-1] != "-----BEGIN PUBLIC KEY-----":
            raise KeyError("Unsupported Key Type")
        for x in range(1, len(key_lines) - 1):
            base64key += key_lines[x][:-1]
        decoded_key = base64.b64decode(base64key)
        #key_values = [chr(byte) for byte in decoded_key]
        key_bytes = bytearray(decoded_key)
        self.__parse_bytes(key_bytes)

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
            parsed_len = intcodecs.defdecode(value_bytes[len_start :
                                                           len_stop])
            data_start = len_stop
            data_stop = data_start + parsed_len + 1
        self.value = asn1key.make_object(maintype,
                                         key_bytes[data_start : data_stop])
    
class KeyError(Exception):
    pass

