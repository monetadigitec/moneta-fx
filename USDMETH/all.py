from subprocess import Popen, CREATE_NEW_CONSOLE


p1 = Popen("python.exe usdmeth1.py",creationflags=CREATE_NEW_CONSOLE)
p2 = Popen("python.exe  usdmeth2.py",creationflags=CREATE_NEW_CONSOLE)
p1.wait()
p2.wait()