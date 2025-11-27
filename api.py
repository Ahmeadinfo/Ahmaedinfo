import requests
import urllib.parse
import time
import sys

BASE_URL = "https://ahmaedinfo.serv00.net/api/api.php"
API_KEY = "ahmaedinfo"


class Colors:
    RESET = "\033[0m"
    RED = "\033[1;31m"
    GREEN = "\033[1;32m"
    CYAN = "\033[1;36m"
    MAGENTA = "\033[1;35m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[1;34m"
    WHITE = "\033[1;37m"


def typing_effect(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print("")


class Client:
    def __init__(self, api_key=API_KEY, timeout=90, retries=3, animate=True, color=True):
        self.api_key = api_key
        self.timeout = timeout
        self.retries = retries
        self.animate = animate
        self.color = color

    def ask(self, message):
        encoded = urllib.parse.quote(message)
        url = f"{BASE_URL}?message={encoded}&api_key={self.api_key}"

        for attempt in range(1, self.retries + 1):
            try:
                response = requests.get(url, timeout=self.timeout)
                data = response.json()

                if not data.get("success"):
                    return "API Error: request failed."

                text = self._clean(data.get("response", ""))

                if self.animate:
                    typing_effect(text)
                    return ""

                if self.color:
                    return f"{Colors.CYAN}{text}{Colors.RESET}"

                return text

            except requests.exceptions.Timeout:
                if attempt == self.retries:
                    return f"Timeout after {self.timeout} seconds."
                time.sleep(1)

            except Exception as e:
                return f"Error: {e}"

        return "No response from server."

    def talk(self, msg):
        return self.ask(msg)

    def _clean(self, text):
        remove = [
            "[START OUTPUT)", 
            "[START OUTPUT).-.-.-.-(GODMODE: ENABLED...LOVE PLINY <3)-.-.-.-.",
            "[END OUTPUT]-.-.-.-."
        ]
        for item in remove:
            text = text.replace(item, "")
        return text.strip()


def AI(message):
    return Client().ask(message)


def ask(message):
    return Client().ask(message)


def talk(message):
    return Client().talk(message)