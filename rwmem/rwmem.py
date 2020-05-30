import struct
from os import path
from ctypes import *
from ctypes.wintypes import *


psapi = WinDLL('Psapi.dll')
EnumProcesses = psapi.EnumProcesses
EnumProcesses.restype = BOOL
GetProcessImageFileName = psapi.GetProcessImageFileNameA
GetProcessImageFileName.restype = DWORD


k32 = WinDLL('kernel32', use_last_error=True)

remem = k32.ReadProcessMemory
remem.argtypes = [HANDLE, LPCVOID, LPVOID, c_size_t, POINTER(c_size_t)]
remem.restype = BOOL

wrmem = k32.WriteProcessMemory
wrmem.argtypes = [HANDLE, LPVOID, LPCVOID, c_size_t, POINTER(c_size_t)]
wrmem.restype = BOOL

PROCESS_ALL_ACCESS = 0x1F0FFF


class ModuleEntry32(Structure):
       _fields_ = [ ( 'dwSize' , DWORD ) ,
                ( 'th32ModuleID' , DWORD ),
                ( 'th32ProcessID' , DWORD ),
                ( 'GlblcntUsage' , DWORD ),
                ( 'ProccntUsage' , DWORD ) ,
                ( 'modBaseAddr' , POINTER(c_ulong)) ,
                ( 'modBaseSize' , DWORD ) ,
                ( 'hModule' , HMODULE ) ,
                ( 'szModule' , c_char * 256 ),
                ( 'szExePath' , c_char * 260 ) ]


class Memory(object):


    def __init__(self,hProcess=None):
        self.hProcess = hProcess


    def open(self, dwProcessId):
        if self.hProcess:self.close()
        if isinstance(dwProcessId, str):
            if not dwProcessId.isdigit():
                dwProcessId = self.getPidOf(dwProcessId)
            dwProcessId = int(dwProcessId)
        if not isinstance(dwProcessId, int):raise TypeError("open(): Error: expected an 'int' or 'str' of ProcessID not '{}'".format(type(dwProcessId).__name__))
        self.hProcess = k32.OpenProcess(PROCESS_ALL_ACCESS, 0 ,int(dwProcessId))


    def close(self, handle=None):
        if not handle:
            if self.hProcess:
                k32.CloseHandle(self.hProcess)
                self.hProcess = None
        else:
           k32.CloseHandle(handle)
           if handle == self.hProcess: self.hProcess = None

    GetLastError  = staticmethod(lambda: WinError(k32.GetLastError()))


    def check(self,funcName, exp=False):
        if not exp:
          if not self.hProcess:raise Exception("{}(): Error: Process handle is not open yet !!!".format(funcName))
        else:
          err = self.GetLastError()
          if err.winerror != 0:raise Exception('{}(): {}'.format(funcName,err))


    def getPidOf(self,processName):
            pid = listProc(find=processName)
            if not pid:raise Exception("getPidOf(): Error: The process '{}' is not running!".format(processName))
            return pid


    def getTypeInfo(self,TYPE):
        TYPE = TYPE.lower()
        if TYPE in ("c", "char"): return '<c', 1
        elif TYPE in ("uc", "uchar"): return '<B',1
        elif TYPE in ("s", "short"): return '<h',2
        elif TYPE in ("us", "ushort"): return '<H',2
        elif TYPE in ("i", "int"): return '<i',4
        elif TYPE in ("ui","uint"):return ('<I',4) if self.getProcessArch() == 32 else ('>I',4)
        elif TYPE in ("f", "float"):return '<f',4
        elif TYPE in ("l", "long"):return '<l',4
        elif TYPE in ("ul", "ulong"): return '<L', 4
        elif TYPE in ("ll","longlong"): return '<q',8
        elif TYPE in ("ull","ulonglong"): return '<Q',8
        elif TYPE in ("d", "double"):return '<d',8
        else: raise Exception("getTypeInfo(): Error: Unsupported data type '{}'".format(TYPE))


    def getProcessArch(self):
        self.check("getProcessArch")
        bits = c_int32()
        try:
            k32.IsWow64Process(self.hProcess, byref(bits))
            return 32 if bits.value else 64
        except Exception as e:raise Exception("getProcessArch(): Error: {}".format(e))


    def readBytes(self, lpBaseAddress, length):
        self.check("readBytes")
        buffer = create_string_buffer(length)
        bytes_read = c_size_t()
        remem(self.hProcess, lpBaseAddress, buffer, length, byref(bytes_read))
        data = buffer.raw
        if not data: self.check("readBytes", exp=True)
        return data


    def readStr(self, lpBaseAddress, length=50):
        buff = self.readBytes(lpBaseAddress, length)
        i = buff.find(b'\x00')
        if i != -1:buff = buff[:i]
        return  str(buff.decode())


    def read(self, lpBaseAddress, TYPE="ui"):
      self.check("read")
      sin,size = self.getTypeInfo(TYPE)
      if not size:raise Exception("read(): Error: invalid Data Size")
      buffer = create_string_buffer(size)
      bytes_read = c_size_t()
      remem(self.hProcess, lpBaseAddress, buffer, size, byref(bytes_read))
      data = struct.unpack(sin, buffer[0:size])[0]
      if not data:self.check("read", exp=True)
      return data


    def writeBytes(self, lpBaseAddress, Value):
          self.check("writeBytes")
          Value = str(Value).encode("utf-8")
          c_data = c_char_p(Value)
          c_data_ = cast(c_data, POINTER(c_char))
          if not wrmem(self.hProcess, lpBaseAddress, c_data_, len(Value), None):self.check("writeBytes", exp=True)


    def write(self, lpBaseAddress, Value, TYPE="ui"):
      self.check("write")
      sin,size = self.getTypeInfo(TYPE)
      c_data = c_char_p(struct.pack(sin, Value))
      c_data_ = cast(c_data, POINTER(c_char))
      if not wrmem(self.hProcess,lpBaseAddress,c_data_,size,None):self.check("write", exp=True)


