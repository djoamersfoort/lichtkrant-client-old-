import argparse
import socket
from pynput import keyboard


class SnakeClient:
    def __init__(self, ip):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, 1029))
            self.s = s

            while True:
                with keyboard.Listener(on_release=self.on_release) as Listener:
                    Listener.join()

    def on_release(self, key):
        self.s.sendall(str(key)[1].encode())


class PongClient:
    def __init__(self, ip):
        self.keys = {"w": False, "s": False}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, 9999))
        while True:
            with keyboard.Listener(on_release=self.on, on_press=self.off) as l:
                l.join()

    def on(self, key):
        if hasattr(key, "char") and key.char in self.keys:
            self.keys[key.char] = False
            self.send()

    def off(self, key):
        if hasattr(key, "char") and key.char in self.keys:
            self.keys[key.char] = True
            self.send()

    def current(self):
        if self.keys["w"] and self.keys["s"]:
            return b"c"
        if self.keys["w"]:
            return b"w"
        if self.keys["s"]:
            return b"s"
        return b"c"

    def send(self):
        self.sock.sendall(self.current())


class TetrisClient:
    def __init__(self, ip):
        self.keys = {
            "w": False,
            "a": False,
            "s": False,
            "d": False,
            "e": False,
            " ": False
        }
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, 7777))
        self.send()
        while True:
            with keyboard.Listener(on_release=self.on, on_press=self.off) as l:
                l.join()

    def on(self, key):
        if hasattr(key, "char"):
            if key.char in self.keys:
                self.keys[key.char] = False
                self.send()
        elif key == keyboard.Key.space:
            self.keys[" "] = False
            self.send()

    def off(self, key):
        if hasattr(key, "char"):
            if key.char in self.keys:
                self.keys[key.char] = True
                self.send()
        elif key == keyboard.Key.space:
            self.keys[" "] = True
            self.send()

    def msg(self):
        return "".join([
            f"{int(value)}" for key, value in self.keys.items()
        ]).encode()

    def send(self):
        self.sock.sendall(self.msg())


class SplashClient:
    def __init__(self, ip):
        self.keys = {"a": False, "d": False, "w": False}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, 42069))
        self.send()
        while True:
            with keyboard.Listener(on_release=self.on, on_press=self.off) as l:
                l.join()

    def on(self, key):
        if hasattr(key, "char") and key.char in self.keys:
            self.keys[key.char] = False
            self.send()

    def off(self, key):
        if hasattr(key, "char") and key.char in self.keys:
            self.keys[key.char] = True
            self.send()

    def msg(self):
        return "".join([
            f"{int(value)}" for key, value in self.keys.items()
        ]).encode()

    def send(self):
        self.sock.sendall(self.msg())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", nargs="?", help="ip of the pong server")
    args = parser.parse_args()
    host = "100.64.0.65"
    if "ip" in args and args.ip:
        host = args.ip

    games = ["Snake", "Pong", "Tetris", "Splash"]
    gameindex = None
    for index, game in enumerate(games):
        print(f"[{index + 1}] {game}")
    while gameindex is None:
        print("")
        game = input("Enter game id: ")
        try:
            index = int(game) - 1
            if index < len(games):
                gameindex = index
            else:
                print("That option is not in the list!")
        except ValueError:
            print("That option is not in the list!")

    print(f"Connecting to {host}")
    try:
        if gameindex == 0:
            SnakeClient(host)
        if gameindex == 1:
            PongClient(host)
        if gameindex == 2:
            TetrisClient(host)
        if gameindex == 3:
            SplashClient(host)
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    main()
