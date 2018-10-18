
import subprocess

cmd = [ "ping", "-t", "127.0.0.1" ]
p = subprocess.Popen(
    cmd,
    shell=True,
    bufsize=0,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    )

while True:    
    print p.stdout.read(80)
