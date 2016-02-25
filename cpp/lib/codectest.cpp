#include "intcodec.h"
#include <iostream>

using namespace std;

int main() {
  vector<unsigned char> input;
  input = definiteEncode(256);
  //for (int i = 0; i < input.size(); ++i) {
  //  cout << int(input[i]) << endl;
  //}
  cout << definiteDecode(input) << endl;
  input = definiteEncode(128);
  cout << definiteDecode(input) << endl;
  input = definiteEncode(512);
  cout << definiteDecode(input) << endl;
  input = definiteEncode(6512);
  cout << definiteDecode(input) << endl;
}
