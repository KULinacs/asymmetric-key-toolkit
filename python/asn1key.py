import intcodecs

class ASN1_Object(object):

    def __init__(self, value):
        self.__set_value(value)

    def __len__(self):
        return len(self.__encoded_value)

    def __str__(self):
        header = 'OBJECT ' + hex(len(self)) + ' ('
        return header + hex(self.__value) + ')'

    def identity(self):
        return 0

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = self.__set_value(value)

    def encode(self):
        byte_values = bytearray(chr(self.identity).encode('utf-8'))
        byte_values.extend(intcodecs.defencode(len(self)))
        byte_values.extend(self.__encoded_value)
        return byte_values

class ASN1_Integer(ASN1_Object):

    '''An ASN1 Encoded Integer'''
    
    def __init__(self, value):
        self.__set_value(value)

    def __len__(self):
        return len(self.__encoded_value)

    def __str__(self):
        header = 'INTEGER ' + hex(len(self)) + ' ('
        return header + hex(self.__value) + ')'

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
    def identity(self):
        return 2

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__set_value(value)

    def encode(self):
        byte_values = bytearray(chr(self.identity).encode('utf-8'))
        byte_values.extend(intcodecs.defencode(len(self)))
        byte_values.extend(self.__encoded_value)
        return byte_values

class ASN1_Bit_String(ASN1_Object):

    '''An ASN1 encoded Bit_String. Currently does not support unused bits'''

    def __init__(self, value):
        self.__set_value(value)

    def __len__(self):
        return len(self.__encoded_value) + 1

    def __str__(self):
        header = 'BIT_STRING ' + hex(len(self)) + ' {\n\t'
        return header + '\n\t'.join(str(item).replace('\t', '\t\t')
                                        for item in self.__value) + '\n\t}'

    def __set_value(self, value):
        self.__value = []
        self.__encoded_value = bytearray()
        self.extend(value[1:])

    def __getitem__(self, i):
        return self.__value[i]
        

    def __setitem__(self, i, value):
        if isinstance(value, ASN1_Object):
            self.__value[i] = value
        else:
            raise TypeError('Only Object values my be set')

    def append(self, value):
        if isinstance(value, ASN1_Object):
            self.extend([value])
        else:
            self.extend(value)

    def extend(self, value):
        if isinstance(value, list):
            try:
                self.__value.extend(value)
                self.__encoded_value.extend(bytearray([item.encode()
                                                       for item in value]))
            except:
                raise TypeError('List must contain ASN1 objects')
        else:
            self.__encoded_value.extend(value)
            try:
                i = 0
                while i < len(value):
                    ident = value[i]
                    ident_len = value[i + 1]
                    if ident_len < 0x80:
                        data_len = ident_len
                        data_start = i + 2
                    else:
                        len_start = i + 1
                        data_start = len_start - ident_len - 0x80 + 1
                        data_len = intcodecs.defdecode(value[len_start : 
                                                            data_start])
                    data_stop = data_start + data_len
                    self.__value.append(make_object(ident, value[data_start :
                                                                 data_stop]))
                    i = data_stop
            except:
                self.__value = self.__encoded_value

    @property
    def identity(self):
        return 3

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = self.__set_value(value)
    
    def encode(self):
        self.__encoded_value = bytearray()
        for item in self.__value:
            self.__encoded_value.extend(item.encode())
        byte_values = bytearray(chr(self.identity).encode('utf-8'))
        byte_values.extend(intcodecs.defencode(len(self)))
        byte_values.extend(bytearray(chr(0x00).encode('utf-8')))
        byte_values.extend(self.__encoded_value)
        return byte_values
        

class ASN1_Null(ASN1_Object):

    '''An ASN1 Null Object'''
    
    def __init__(self, value):
        self.__set_value(value)

    def __len__(self):
        return len(self.__encoded_value)

    def __str__(self):
        header = 'NULL ' + hex(len(self)) + ' ('
        return header + ')'

    def __set_value(self, value):
        if value == None or value == 0 or len(value) == 0:
            self.__value = None
            self.__encoded_value = bytearray()
        else:
            raise TypeError('ASN1 Null Objects can have no value')

    @property
    def identity(self):
        return 5

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__set_value(value)

    def encode(self):
        byte_values = bytearray(chr(self.identity).encode('utf-8'))
        byte_values.extend(intcodecs.defencode(len(self)))
        byte_values.extend(self.__encoded_value)
        return byte_values

