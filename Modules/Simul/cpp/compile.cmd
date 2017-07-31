@echo off

if exist build rmdir /S /Q build
if %errorlevel% neq 0 goto exit
mkdir build
if %errorlevel% neq 0 goto exit
cd build
if %errorlevel% neq 0 goto exit
cmake -G "MinGW Makefiles" ..
if %errorlevel% neq 0 goto exit
mingw32-make
if %errorlevel% neq 0 goto exit
move pyry3d_cpp.py .. > nul
if %errorlevel% neq 0 goto exit
move _pyry3d_cpp.pyd .. > nul
if %errorlevel% neq 0 goto exit

:exit
pause
