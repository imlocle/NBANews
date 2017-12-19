# Command line to deal with security protocol
env ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install PyOpenSSL

#kill port
sudo lsof -t -i tcp:8000 | xargs kill -9

brew install --build-from-source python

pip install requests
pip install bcrypt
pip install 'django<2.0'
pip install -e
pip install --two jupyter