class ASN1_ObjectID(ASN1_Object):

    '''An ASN1 Object ID'''
    
    def __init__(self, value):
        self.__set_value(value)

    def __len__(self):
        return len(self.__encoded_value)

    def __str__(self):
        header = 'OBJECTID ' + hex(len(self)) + ' ('
        return header + str(self.__value) + ')'

    def __set_value(self, value):
        if isinstance(value, str):
            self.__value = value
            self.__encoded_value = intcodecs.multivlqencode(value.split('.'))
        else:
            try:
                self.__value = str(value[0] // 40) + '.'
                self.__value += str(value[0] % 40) + '.'
                self.__value += '.'.join(str(octet) for octet in
                                       intcodecs.multivlqdecode(value[1:]))
                self.__encoded_value = value
            except:
                raise TypeError('Input must a "." separated string or a list of bytes')
        
    @property
    def identity(self):
        return 6

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__set_value(value)

    def encode(self):
        byte_values = bytearray(chr(self.identity).encode('utf-8'))
        byte_values.extend(intcodecs.defencode(len(self)))
        byte_values.extend(self.__encoded_value)
        return byte_values

class ASN1_Sequence(ASN1_Object):

    '''An ASN1 encoded Bit_String. Currently does not support unused bits'''
    
    def __init__(self, value):
        self.__set_value(value)

    def __len__(self):
        return len(self.__encoded_value)

    def __str__(self):
        header = 'SEQUENCE ' + hex(len(self)) + ' {\n\t'
        return header + '\n\t'.join(str(item).replace('\t', '\t\t')
                                    for item in self.__value) + '\n\t}'

    def __set_value(self, value):
        self.__value = []
        self.__encoded_value = bytearray()
        self.extend(value)

    def __getitem__(self, i):
        return self.__value[i]
        
    def __setitem__(self, i, value):
        if isinstance(value, ASN1_Object):
            self.__value[i] = value
        else:
            raise TypeError('Only Object values my be set')

    def append(self, value):
        if isinstance(value, ASN1_Object):
            self.extend([value])
        else:
            self.extend(value)

    def extend(self, value):
        if isinstance(value, list):
            try:
                self.__value.extend(value)
                self.__encoded_value.extend(bytearray([item.encode()
                                                       for item in value]))
            except:
                raise TypeError('List must contain ASN1 objects')
        else:
            self.__encoded_value.extend(value)
            try:
                i = 0
                while i < len(value):
                    ident = value[i]
                    ident_len = value[i + 1]
                    if ident_len < 0x80:
                        data_len = ident_len
                        data_start = i + 2
                    else:
                        len_start = i + 1
                        data_start = len_start + (ident_len - 0x80) + 1
                        data_len = intcodecs.defdecode(value[len_start : 
                                                        data_start])
                    data_stop = data_start + data_len
                    self.__value.append(make_object(ident, value[data_start :
                                                             data_stop]))
                    i = data_stop
            except:
                raise TypeError('Invalid bytes passed')

    @property
    def identity(self):
        return 48

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__set_value(value)

    def encode(self):
        self.__encoded_value = bytearray()
        for item in self.__value:
            self.__encoded_value.extend(item.encode())
        byte_values = bytearray(chr(self.identity).encode('utf-8'))
        byte_values.extend(intcodecs.defencode(len(self)))
        byte_values.extend(self.__encoded_value)
        return byte_values

class ASN1_Error(Exception):
    pass

objects = {1 : ASN1_Object, 2 : ASN1_Integer, 3 : ASN1_Bit_String,
           5 : ASN1_Null, 6 : ASN1_ObjectID, 48 : ASN1_Sequence}

def make_object(identity, value):
    #try:
    return objects[identity](value)
    #except:
    #    raise ASN1_Error('Unknown ASN1 Type specifed: ' + str(identity))
