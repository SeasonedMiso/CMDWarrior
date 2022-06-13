import random
import sys
import time
from termcolor import colored


class card:
    def __init__(self, name, attack):
        self.name = name
        self.attack = attack


class colors:
    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    CYAN = "\033[1;36m"
    GREEN = "\033[0;32m"


def slowPrint(s, color=colors.CYAN):
    sys.stdout.write(color)
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.02)
    sys.stdout.write("\n")
    time.sleep(0.3)


class player:
    def __init__(self, name, hand, life, deck):
        self.name = name
        self.hand = hand
        self.life = life
        self.deck = deck
        self.activeCard = None
        self.graveyard = []

    def draw(self, num):
        if(len(self.deck) > 0):
            for i in range(0, num):
                out = random.choice(self.deck)
                self.deck.remove(out)
                self.hand.append(out)
        else:
            slowPrint("Deck out!, Graveyard into deck... Draw!", colors.RED)
            self.deck = self.graveyard
            self.graveyard = []
            for i in range(0, num):
                out = random.choice(self.deck)
                self.deck.remove(out)
                self.hand.append(out)

    def getHandLen(self):
        return len(self.hand)

    def showHand(self):
        slowPrint("Life: " + str(self.life) + "  " +
                  "Deck count: " + str(len(self.deck)), colors.GREEN)
        slowPrint("Your hand consists of: ")
        slowPrint("----------------------")
        for i in range(0, len(self.hand)):
            slowPrint("[" + str(i) + "]" + self.hand[i].name +
                      ": ATK = " + str(self.hand[i].attack), colors.GREEN)
        slowPrint("----------------------")

    def playCard(self, handPos):
        self.activeCard = self.hand[handPos]
        self.hand.remove(self.hand[handPos])

    def wipeBoard(self):
        self.graveyard.append(self.activeCard)
        self.activeCard = None


def wipeBoards():
    player1.wipeBoard()
    player2.wipeBoard()


def battleCalc():
    atkDif = player1.activeCard.attack - player2.activeCard.attack
    if((atkDif) < 0):
        slowPrint("Your monster is defeated and take you take {} damage!".format(
            -atkDif), colors.RED)
        player1.life += atkDif
        wipeBoards()
        return
    if((atkDif) > 0):
        slowPrint("You destroy their monster and deal {} damage!".format(
            atkDif), colors.GREEN)
        player2.life -= atkDif
        wipeBoards()
        return
    wipeBoards()
    slowPrint("It's a tie!")


playValid = False

myDeck = [
    card("Steve the Impaler", 1),
    card("John the Meek", 3),
    card("Pat the Brave", 5),
    card("Rob the Bottom", 7),
    card("Alex the Sub", 9)


]
opponentDeck = [
    card("Jennifer the Confusion", 2),
    card("Ryan the Darkness", 4),
    card("Kat the Rave", 6),
    card("Toki the Imposter", 8),
    card("Dennis the Sussy", 10)
]
# Pre-Game
# GAME STARTS--------------
slowPrint("~~~~~~~~~~~~~~~~~~~~~~~~~")
turnCount = 1
player1 = player(input("Enter name: "), [], 15, myDeck)
player2 = player("You", [], 15, opponentDeck)

player1.draw(3)
player2.draw(3)
# Turn looper

while(player1.life > 0 and player2.life > 0):
    slowPrint("~~~")
    slowPrint("Turn {}!".format(turnCount))
    slowPrint("~~~")
    if turnCount > 1:
        player1.draw(1)
        player2.draw(1)
    slowPrint("Enemy Life: "+str(player2.life), colors.RED)
    player1.showHand()
    # selects card
    slowPrint("~~~~~~~~~~~~~~~~~~~~~~~~~")

    while(not playValid):
        cardToPlay = input("Pick a card: ")
        try:
            cardToPlay = int(cardToPlay)
        except:
            pass
        if isinstance(cardToPlay, int) and len(player1.hand) > cardToPlay and cardToPlay >= 0:
            playValid = True
        else:
            slowPrint("Not a valid input")
    playValid = False
    player1.playCard(cardToPlay)
    slowPrint("You Play: " + player1.activeCard.name +
              ": ATK = " + str(player1.activeCard.attack), colors.GREEN)

    # opponent selects card
    player2.playCard(random.randrange(0, player2.getHandLen()))
    slowPrint("Opponent Plays: " + player2.activeCard.name +
              ": ATK = " + str(player2.activeCard.attack), colors.RED)

    # compare attack
    battleCalc()
    turnCount += 1

# Win loss check
if(player1.life > 0):
    slowPrint("Congratulations! {} has defeated the enemy!".format(
        player1.name), colors.GREEN)
else:
    slowPrint("OH NOES! {} has died... GitGud?".format(
        player1.name), colors.RED)
