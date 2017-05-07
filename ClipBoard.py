import time
import os
import signal


def clipboard_clear():
    time.sleep(5)
    os.system("echo %s | pbcopy" %"")
    return True

def to_clipboard(password):
    pid = os.fork()
    if pid == 0:
        clipboard_clear()
        os.kill(pid, signal.SIGTERM)
    else:
        os.system("echo %s | pbcopy" %password)

    return True