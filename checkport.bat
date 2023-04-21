@echo off
CLS
set myRegistry=%~dp0/ports/
echo %myRegistry%
vcpkg install videoframe --overlay-ports=ports --triplet x64-windows