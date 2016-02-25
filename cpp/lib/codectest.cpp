#include "intcodec.h"
#include <iostream>

using namespace std;

int main() {
  vector<unsigned char> input;
  //for (int i = 0; i < input.size(); ++i) {
  //  cout << int(input[i]) << endl;
  //}
  input = derIntEncode(311);
  //for (int i = 0; i < input.size(); ++i) {
    //  cout << int(input[i]) << endl;
  //}
  cout << derIntDecode(input) << endl;
  input = derIntEncode(128);
  cout << derIntDecode(input) << endl;
  input = derIntEncode(100);
  cout << derIntDecode(input) << endl;
  input = derIntEncode(-512);
  //for (int i = 0; i < input.size(); ++i) {
  //  cout << int(input[i]) << endl;
  //}
  cout << derIntDecode(input) << endl;
  input = derIntEncode(6512);
  cout << derIntDecode(input) << endl;
  input = derIntEncode(0);
  cout << derIntDecode(input) << endl;
}
