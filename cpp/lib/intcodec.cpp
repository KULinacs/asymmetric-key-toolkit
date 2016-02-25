#include <vector>
#include <stdexcept>

// Definite Length Encoding for ASN1 Length Fields
std::vector<unsigned char> definiteEncode(int input) {
  // If length is less than 128, no length identifier is needed.
  if (input < 0x80 && input > -1) {
    std::vector<unsigned char> encodedInt;
    encodedInt.push_back(input);
    return encodedInt;
  // If length is greater than 128, a length identifier is added.
  } else if (input >= 0x80) {
    int counter = 0x80;
    std::vector<unsigned char> encodedInt;
    while (input > 0) {
      encodedInt.insert(encodedInt.begin(), input & 0xFF);
      input = input >> 8;
      counter++;
    }
    encodedInt.insert(encodedInt.begin(), counter);
    return encodedInt;
  } else {
    throw std::invalid_argument("Negative Number passed");
  }
}

// Definite Length Decoding for ASN1 Length Fields
int definiteDecode(std::vector<unsigned char> inputVector) {
  // No length identifier
  if (inputVector[0] < 0x80) {
    int decodedInt = inputVector[0];
    return decodedInt;
  } else {
    int length = inputVector[0] ^ 0x80;
    int decodedInt = 0;
    for (int i = 1; i <= length; i++) {
      decodedInt = decodedInt << 8;
      decodedInt = decodedInt | inputVector[i];
    }
    return decodedInt;
  }
}
