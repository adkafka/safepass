import time
import os
import signal


def to_clipboard(password, timeout=60):
    def clipboard_clear():
        time.sleep(timeout)
        os.system("echo %s | pbcopy" %"")
        return True

    pid = os.fork()
    if pid == 0:
        clipboard_clear()
        os.kill(pid, signal.SIGTERM)
    else:
        os.system("echo %s | pbcopy" %password)

    return True
