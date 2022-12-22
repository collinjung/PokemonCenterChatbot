#!/usr/bin/env python3
import time
import random

# Prompt user to input a username until it is valid.
def make_user():
    username = input("Please enter your username (Cannot include spaces or the % symbol!): ")
    while "%" in username or " " in username:
        username = input("Sorry! Your username can't include spaces or the % symbol. Enter a new username: ")
    return username


# Registers account for a new user and appends the info to the accounts.txt file.
def create_account():
    print("Let's register an account so we can heal your Pokemon!")
    username = make_user()
    while check_account(username, "user"):
        try_login = input("Sorry, that username already exists! Would you like to try logging in? Y/N ")
        if (try_login.strip())[0].lower() == "y":
            return
        username = make_user()
    print("Hi " + username + ", nice to meet you! My name is Nurse Joy!")
    password = input("Now, enter a passphrase (Cannot include spaces or the % symbol): ")
    while "%" in password or " " in password:
        password = input("Sorry! Your password can't include spaces or the % symbol. Enter a new password: ")
    print("Your account password is " + password)
    with open("accounts.txt", "a") as f:
        f.write(username + "%" + password + "\n")
    print("Let's run through the login process and get your Pokemon back to full health!")
    print("--------------------------------------------------------------------------------------")
    print("--------------------------------++ Pokemon Center ++----------------------------------")
    print("--------------------------------++  Login here... ++----------------------------------")
    print("--------------------------------------------------------------------------------------")


# Checks the accounts.txt file to see if a given user exists.
def check_account(login, option):
    with open("accounts.txt", "r") as f:
        if option == "login":
            for line in f:
                if line.strip() == login:
                    return True
        elif option == "user":
            for line in f:
                if line.split("%")[0] == login:
                    return True
    return False


# Logs a user into their account allowing access to their party.
def login_account():
    username = input("I will check your account status. Please enter your username: ")
    time.sleep(1)
    while "%" in username or " " in username:
        username = input("Your username can't contain spaces or the % symbol. Please try again: ")
    password = input("Please enter your password: ")
    while "%" in password or " " in password:
        password = input("Your password can't contain spaces or the % symbol. Please enter a valid password: ")
    return username + "%" + password.strip()


# Checks the party.txt file to see if a given user has a registered party.
def check_party(login):
    username = login.split("%")[0]
    with open("party.txt", "r") as f:
        for line in f:
            if line.split("-")[0] == username:
                return line
    return "Does not exist"


# Checks the pokemon.txt database to see if the Pokemon exists.
def pokemon_exists(pokemon):
    with open("pokemon.txt", "r") as f:
        for line in f:
            if pokemon == line.strip().lower():
                return True
    return False


# Checks a string for special characters.
def check_special(check):
    special_characters = "!@#$%^&*()-+?_=,<>/\""
    for c in check:
        if c in special_characters:
            return True
    return False

# Registers a party of valid size and writes the info as a string into the pokemon.txt file.
def register_party(login):
    username = login.split("%")[0]
    print("I'll help you register your party!")
    pokecount = input("How many Pokemon are in your party? ")
    while pokecount.isdigit() is False or int(pokecount) < 1 or int(pokecount) > 6:
        pokecount = input("That's not a valid number of Pokemon! Please enter the number of Pokemon in your party: ")
    print("Please list the names of your Pokemon.")
    party = ""
    for i in range(int(pokecount)):
        pokemon = input("What is your Pokemon in slot " + str(i + 1) + "? Enter the name as it appears in the Pokedex (Not nickname): ").strip().lower()
        max_health = 0
        current_health = 0
        while pokemon_exists(pokemon) is False:
            pokemon = input("That's not a valid Pokemon! Please enter the name of your Pokemon as it appears in the Pokedex: ").strip().lower()
        if pokemon.lower() == "shedinja":
            max_health = 1
        if (input("Does " + pokemon + " have a nickname? Y/N ").strip())[0].lower() == "y":
            pokemon = input("Please enter this Pokemon's nickname. The nickname cannot contain any spaces or special characters: ")
            while " " in pokemon or check_special(pokemon):
                pokemon = input("This nickname contains invalid characters. Please enter a new nickname: ")
        print("Scanning " + pokemon + "...")
        time.sleep(1)
        if max_health != 1:
            max_health = random.randint(10, 255)
        current_health = random.randint(0, max_health)
        print(pokemon + "'s current health is " + str(current_health) + "/" + str(max_health))
        party += "-" + pokemon + "_" + str(current_health) + "/" + str(max_health)
    with open("party.txt", "a") as f:
        f.write(username + party + "\n")

# Searches an info string for information about a user's party.
def get_party(info):
    party = info.split("-")[1:]
    conditions = {}
    for slot in party:
        parts = slot.split("_")
        pokemon = parts[0]
        conditions[pokemon] = [parts[1].split("/")[0], parts[1].split("/")[1].strip()]
    return conditions


# Removes party info from the party.txt file.
def remove_party(login):
    username = login.split("%")[0]
    with open("party.txt", "r") as f:
        lines = f.readlines()
    with open("party.txt", "w") as f:
        for line in lines:
            if line.split("-")[0] != username:
                f.write(line)


# Heals pokemon and updates the information in the party.txt folder.
def heal_pokemon(login, info):
    username = login.split("%")[0]
    new_info = username
    for pokemon in info:
        health = info[pokemon]
        new_info += "-" + pokemon + "_" + health[1] + "/" + health[1]
    remove_party(login)
    with open("party.txt", "a") as f:
        f.write(new_info + "\n")


def main():
    print("+++++++++++++")
    print("+-----------+")
    print("+--Pokemon--+")
    print("+--Center---+")
    print("+-----------+")
    print("+++++++++++++")
    print("Welcome to the Pokemon Center, where we will hear your Pokemon back to full health.")
    time.sleep(0.5)
    first_time = input("Is this your first time here? Y/N ")
    if (first_time.strip())[0].lower() == "y":
        create_account()
    time.sleep(1);
    login = login_account()
    print("Searching for your account...")
    time.sleep(1)
    count = 0
    while check_account(login, "login") is False:
        print("Either your username or password is wrong. Please try again.")
        login = login_account()
        if count > 2:
            new_account = input("Maybe you don't have an account set up! Would you like to create a new account? Y/N/Exit ")
            if new_account[0].lower() == "y":
                create_account()
            elif new_account[0].lower() == "e":
                return
        count += 1
    print("Success! We've found your account.")
    info = check_party(login)
    if info == "Does not exist":
        print("It looks like you don't have any Pokemon registered...")
        if (input("Would you like to register your party now? Y/N ").strip())[0].lower() == "n":
            print("We hope to see you again")
            return
        register_party(login)
        info = check_party(login)
        party_info = get_party(info)
    else:
        print("You have a party registered!")
        print("Here are the health conditions of your party:")
        party_info = get_party(info)
        for pokemon in party_info:
            print("    " + pokemon + " currently has " + party_info[pokemon][0] + " out of " + party_info[pokemon][1] + " HP.")
        if (input("Would you like to register a new party? Y/N ").strip())[0].lower() == "y":
            remove_party(login)
            register_party(login)
    if (input("Would you like me to take your Pokemon? ").strip())[0].lower() == "n":
        print("We hope to see you again")
        return
    print("Okay, I'll take your Pokemon for a few seconds")
    time.sleep(2)
    heal_pokemon(login, party_info)
    print("Your Pokemon are now healed. We hope to see you again.")
    return


if __name__ == '__main__':
    main()
