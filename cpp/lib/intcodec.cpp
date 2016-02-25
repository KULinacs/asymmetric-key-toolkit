#include <vector>
#include <stdexcept>
#include <iostream>

// Definite Length Encoding
// Consider pushing back entries and then reversing
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

// Definite Length Decoding
int definiteDecode(std::vector<unsigned char> inputVector) {
  // No length identifier
  int decodedInt;
  if (inputVector[0] < 0x80) {
     decodedInt = inputVector[0];
  } else {
    int length = inputVector[0] & 0x7F;
    decodedInt = 0;
    for (int i = 1; i <= length; i++) {
      decodedInt = decodedInt << 8;
      decodedInt = decodedInt | inputVector[i];
    }
  }
  return decodedInt;
}

// Variable Length Quantity Encoding
// Do NOT use this for first two nodes of DER ASN1 Object Identifiers
std::vector<unsigned char> variableLengthEncode(int input) {
  // If length is less than 128, no extra action is taken
  if (input < 0x80 && input > -1) {
    std::vector<unsigned char> encodedInt;
    encodedInt.push_back(input);
    return encodedInt;
  // If length is greater than 128, each byte but the last has the MSB set to 1
  } else if (input >= 0x80) {
    std::vector<unsigned char> encodedInt;
    encodedInt.push_back(input & 0x7F);
    input = input >> 7;
    while (input > 0) {
      encodedInt.insert(encodedInt.begin(), input | 0x80);
      input = input >> 7;
    }
    return encodedInt;
  } else {
    throw std::invalid_argument("Negative Number passed");
  }
}

// Variable Length Quantity Decoding
// Do NOT use this for first two nodes of DER ASN1 Object Identifiers
int variableLengthDecode(std::vector<unsigned char> inputVector) {
  // No length identifier
  int decodedInt;
  if (inputVector[0] < 0x80) {
    decodedInt = inputVector[0];
  } else {
    decodedInt = 0;
    for (int i = 0; i < inputVector.size(); i++) {
      decodedInt = decodedInt << 7;
      decodedInt = decodedInt | (inputVector[i] & 0x7F);
    }
  }
  return decodedInt;
}

// DER Integer Encoding
std::vector<unsigned char> derIntEncode(int input) {
  std::vector<unsigned char> encodedInt;
  if (input > -1) {
    if (input == 0) {
      encodedInt.push_back(0);
    }
    while (input > 0) {
      encodedInt.insert(encodedInt.begin(), input & 0xFF);
      input = input >> 8;
    }
    if ((encodedInt[0] & 0x80) == 0x80) {
      encodedInt.insert(encodedInt.begin(), 0);
    }
  } else {
    input = input * -1;
    while (input > 0) {
      encodedInt.insert(encodedInt.begin(), input & 0xFF);
      input = input >> 8;
    }
    if ((encodedInt[0] & 0x80) == 0x80) {
      encodedInt.insert(encodedInt.begin(), 0x80);
    } else {
      encodedInt[0] = encodedInt[0] | 0x80;
    }
  }
  return encodedInt;
}

// DER Integer Decode
int derIntDecode(std::vector<unsigned char> inputVector) {
  int sign = 1;
  int decodedInt = 0;
  if ((inputVector[0] & 0x80) == 0x80) {
    sign = -1;
    inputVector[0] = inputVector[0] & 0x7F;
  }
  for (int i = 0; i < inputVector.size(); i++) {
    decodedInt = decodedInt << 8;
    decodedInt = decodedInt | inputVector[i];
  }
  decodedInt = decodedInt * sign;
  return decodedInt;
}
