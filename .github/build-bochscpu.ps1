$ErrorActionPreference = "Stop"

Push-Location

New-Item -ItemType Directory -Name bxbuild
Set-Location bxbuild

git clone https://github.com/yrp604/bochscpu-build.git
git clone https://github.com/yrp604/bochscpu.git
git clone https://github.com/yrp604/bochscpu-ffi.git

bash -c "cd bochscpu-build && bash prep.sh && cd Bochs/bochs && bash .conf.cpu-msvc"

Set-Location bochscpu-build\Bochs\bochs
$env:CL = "/MP$env:NUMBER_OF_PROCESSORS"
nmake cpu\softfloat3e\libsoftfloat.a
nmake cpu\fpu\libfpu.a
nmake cpu\avx\libavx.a
nmake cpu\cpudb\libcpudb.a
nmake cpu\libcpu.a

# Don't actually need the rest
# nmake

Remove-Item -Recurse -Force -ErrorAction Ignore ..\..\..\bochscpu\bochs
Remove-Item -Recurse -Force -ErrorAction Ignore ..\..\..\bochscpu\lib

New-Item -ItemType Directory -Name ..\..\..\bochscpu\lib
Copy-Item cpu\libcpu.a ..\..\..\bochscpu\lib\cpu.lib
Copy-Item cpu\fpu\libfpu.a ..\..\..\bochscpu\lib\fpu.lib
Copy-Item cpu\avx\libavx.a ..\..\..\bochscpu\lib\avx.lib
Copy-Item cpu\cpudb\libcpudb.a ..\..\..\bochscpu\lib\cpudb.lib
Copy-Item cpu\softfloat3e\libsoftfloat.a ..\..\..\bochscpu\lib\softfloat.lib

New-Item -ItemType Directory -Name ..\..\..\bochscpu\bochs
Copy-Item -Recurse -Force . ..\..\..\bochscpu

Set-Location ..\..\..\bochscpu-ffi
cargo clean
cargo build --jobs $env:NUMBER_OF_PROCESSORS
cargo build --jobs $env:NUMBER_OF_PROCESSORS --release

Pop-Location
