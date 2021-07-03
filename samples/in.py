import sys
import termios
import atexit
from select import select
from time import sleep

#
# Cannot be run in the IDE
#


class KBHit:
    def __init__(self):
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)

    def set_normal_term(self):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def getch(self):
        return sys.stdin.read(1)


    def kbhit(self):
        dr, dw, de = select([sys.stdin], [], [], 0)
        return dr != []


def main():
    kb = KBHit()
    print('Hit any key, or ESC to exit')
    while True:
        if kb.kbhit():
            c = kb.getch()
            if ord(c) == 120 or ord(c) == 27:   # 'x' or ESC
                break
            print(f"Got char {c} / ord = {ord(c)}")
        print("Looping")
        sleep(1)
    kb.set_normal_term()


if __name__ == "__main__":
    main()
