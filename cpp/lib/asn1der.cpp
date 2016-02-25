#include <string>
#include <vector>

class DerObject {
public:
  DerObject();
  DerObject(std::vector<unsigned char> inBytes);
  DerObject(std::string inBytes);
  DerObject(unsigned char inBytes[], size_t size);
  virtual ~DerObject() = 0;
  int size();
protected:
  std::vector<unsigned char> bytes;
  static const unsigned char tag = 0;
};

DerObject::DerObject() {
  std::vector<unsigned char> bytes(0, 0);
}

DerObject::DerObject(std::vector<unsigned char> inBytes) {
  std::vector<unsigned char> bytes = inBytes;
}

DerObject::DerObject(std::string inBytes) {
  std::vector<unsigned char> bytes(inBytes.begin(), inBytes.end());
}

DerObject::DerObject(unsigned char inBytes[], size_t size) {
  std::vector<unsigned char> bytes(inBytes, inBytes + size);
}
  
int DerObject::size() {
  return bytes.size();
}
