## Program to simulate a game of "Rock, Paper, Scissors" between computer and user
## Code written by Jordi A. Cochegrus

from computer import *

# instructions for user
print('Let\'s play "Rock, Paper, Scissors"!'
      '\nEnter "rock", "paper" or "scissors" to pick your hand.'
      '\nYou are playing for best out of three!')
# prompts user's name to load game data
name = input('Enter name to load data:\n')

start = ""
# start of game
while start == "":
    cpu = Computer(name)
    playerWins = 0  # records number of games won by user
    cpuWins = 0  # records number of games won by computer

    # game continues
    while not playerWins == 2 and not cpuWins == 2:
        tie = 1  # lets program repeat the round until either user or computer wins

        # start of round
        while tie == 1 and start == "":
            cpuHand = cpu.setHand()                             # computer predicts hand user will play
            userHand = input("\nROCK!\nPAPER!\nSCISSORS!\n")
            userHand = userHand.upper()
            if cpuHand == "R":
                print("rock")
            elif cpuHand == "P":
                print("paper")
            else:   # cpuHand == "S"
                print("scissors")

            valid = True    # used to prevent invalid hands being saved into memory

            # changes input to match computer output
            if userHand == "ROCK":
                userHand = "R"
            elif userHand == "PAPER":
                userHand = "P"
            elif userHand == "SCISSORS":
                userHand = "S"
            # if invalid input
            else:
                valid = False
                print("That's a weird hand...\nYou can only use rock, paper or scissors!")
                start = input('Press "Enter" if you want to keep playing. If you want to quit, enter any other key.')
                if not start == "":  # ends game
                    print("\nThanks for playing my game!")
                    exit(0)

            if userHand == cpuHand:
                print("TIE\n")
            else:
                tie = 0
                if userHand == "R":
                    if cpuHand == "S":  #scissors
                        print("YOU WIN!")
                        playerWins += 1
                    else: #paper
                        print("YOU LOSE!")
                        cpuWins += 1

                elif userHand == "P":
                    if cpuHand == "R":  #rock
                        print("YOU WIN!")
                        playerWins += 1
                    else: #scissors
                        print("YOU LOSE!")
                        cpuWins += 1

                elif userHand == "S":
                    if cpuHand == "P":  #paper
                        print("YOU WIN!")
                        playerWins += 1
                    else:   #rock
                        print("YOU LOSE!")
                        cpuWins += 1

            # end of round if not a tie
            if valid:
                cpu.updateMemory(userHand)

    # game pauses after either computer or user wins 2 out of 3 rounds
    cpu.updateData()

    if cpuWins == 2:
        print("\nGood game. Better luck next time!")
        start = input('Press "Enter" if you want play again. If you want to quit, enter any other key. ')

    else:  # playerWins == 2:
        print("\nGood game. I'll get you next time!")
        start = input('Press "Enter" if you want to play again. If you want to quit, enter any other key. ')

# end of game
print("\nThanks for playing my game!")