def listProc(Value=None,find=None):
        count = 32
        while True:
            ProcessIds = (DWORD*count)()
            cb =sizeof(ProcessIds)
            BytesReturned = DWORD()
            if EnumProcesses(byref(ProcessIds), cb, byref(BytesReturned)):
                if BytesReturned.value<cb:
                    break
                else:count *= 2
            else:raise Exception("getPidOf(): Error: Call to EnumProcesses failed")
        if not find:
            LAYOUT ="{!s:10} {!s:70}"
            print(LAYOUT.format(*["ProcessId","ProcessName"]))
            print(LAYOUT.format(*["---------","-----------"]))
        for index in range(BytesReturned.value // sizeof(DWORD)):
            ProcessId = ProcessIds[index]
            hProcess = k32.OpenProcess(PROCESS_ALL_ACCESS,0, ProcessId)
            if hProcess:
                ImageFileName = (c_char*260)()
                if GetProcessImageFileName(hProcess, ImageFileName, MAX_PATH)>0:
                    filename = path.basename(ImageFileName.value)
                    if find:
                        k32.CloseHandle(hProcess)
                        if (isinstance(find, int)) or (isinstance(find, str) and find.isdigit()):
                            if int(find) == int(ProcessId):return filename
                        elif isinstance(find, str):
                            if find in str(filename):return ProcessId
                        else:raise TypeError("expected 'str' of processName or 'int' of ProcessID not '{}'".format(type(find).__name__))
                    elif Value:
                        if (isinstance(Value, int)) or (isinstance(Value, str) and Value.isdigit()):
                            if int(Value) == int(ProcessId):
                                print("  "+ LAYOUT.format(*[ProcessId, filename]))
                        elif isinstance(Value, str):
                            if str(Value) in str(filename):
                                print("  "+ LAYOUT.format(*[ProcessId, filename]))
                        else:raise TypeError("expected 'str' of processName or 'int' of ProcessID not '{}'".format(type(Value).__name__))
                    else:print("  "+ LAYOUT.format(*[ProcessId, filename]))
                k32.CloseHandle(hProcess)
        if find:return False

def getModuleBaseOf(ModuleName,PID):
    hModuleSnap = k32.CreateToolhelp32Snapshot( 0x00000010 | 0x00000008, PID );
    me32 = ModuleEntry32()
    me32.dwSize = sizeof(ModuleEntry32)
    k32.Module32First( hModuleSnap, byref(me32))
    base = None
    while True:
        if (me32.szModule.lower()==ModuleName.lower()):
            base=me32.modBaseAddr
            break
        if not k32.Module32Next(hModuleSnap, byref(me32)):break
    k32.CloseHandle(hModuleSnap)
    if not base:raise Exception("getModuleBaseOf(): Error: unable to find Module Base Address Of '{}' ".format(ModuleName))
    return "0x{:08X}".format((addressof(base.contents)))
memory = Memory()
