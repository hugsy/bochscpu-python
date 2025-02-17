#
# Script taken from WTF (https://github.com/0vercl0k/wtf/)
#
# Axel '0vercl0k' Souchet - May 2 2020
# Build / configure bxcpu-ffi
set -x
set -e

pushd .

test -z $NB_CPU && NB_CPU=1

mkdir bxbuild
cd bxbuild

git clone https://github.com/hugsy/bochscpu-build.git
git clone https://github.com/hugsy/bochscpu.git
git clone https://github.com/hugsy/bochscpu-ffi.git

cd bochscpu-build
bash prep.sh && cd Bochs/bochs && sh .conf.cpu 
make -j ${NB_CPU} -C cpu/fpu
make -j ${NB_CPU} -C cpu/avx
make -j ${NB_CPU} -C cpu/cpudb
make -j ${NB_CPU} -C cpu/softfloat3e
make -j ${NB_CPU} -C cpu

# Remove old files in bochscpu.
rm -rf ../../../bochscpu/bochs
rm -rf ../../../bochscpu/lib

# Create the libs directory where we stuff all the libs.
mkdir ../../../bochscpu/lib
find . -type f -name 'lib*.a' -exec cp -v {} ../../../bochscpu/lib/ \;
make all-clean

# Now we want to copy the bochs directory over there.
cd ..
mv bochs ../../bochscpu/bochs

# Now its time to build it.
cd ../../bochscpu-ffi

cargo clean
cargo build -j ${NB_CPU}
cargo build -j ${NB_CPU} --release

# Get back to where we were.
popd
