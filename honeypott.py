
import socket
import threading
import time
import random
import os
import sys

def warning(msg):
    print(f"[!] {msg}")

def main():
    print("\n Honeypot Based Secure Network System \n")
    if os.geteuid() != 0:
        warning("You must run Honeypot with root privileges.\n")
    print(" Select option.\n")
    print("1- Fast Auto Configuration")
    print("2- Manual Configuration [Advanced Users, more options]\n")
    choice = input("   -> ").strip()

    if choice == '1':
        access = random.randrange(3)
        if access == 0:
            msg = ("<HEAD>\n<TITLE>Access denied</TITLE>\n</HEAD>\n"
                   "<H2>Access denied</H2>\n"
                   "<H3>HTTP Referrer login failed</H3>\n"
                   "<H3>IP Address login failed</H3>\n"
                   "<P>\n" + time.ctime() + "\n</P>")
        elif access == 1:
            msg = ("<HEAD>\n<TITLE>Access denied</TITLE>\n</HEAD>\n"
                   "<H2>Access denied</H2>\n"
                   "<H3>IP Address login failed</H3>\n"
                   "<P>\n" + time.ctime() + "\n</P>")
        else:
            msg = ("<HEAD>\n<TITLE>Access denied</TITLE>\n</HEAD>\n"
                   "<H2>Access denied</H2>\n"
                   "<P>\n" + time.ctime() + "\n</P>")
        honeyconfig(24, msg, sound='n', log='n', logname='')

    elif choice == '2':
        print("\n Insert port to Open.\n")
        port_str = input("   -> ").strip()
        try:
            port = int(port_str)
        except ValueError:
            print("\n Invalid port.\n")
            sys.exit(1)

        print("\n Insert false message to show.\n")
        message = input("   -> ")

        print("\n Save a log with intrusions? (y/n)\n")
        log = input("   -> ").strip().lower()
        logname = ""
        if log == 'y':
            print("\n Log file name? (incremental)")
            print(" Default: ./log_honeypot.txt\n")
            logname_in = input("   -> ").strip()
            if logname_in:
                logname = logname_in
            else:
                logname = os.path.join(os.path.dirname(__file__), 'log_honeypot.txt')

        print("\n Activate beep() sound when intrusion? (y/n)\n")
        sound = input("   -> ").strip().lower()

        honeyconfig(port, message, sound, log, logname)

    else:
        print("\n Invalid option.\n")

def honeyconfig(port, message, sound, log, logname):
    """Function to launch the Honeypot."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(5)
        print()
        print(f"  HONEYPOT ACTIVATED ON PORT {port} ({time.ctime()})\n")
        if log.lower() == 'y':
            try:
                with open(logname, 'a') as lf:
                    lf.write("#Honeypot log\n\n")
                    lf.write(f"  HONEYPOT ACTIVATED ON PORT {port} ({time.ctime()})\n\n")
            except OSError:
                print("\n Saving log error: No such file or directory.\n")

        def handle_client(client_sock, addr):
            time.sleep(1)  # mitigate DoS
            remote_ip, remote_port = addr
            print()
            print(f"  INTRUSION ATTEMPT DETECTED! from {remote_ip}:{remote_port} ({time.ctime()})")
            print(" -----------------------------")
            try:
                data = client_sock.recv(1024).decode(errors='ignore')
            except:
                data = ''
            print(data)
            if sound.lower() == 'y':
                # beep 3 times
                sys.stdout.write('\a\a\a')
                sys.stdout.flush()
            if log.lower() == 'y':
                try:
                    with open(logname, 'a') as lf:
                        lf.write("\n")
                        lf.write(f"  INTRUSION ATTEMPT DETECTED! from {remote_ip}:{remote_port} ({time.ctime()})\n")
                        lf.write(" -----------------------------\n")
                        lf.write(data + "\n")
                except OSError:
                    print("\n Saving log error: No such file or directory.\n")
            time.sleep(2)  # sticky honeypot
            try:
                client_sock.sendall(message.encode())
            except:
                pass
            client_sock.close()

        while True:
            client, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(client, addr))
            t.daemon = True
            t.start()

    except PermissionError:
        print("\n Error: Honeypot requires root privileges.\n")
    except OSError as e:
        if e.errno == 98:
            print("\n Error: Port in use.\n")
        else:
            print(f"\n Unknown error: {e}\n")
    except Exception as e:
        print(f"\n Unknown error: {e}\n")



