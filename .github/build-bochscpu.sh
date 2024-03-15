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

git clone https://github.com/yrp604/bochscpu-build.git
git clone https://github.com/yrp604/bochscpu.git
git clone https://github.com/yrp604/bochscpu-ffi.git

cd bochscpu-build
bash prep.sh && cd Bochs/bochs && sh .conf.cpu && make -j ${NB_CPU}|| true

# Remove old files in bochscpu.
rm -rf ../../../bochscpu/bochs
rm -rf ../../../bochscpu/lib

# Create the libs directory where we stuff all the libs.
mkdir ../../../bochscpu/lib
cp -v cpu/libcpu.a ../../../bochscpu/lib/libcpu.a
cp -v cpu/fpu/libfpu.a ../../../bochscpu/lib/libfpu.a
cp -v cpu/avx/libavx.a ../../../bochscpu/lib/libavx.a
cp -v cpu/cpudb/libcpudb.a ../../../bochscpu/lib/libcpudb.a
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
