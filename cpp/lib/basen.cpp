// Author kulinacs <kulinacs@bellicosedev.com>
// Uses standards defined in RFC 4648

#include <string>
#include <stdexcept>
#include <cstring>

const std::string base64Alphabet[] = { "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef"
                                       "ghijklmnopqrstuvwxyz0123456789+/",
                                       "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef"
                                       "ghijklmnopqrstuvwxyz0123456789-_" };

std::string base64Encode(const unsigned char bytes[], const size_t size,
                         const int alphabet = 0, const char padChar = '=') {
  if (base64Alphabet[alphabet].find(padChar) > -1 &&
      base64Alphabet[alphabet].find(padChar) < 64) {
    throw std::invalid_argument("Invalid Padding Character");
  }
  std::string encodedString = "";
  int byteValue;
  for (int i = 0; i < size; i = i + 3) {
    byteValue = (bytes[i] & 0b11111100) >> 2;
    encodedString += base64Alphabet[alphabet][byteValue];
    byteValue = (bytes[i] & 0b00000011) << 4;
    if (i + 1 < size) {
      byteValue |= (bytes[i + 1] & 0b11110000) >> 4;
      encodedString += base64Alphabet[alphabet][byteValue];
      byteValue = (bytes[i + 1] & 0b00001111) << 2;
      if (i + 2 < size) {
        byteValue |= (bytes[i + 2] & 0b11000000) >> 6;
        encodedString += base64Alphabet[alphabet][byteValue];
        byteValue = bytes[i + 2] & 0b00111111;
        encodedString += base64Alphabet[alphabet][byteValue];
      } else {
        encodedString += base64Alphabet[alphabet][byteValue];
        encodedString.append(1, padChar);
      }
    } else {
      encodedString += base64Alphabet[alphabet][byteValue];
      encodedString.append(2, padChar);
    }
  }
  return encodedString;
}

std::string base64Encode(const std::string &decodedString, const int alphabet = 0,
                         const char padChar = '=') {
    unsigned char* decodedArray = new unsigned char[decodedString.size()];
    strcpy((char*) decodedArray, decodedString.c_str());
    std::string encodedString = base64Encode(decodedArray, decodedString.size(),
                                             alphabet, padChar);
    delete decodedArray;
    return encodedString;
}

std::string base64Decode(const std::string &encodedString, const int alphabet = 0,
                         const char padChar = '=') {
  if (encodedString.size() % 4 != 0) {
    throw std::invalid_argument("Invalid Base64 Data");
  }
  if (base64Alphabet[alphabet].find(padChar) > -1 &&
      base64Alphabet[alphabet].find(padChar) < 64) {
    throw std::invalid_argument("Invalid Padding Character");
  }
  std::string decodedString = "";
  int tempByte;
  char bytes[4];
  for (int i = 0; i < encodedString.size(); i = i + 4) {
    for (int j = 0; j < 4; j++) {
      tempByte = base64Alphabet[alphabet].find(encodedString[i + j]);
      if (tempByte == std::string::npos &&
          (encodedString[i + j] != padChar || j < 2)) {
        throw std::invalid_argument("Invalid Base64 Data");
      }
      bytes[j] = tempByte;
    }
    tempByte = bytes[0] << 2;
    tempByte |= (bytes[1] & 0b110000) >> 4;
    decodedString += tempByte;
    if (encodedString[i + 2] != padChar) {
      tempByte = (bytes[1] & 0b001111) << 4;
      tempByte |= (bytes[2] & 0b111100) >> 2;
      decodedString += tempByte;
      if (encodedString[i + 3] != padChar) {
        tempByte = (bytes[2] & 0b000011) << 6;
        tempByte |= bytes[3];
        decodedString += tempByte;
      } else {
        break;
      }
    } else {
      break;
    }
  }
  return decodedString;
}
