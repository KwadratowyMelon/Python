import requests
import time
from rich.console import Console
import rich.traceback

console = Console()
console.clear()
rich.traceback.install()

sell = {'content': ";s"}
upPickaxe = {'content': ";up p a"}
upBackpack = {'content': ";up b a"}
hunt = {'content': ";h"}
fish = {'content': ";f"}
quiz = {'content': ";q"}
answer = {'content': "a"}

header = {
    'authorization': ''#tu wstawic klucz autoryzacji
}
x = "https://discord.com/api/v9/channels/876116800734134335/messages"

def multi_decor(f, g, h, e):
   def many_things():
       for i in range(60):
        f()
        print(f"wykonala sie funkcja {f.__name__}")
        g()
        print(f"wykonala sie funkcja {g.__name__}")
        time.sleep(20)
        g()
        print(f"wykonala sie funkcja {g.__name__}")
        time.sleep(20)
        h()
        print(f"wykonala sie funkcja {h.__name__}")
        time.sleep(20)
        if i % 5 == 0:
            e()
            print(f"wykonala sie funkcja {e.__name__}")
        else:
            pass

        print(f"zakonczono {i+1} cykl")
        print("reset terminalu za 3 sekundy")
        for j in range(3):
            print(3-j)
            time.sleep(1)

        console.clear()
      
   return many_things


def Hunting():
    r = requests.post(x, data=hunt, headers=header)
    time.sleep(0.2)

def Pick_up():
    r = requests.post(x, data=sell, headers=header)
    time.sleep(0.5)
    r = requests.post(x, data=upPickaxe, headers=header)

def Back_up():
    r = requests.post(x, data=sell, headers=header)
    time.sleep(0.5)
    r = requests.post(x, data=upBackpack, headers=header)

def Fishing():
    r = requests.post(x, data=fish, headers=header)
    time.sleep(0.2)


sequenced_func = multi_decor(Hunting, Pick_up, Back_up, Fishing)
sequenced_func()
