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
[*] JOB: Open a handle for process, you can select  the process by it name or process id
[*] Examples:
   memory.open(7696)
   memory.open("someGame")

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

memory.close()
"""
Close the open process handle
"""

getPID()
"""
[*] JOB: returns process Id of processName
[*] Example:
      getPID("someGame")
      7692
      >>>
"""

procList()
"""
[*] JOB: list processes with its process id
[*] Parms:
     1 - Value
     2 - find
     Examples:
       procList()
       {1: ('SomeGame.exe', 7692), 2: ('someProg.exe', 1608), 3: ('chrome.exe', 3864)} #..etc
       >>>
       procList(Value="chrome")
       {1: ('chrome.exe', 3864), 2: ('chrome.exe', 5652)}
       >>>
       procList(find="chrome")
       3864
       >>>
       procList(find=3864)
       'chrome.exe'
"""

getModuleBase()
"""
[*] JOB: returns the module base address
[*] Parms:
     1 - moduleName
     2 - PID
     [*] Example:
        getModuleBase("someGame.exe", 7696)
        '0x1C580000'
        >>>
"""
```

***

**That's All :)**
   * This Module By Oseid Aldary
   * Thanks For Usage
   * Have A Nice Day...GoodBye :)
