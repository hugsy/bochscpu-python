$ErrorActionPreference = "Stop"

Push-Location

New-Item -ItemType Directory -Name bxbuild
Set-Location bxbuild

bash -c "
git clone https://github.com/hugsy/bochscpu-build.git &&
git clone https://github.com/hugsy/bochscpu.git &&
git clone https://github.com/hugsy/bochscpu-ffi.git &&
cd bochscpu-build && bash prep.sh && cd Bochs/bochs && bash .conf.cpu-msvc
"

Set-Location bochscpu-build\Bochs\bochs
$env:CL = "/MP"
nmake

Remove-Item -Recurse -Force -ErrorAction Ignore ..\..\..\bochscpu\bochs
Remove-Item -Recurse -Force -ErrorAction Ignore ..\..\..\bochscpu\lib

New-Item -ItemType Directory -Name ..\..\..\bochscpu\lib
Copy-Item cpu\libcpu.a ..\..\..\bochscpu\lib\cpu.lib
Copy-Item cpu\fpu\libfpu.a ..\..\..\bochscpu\lib\fpu.lib
Copy-Item cpu\avx\libavx.a ..\..\..\bochscpu\lib\avx.lib
Copy-Item cpu\cpudb\libcpudb.a ..\..\..\bochscpu\lib\cpudb.lib

New-Item -ItemType Directory -Name ..\..\..\bochscpu\bochs
robocopy . ..\..\..\bochscpu\bochs /e

Set-Location ..\..\..\bochscpu-ffi
cargo clean
cargo build -j $env:NUMBER_OF_PROCESSORS
cargo build -j $env:NUMBER_OF_PROCESSORS --release

Pop-Location
