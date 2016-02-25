import askey
import base64

test = askey.Asymmetric_Key('testkeys/id_ed25519.pub')
for ssh_string in test.value:
    print(ssh_string)
