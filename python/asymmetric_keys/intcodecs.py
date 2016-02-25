'''
Contains functions to encode integers bytewise, particularly for use
in DER encoding
'''

def defencode(number):
    '''
    Definite Length encode an integer
    Returns a bytearray
    '''
    #try:
    if number < 0x80 and number > -1:
        return bytearray(chr(number).encode('utf-8'))
    elif number >= 0x80:
        hexnumber = hex(number)[2:]
        if len(hexnumber) % 2 == 1:
            hexnumber = '0' + hexnumber
        byte_count = len(hexnumber) // 2
        byte_array = bytearray(chr(0x80 + byte_count))
        byte_array.extend(bytearray.fromhex(hexnumber))
        return byte_array
    else:
        raise ValueError('Integer must be positive')
    #except:
    #    raise TypeError('Input must be an integer')

def defdecode(byte_array):
    '''
    Definite Length decode a bytearray
    Returns an integer
    '''
    try:
        value = 0
        exponent = (len(byte_array) - 2) * 2
        for byte in byte_array[1:]:
            value += byte * pow(16, exponent)
            exponent -= 2
        return value
    except:
        raise TypeError('Input must be a list of byte values')

def vlqencode(number):
    '''
    Variable Length Quantity encode an integer
    Returns a bytearray
    '''
    try:
        if number < 0x80 and number > -1:
            return bytearray(chr(number))
        elif number >= 0x80:
            bit_length = number.bit_length()
            binary = bin(number)[2:]
            if bit_length % 7 != 0:
                binary = (7 - bit_length % 7) * '0' + binary
                bit_length += 7 - bit_length % 7
            current_byte = 0
            bytes_list = []
            while current_byte < bit_length - 7:
                bytes_list.append('1' + binary[current_byte:current_byte + 7])
                current_byte += 7
            bytes_list.append('0' + binary[current_byte:current_byte + 7])
            byte_array = bytearray([chr(int(byte, 2)) for byte in bytes_list])
            return byte_array
        else:
            raise ValueError('Integer must be positive')
    except:
        raise TypeError('Input must be an integer')

def vlqdecode(byte_array):
    '''
    Variable Length Qunatity decode a bytearray
    Returns an integer
    '''
    try:
        binary = ''.join('{:08b}'.format(byte)[1:] for byte in byte_array)
        return int(binary, 2)
    except:
        raise TypeError('Input must be a list of byte values')

def multivlqencode(number_list):
    '''
    Variable Length Quantity encodes a list of integers
    Returns a bytearray
    '''
    try:
        byte_array = bytearray()
        for number in number_list:
            byte_array.extend(vlqencode(number))
        return byte_array
    except:
        raise TypeError('Input must be a list of integers')

def multivlqdecode(byte_array):
    '''
    Variable Length Qunatity decodes a bytearray containing multiple values
    Returns a list of integers
    '''
    try:
        previous = 0
        current = 1
        number_list = []
        while current < len(byte_array):
            while current < len(byte_array) - 1 and byte_array[current] > 0x80:
                current += 1
            number_list.append(vlqdecode(byte_array[previous:current + 1]))
            previous = current + 1
            current += 1
        return number_list
    except:
        raise TypeError('Input must be a list of byte values')

def derencode(number):
    '''
    DER Integer encode an integer
    Returns a bytearray
    '''
    if number >= 0:
        hexnumber = hex(number)[2:]
        if len(hexnumber) % 2 == 1:
            hexnumber = '0' + hexnumber
        elif int(hexnumber[0] + '0', 16) > 0x80:
            hexnumber = '00' + hexnumber
    else:
        hexnumber = hex(number)[3:]
        if len(hexnumber) % 2 == 1:
            hexnumber = '0' + hexnumber
        elif int(hexnumber[0] + '0', 16) > 0x80:
            hexnumber = '00' + hexnumber
        complimentary = 'F' * len(hexnumber)
        hexnumber = hex(int(complimentary, 16) - int(hexnumber, 16))[2:]
    byte_array = bytearray.fromhex(hexnumber)
    return byte_array

def derdecode(byte_array):
    '''
    DER Integer decode a bytearray
    Returns an integer
    '''
    hexnumber = ''.join('{:02x}'.format(byte) for byte in byte_array)
    if byte_array[0] >= 0x80:
        complimentary = 'F' * len(hexnumber)
        number = -(int(complimentary, 16) - int(hexnumber, 16))
    else:
        number = int(hexnumber, 16)
    return number
          
            
