***

**Module**: rwmem

   **JOB**: Read/Write Process Memory for **Windows Python**
***

**installation**:
   - pip install rwmem

***

**Usage**

```python
from rwmem import *


memory.open()
"""
Open a handle for an process, you can select  the process by it name or process id
Examples:
   memory.open(7696)
   memory.open("someGame")

"""

memory.close()
"""
Close the open process handle
"""

listProc()
"""
[*] JOB: list processes with its process id
[*] without Value Parm: list all processes
[*] With Value Parm:
       memory.listProc(Value="SomeGame")
       ProcessId  ProcessName
       ---------  -----------
         7696       SomeGame.exe
       >>>
       memory.listProc(Value=7696)

"""

memory.getProcessArch()
"""
[*] JOB: Get the open process architecture
[*] Example:
     memory.getProcessArch()
     64
     >>>
"""

memory.read()
"""
[*] JOB: Read Process memory Address Value
[*] Parms:
     1 - Address
     2 - TYPE Default(<U_INT>)
     [*] Examples:
        memory.read(0x11111111)
        100
        >>>
        memory.read(0x11111111, TYPE="float")
        100.0
"""

memory.readStr()
"""
[*] JOB: Read string values
[*] Parms:
     1 - Address
     2 - length Default(<50>)
     [*] Examples:
           memory.readStr(0x11111111)
           'helloWorld'
           >>>
          memory.readStr(0x11111111, length=100)
          'helloWorld I Love python'
          >>>
"""

memory.readBytes()
"""
[*] JOB: Read process memory Address bytes
[*] Parms:
     1 - Address
     2 - length
     [*] Example:
          memory.readBytes(0x11111111, length=11)
          'helloWorld\x00'
          >>>
"""

memory.write()
"""
[*] JOB: Write some value to process memory Address
[*] Parms:
     1 - Address
     2 - Value
     3 - TYPE Default(<U_INT>)
     [*] Examples:
        memory.write(0x11111111, 100)
        memory.write(0x11111111, 100.0 , TYPE="float")
"""

memory.writeBytes()
"""
[*] JOB: Write some bytes value to process memory Address
[*] Parms:
     1 - Address
     2 - Value
     [*] Example:
        memory.writeBytes(0x11111111, "helloWorld")
"""

getModuleBaseOf()
"""
[*] JOB: returns the module base address
[*] Parms:
     1 - Module Name
     2 - PID
     [*] Example:
        getModuleBaseOf("someGame.exe", 7696)
        '0x1C580000'
        >>>
"""
```

***

**That's All :)**
   * This Module Coded By Oseid Aldary
   * Thanks For Usage
   * Have A Nice Day...GoodBye :)
