#ifndef __INTCODEC_H_INCLUDED__
#define __INTCODEC_H_INCLUDED__

#include <vector>
#include <stdexcept>

std::vector<unsigned char> definiteEncode(int input);
int definiteDecode(std::vector<unsigned char> inputVector);
std::vector<unsigned char> variableLengthEncode(int input);
int variableLengthDecode(std::vector<unsigned char> inputVector);
std::vector<unsigned char> derIntEncode(int input);
int derIntDecode(std::vector<unsigned char> inputVector);
#endif
