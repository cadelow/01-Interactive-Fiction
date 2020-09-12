#!/usr/bin/env python3
import sys,os,json,re
assert sys.version_info >= (3,8), "This script requires at least Python 3.8"
score = 50

def load(l):
    f = open(os.path.join(sys.path[0], l))
    data = f.read()
    j = json.loads(data)
    return j

def find_passage(game_desc, pid):
    for p in game_desc["passages"]:
        if p["pid"] == pid:
            return p
    return {}

# ------------------------------------------------------

def update(current, game_desc, choice):
    global score
    if choice == "":
        return current
    if int(current["pid"]) < 14:
        for l in current["links"]:
            if choice == l["name"].lower():
                current = find_passage(game_desc, l["pid"])
                score += l["effect"]
                if current:
                    return current
    print("\n\n---------------------\n\nI don't understand what you are asking me to do. Please try again.")
    return current

def render(current):
    global score
    print(current["text"])
    if score > 0:
        print("Your relationship with Anna: " + str(score) + "/100")
    
def get_input(current):
    global score
    if score > 0:
        choice = input("\nWhat would you like to do? (type your choice in number, or quit to exit) ")
        choice = choice.lower()
        if choice in ["quit","q","exit"]:
            return "quit"
        return choice

# ------------------------------------------------------

def main():
    global score
    game_desc = load("game.json")
    current = find_passage(game_desc, game_desc["startnode"])
    choice = ""

    while choice != "quit" and (score > 0) and current != {} and int(current["pid"]) < 14:
        current = update(current, game_desc, choice)
        render(current)
        if int(current["pid"]) < 14:
            choice = get_input(current)
    
    if int(current["pid"]) >= 14 and score != 0:
        if score < 50:
            print("Anna feels neutral about you. You should try a lot harder if you want to be on her good side.")
        elif score < 70:
            print("Anna thinks you're okay. You should try harder if you want to become friends with them.")
        elif score < 95:
            print("Anna likes you! They think you are a nice person!")
        else:
            print("Anna really likes you! They think you're cool and would love to be one of your closest friends!")

    if score <= 0:
        print("You made a bad first impression! Anna doesn't seem to be too fond of you! :(")

    print("Thanks for playing!")

if __name__ == "__main__":
    main()