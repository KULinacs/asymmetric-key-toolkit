import askey
import base64

test = askey.Asymmetric_Key("one.pub")
print(base64.b64encode(test.value.encode()))
test.value[1][0][1].value = 3
print(base64.b64encode(test.value.encode()))
