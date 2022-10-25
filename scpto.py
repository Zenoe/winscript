#!/usr/bin/env python3

import sys
import subprocess
if __name__ == '__main__':
    # in case of space sperated path
    filepath=' '.join(sys.argv[1:])
    print ( filepath )
    # print (filepath)
    linuxPath = filepath.replace('C:', '/cygdrive/c').replace('\\','/')
    print (linuxPath)
    subprocess.run([r"C:\Apps\cygwin\bin\bash.exe", "-l",'-c',"scp -r -o StrictHostKeyChecking=no '%s' root@10.110.198.50:~/fromwindows"%linuxPath])
