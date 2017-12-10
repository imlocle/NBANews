# Command line to deal with security protocol
env ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install PyOpenSSL

brew install --build-from-source python
