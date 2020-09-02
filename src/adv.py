from room import Room
from player import Player
# Declare all the rooms


room = {
    'outside':  Room("Outside of the Tower of Sauron",
                     "North of you, the tower entrance beckons. A hastily scrawled map has been scratched into the side of the entrance: N>E>N."),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Broken furniture has been pushed to the walls 
and what looks like the remnants of a fire lay in the center of the room. Dusty passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling into the darkness. 
Ahead to the north, a light in the shape of an eye flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Stone Passage", """The narrow passage bends here from west to north.
Spider webs hang from the ceiling and the smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure chamber!
Sadly, it has already been completely emptied by earlier adventurers. A glint catches your eye
and a single golden ring remains partially buried in dust. The only exit is to the south."""),
}

room['overlook'].addItem('Sword')
room['outside'].addItem('Cape')
room['treasure'].addItem('Ring')
room['foyer'].addItem('Torch')

# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

player = Player("Frodo", room["outside"])

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

class Game(): 
   
    def __init__(self):
       self.commandMap = {
           'n': self.move,
           'w': self.move,
           's': self.move,
           'e': self.move,
           'drop': self.dropItem,
           'pickup': self.pickupItem,
           'q': self.quit
       }
    
    def printState(self, player):

        print(player.room.name)
        print(player.room.description)
        print('Items in Room: ', player.room.items)
        print('Personal Inventory: ', player.inventory)

        return input('Input a Movement Direction (n,w,s,e) or press "q" to Exit the Game: ')


    def move(self, player, userInput):

        print(player, userInput[0])
        
        if(not hasattr(player.room, f'{userInput[0]}_to')):
            return input('You cannot move in that direction: Please choose another or press "q" to Exit the Game: ')
        else:

            player.room = getattr(player.room, f'{userInput[0]}_to')

            return self.printState(player)

            
    def dropItem(self, player, commands):

        player.removeItem(commands[1])
        player.room.addItem(commands[1])
        
        return self.printState(player)

        

    def pickupItem(self, player, commands): 

        player.addItem(commands[1])
        player.room.removeItem(commands[1])

        return self.printState(player)

        
    
    def quit(self, *args): 
        return 'q'


    def issueCommand(self, userInput, player):
        
        commands = userInput.split(" ")

        if(commands[0] in self.commandMap.keys()):

            nextCommand = self.commandMap[commands[0]](player, commands)
    
            if nextCommand == 'q': return

            else: self.issueCommand(nextCommand, player)

        else:
            
            userInput = input('Please enter a valid input or press "q" to Exit the Game: ')
            self.issueCommand(userInput, player)


gameInstance = Game()

print(player.room.name)
print(player.room.description)
print('Items in Room: ', player.room.items)
print('Personal Inventory: ', player.inventory)

userInput = input('Input a Movement Direction (n,w,s,e) or press "q" to Exit the Game: ')

gameInstance.issueCommand(userInput, player)

print("Your Quest is Over")  