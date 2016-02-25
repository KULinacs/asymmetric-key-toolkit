#ifndef __BASEN_H_INCLUDED__
#define __BASEN_H_INCLUDED__

#include <string>
#include <stdexcept>

const std::string base64Alphabet[] = { "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef"
                                       "ghijklmnopqrstuvwxyz0123456789+/",
                                       "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef"
                                       "ghijklmnopqrstuvwxyz0123456789-_" };

std::string base64Encode(const unsigned char bytes[], const size_t size,
                         const int alphabet = 0, const char padChar = '=');
std::string base64Encode(const std::string &decodedString, const int alphabet = 0,
                         const char padChar = '=');
std::string base64Decode(const std::string &encodedString, const int alphabet = 0,
                         const char padChar = '=');
#endif
