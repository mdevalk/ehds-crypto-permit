brew install cmake ninja openssl@3 git
git clone https://github.com/open-quantum-safe/liboqs.git
cd liboqs
mkdir build
cd build
cmake -GNinja .. -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=/usr/local
ninja
sudo ninja install