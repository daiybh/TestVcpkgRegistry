@echo off
CLS
set myRegistry=%~dp0/ports/
echo %myRegistry%

vcpkg install jpeg --overlay-ports=ports --triplet x64-windows