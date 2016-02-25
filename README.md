# Asymmetric Key Toolkit
A work in progress library designed to parse DER encoded asymmetric keys (generated from OpenSSH and OpenSSL) implemented in Python and C++. Code scattered as it is in sporadic development and will be cleaned up as updates are published.

## Python
NOTE: In an attempt to provide functionality for Python3, some features were broken and are being fixed in order of discovery.
### Current Features:
* Full parsing of OpenSSL generated keys and OpenSSH generated private keys
* Some parsing of OpenSSH public keys (YMMV)
* Full back-end support for binary to needed ASN1 Objects
* Printing of ASN1 Objects into a human readable format

### Planned Features:
* More user friendly interaction with keys that doesn't require back-end knowledge
* Key specific classes to provided more key specific functionality (i.e. setting parameters by functionality instead of position in encoded data)
* Command line interface
* Tests to ensure program correctness

## C++
NOTE: The C++ library is significantly newer and is lagging behind in features and ease of use.
### Current Features:
* Base64 Decoding of generated keys
* Integer codecs that DER requires

### Features in Progress:
* DER decoding of key binary data