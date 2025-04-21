# Importing a module to create random numbers (for fighting)
import random

# Class to define items like a knife or banana
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

# Class to define enemies like panther or snake
class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def is_alive(self):
        return self.health > 0

# Class to define each room in the game
class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []
        self.enemies = []
        self.paths = {}

    # Connect this room to another room
    def connect_room(self, direction, room):
        self.paths[direction] = room

    # Show what’s in the room
    def describe(self):
        print(f"\nYou are in the {self.name}")
        print(self.description)
        if self.items:
            print("Items here:")
            for item in self.items:
                print(f"- {item.name}: {item.description}")
        if self.enemies:
            for enemy in self.enemies:
                if enemy.is_alive():
                    print(f"A {enemy.name} is here!")
        print("Exits:", ", ".join(self.paths.keys()))

# Class to define the player
class Player:
    def __init__(self, start_room):
        self.current_room = start_room
        self.health = 100
        self.inventory = []

    # Move to another room
    def go(self, direction):
        if direction in self.current_room.paths:
            self.current_room = self.current_room.paths[direction]
            self.current_room.describe()
        else:
            print("You can't go that way.")

    # Take an item from the room
    def take(self, item_name):
        for item in self.current_room.items:
            if item.name == item_name:
                self.inventory.append(item)
                self.current_room.items.remove(item)
                print(f"You took the {item.name}.")
                return
        print("That item is not here.")

    # Fight an enemy in the room
    def fight(self, enemy_name):
        for enemy in self.current_room.enemies:
            if enemy.name == enemy_name and enemy.is_alive():
                print(f"You fight the {enemy.name}!")
                while enemy.is_alive() and self.health > 0:
                    enemy.health -= random.randint(5, 15)
                    print(f"You hit the {enemy.name}. Its health is now {enemy.health}.")
                    if enemy.is_alive():
                        damage = random.randint(1, enemy.attack)
                        self.health -= damage
                        print(f"{enemy.name} hits you! Your health is now {self.health}.")
                    else:
                        print(f"You defeated the {enemy.name}!")
                return
        print("No enemy like that here.")

    # Show your inventory
    def show_inventory(self):
        if self.inventory:
            print("You have:")
            for item in self.inventory:
                print(f"- {item.name}")
        else:
            print("You are carrying nothing.")

# ---- Game Setup Below ----

# Create items
knife = Item("knife", "A sharp jungle knife.")
banana = Item("banana", "Tasty and might give you energy.")

# Create enemies
panther = Enemy("panther", 30, 10)
snake = Enemy("snake", 20, 6)

# Create rooms
camp = Room("Camp", "A small campsite with a fire.")
jungle = Room("Jungle", "Tall trees and jungle sounds.")
cave = Room("Cave", "Dark and full of echoes.")
river = Room("River", "A wide river flowing fast.")

# Connect rooms
camp.connect_room("north", jungle)
jungle.connect_room("south", camp)
jungle.connect_room("east", cave)
jungle.connect_room("north", river)
cave.connect_room("west", jungle)
river.connect_room("south", jungle)

# Add items and enemies to rooms
camp.items.append(knife)
cave.items.append(banana)
jungle.enemies.append(panther)
cave.enemies.append(snake)

# Start the game with the player in the camp
player = Player(camp)
print("🌴 Welcome to the Jungle Adventure Game!")
player.current_room.describe()

# Game loop
while True:
    command = input("\nWhat do you want to do? ").lower()

    if command == "quit":
        print("Thanks for playing!")
        break
    elif command.startswith("go "):
        direction = command.split(" ")[1]
        player.go(direction)
    elif command.startswith("take "):
        item_name = command.split(" ")[1]
        player.take(item_name)
    elif command.startswith("fight "):
        enemy_name = command.split(" ")[1]
        player.fight(enemy_name)
    elif command == "inventory":
        player.show_inventory()
    elif command == "health":
        print(f"Your health is {player.health}")
    else:
        print("Commands: go [direction], take [item], fight [enemy], inventory, health, quit")

