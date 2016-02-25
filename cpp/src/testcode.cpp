#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

int main() {
  vector<string> contents;
  string line;
  ifstream infile("../test/testkeys/id_rsa.pub");
  if (infile.is_open()) {
    while (getline(infile, line)) {
      contents.push_back(line);
    }
    infile.close();
    cout << contents.size();
  } else {
    cout << "Unable to open file" << endl;
  }
  return 0;
}
