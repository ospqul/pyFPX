# OpenView SDK in Python

This is a very simple python script to control Focus PX with OpenView SDK. It demonstrates how to connect device, create conventional beamset, start acquisition and collect ascan data.

#### Include .Net Library

Copy `OlympusNDT.Instrumentation.NET.dll` in the same folder next to this script.

The library's default path is:

`C:\OlympusNDT\OpenView SDK\1.0\Bin\.NET\OlympusNDT.Instrumentation.NET.dll`

#### 64-bit Python

Since OpenView SDK provide 64-bit library, please use 64-bit python.

#### Dependencies

The required dependencies are included in `requirements.txt` file:

- [numpy](https://numpy.org/)==1.19.0
- [pythonnet](https://github.com/pythonnet/pythonnet)==2.5.1

Run `$ pip install -r requirements.txt` to install required dependencies.

#### Run

`$ python.exe .\FPXDevice.py`