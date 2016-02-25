from asymmetric_keys import sshkey, asn1key

key_formats = {'asn1' : _parse_asn1, 'ssh' : _parse_ssh}

def parse(filename):
    key_format = _get_format(filename)
    return key_formats[key_format]

def _get_format(filename):
    key_file = open(filename, 'r')
    first_line = key_file.next()
    if first_line.contains('-----'):
        return "asn1"
    elif first_line.contains('ssh'):
        return 'ssh'
    else:
        raise KeyException('Unsupported Key Format')

def _parse_asn1(filename):
    
def _parse_ssh(filename):
    
class KeyException(Exception):
    def __init__(self, *args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
