<b>Task</b>: design a set of test cases for owner/permission/content modification testing of NFS4 file system. Implement them.

<b>Test cases</b>: https://kb.epam.com/display/FLKMWD/Test+task+documentation%3A+test+cases

<b>Necessary Python versions</b>: Python 3.5.2, pytest-3.6.4, py-1.5.4, pluggy-0.7.1

<b>Necessary environment</b>: a Linux-based computer (it should be a NFS-server), a Linux-based virtual machine (it should be a NFS-client) installed on it. They should be connected via a network. A Linux-based computer (a NFS-server) should have ssh. A Linux-based virtual machine should have ssh and 2 network adapters (NAT and a Host-only adapter named vboxnet0 (by default)). A programme should be executed on a Linux-based computer (a NFS-server). 

<b>Necessary steps for NFS installation</b>:
  1. To install NFS on both a server (a Linux-based computer) and a client (a Linux-based virtual machine) on Ubuntu 16.04 (for example) you can run a command "sudo apt install nfs-kernel-server nfs-common"
  2. Check (on both a server and a client) if a NFS-server is correctly installed. You can do it with a command "rpcinfo -p | grep nfs"
  3. Check (on both a server and a client) if NFS is supported on a kernel level. You can do it with a command "cat /proc/filesystems | grep nfs". If it is not supported on a kernel level, run a command "modprobe nfs" to load a kernel's module manually


<b>Necessary steps for a programme execution</b>: 
  1. Prepare a Linux-based computer (as a NFS-server) and a Linux-based virtual machine (as a NFS-client) according with a necessary environment described above.  
  2. Download all the files from the project
  3. Paste them in one directory
  4. Paste a necessary value to a server_IP variable in a conftest.py file
  4. In a directory with the project open a terminal. Run there "pytest ./test_1.py --clientIP="192.168.56.102" --clientPort="22" --clientName="bobs" --clientPassword="flylesenok" --log-file=/home/polina/fileWithLogs --clientIP="192.168.56.1"", where in --clientIP, --clientPort, --clientName, --clientPassword, --log-file write your values.
  
 <b>Additional information</b>:
 --clientIP means an IP (in my case enp0s8 was used) of a Linux-based virtual machine (a NFS-client); 
 --clientPort - write down yours (of a Linux-based virtual machine (a NFS-client)) if specified, if not - write down 22 (it is a default);
 --clientName - means a user on a Linux-based virtual machine (a NFS-client), but not root;
 --clientPassword - means a password of a user on a Linux-based virtual machine (a NFS-client). 
 --log-file - means a file, where all logs will be stored
