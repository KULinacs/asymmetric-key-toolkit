import intcodecs

def __decode_length(byte_array):
    value = 0
    exponent = (len(byte_array) - 2) * 2
    for byte in byte_array[1:]:
        value += byte * pow(16, exponent)
        exponent -= 2
    return value

def __encode_length(number):
    hexnumber = hex(number)[2:]
    if len(hexnumber) % 2 == 1:
        hexnumber = '0' + hexnumber
    if len(hexnumber) > 8:
        raise TypeError('Input number is too large')
    return bytearray().fromhex(hexnumber)
    
def parse_key(value):
    i = 0
    string_list = []
    length = __decode_length(value[i : i+4])
    i += 4
    string_list.append(SSH_String(value[i : i+length]))
    i += length
    while i < len(value):
        length = __decode_length(value[i : i+4])
        i += 4
        string_list.append(SSH_Integer(value[i : i+length]))
        i += length
    return string_list

class SSH_String(object):

    def __init__(self, value):
        self.__set_value(value)

    def __str__(self):
        return hex(len(self)) + ": " + str(self.__value)

    def __len__(self):
        return len(self.__encoded_value)

    def __set_value(self, value):
        if isinstance(value, str):
            self.__value = value
            self.__encoded_value = bytearray(value)
        else:
            try:
                self.__value = str(value)
                self.__encoded_value = value
            except:
                raise TypeError('Input must be a string or a list of bytes')
                
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__set_value(value)

    def encode(self):
        byte_values = __decode_length(len(self))
        byte_values.extend(self.__encoded_value)
        return byte_values

class SSH_Integer(object):
    
    def __init__(self, value):
        self.__set_value(value)

    def __str__(self):
        return hex(len(self)) + ": " + hex(self.__value)

    def __len__(self):
        return len(self.__encoded_value)

    def __set_value(self, value):
        '''Accepts integer or byte values'''
        if isinstance(value, int):
            self.__value = value
            self.__encoded_value = intcodecs.derencode(value)
        else:
            try:
                self.__value = intcodecs.derdecode(value)
                self.__encoded_value = value
            except:
                raise TypeError('Value must be an integer or a list of bytes')
                
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__set_value(value)

    def encode(self):
        byte_values = __decode_length(len(self))
        byte_values.extend(self.__encoded_value)
        return byte_values
