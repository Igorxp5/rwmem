from sys import platform
if platform != 'win32':raise Exception("rwmem: Error: Unsupported Operating System : expected 'Windows'")
from rwmem import *
__version__ = "0.0.5"
memory = Memory()
