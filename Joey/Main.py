import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.weapons = {"Pistol": 10, "Shotgun": 20, "Rifle": 30}
    
    def attack(self, opponent):
        weapon = random.choice(list(self.weapons.keys()))
        damage = self.weapons[weapon]
        opponent.health -= damage
        print(f"{self.name} shoots {opponent.name} with a {weapon} for {damage} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} is eliminated!")

# Initialize players
player1 = Player("Cowboy")
player2 = Player("Bandit")

# Game loop
round_num = 1
while player1.health > 0 and player2.health > 0:
    print(f"\nRound {round_num}")
    if random.choice([True, False]):
        player1.attack(player2)
    else:
        player2.attack(player1)
    print(f"{player1.name} Health: {player1.health} | {player2.name} Health: {player2.health}")
    round_num += 1

# Determine winner
winner = player1.name if player1.health > 0 else player2.name
print(f"\n{winner} wins the shootout!")




