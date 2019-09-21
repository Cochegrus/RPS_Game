## Class used to define computer behaviour and memory in "Rock, Paper, Scissors" game
## Code written by Jordi A. Cochegrus

import random

class Computer:

    def __init__(self, name = ""):
        self._file = name + ".txt"
        self._games = None
        # memory format = {[hand played by user]: {[previous hand played by user]: {[previous hand played by computer]: [number of times this combination has been observed}
        memory = {"R": {"R": {"R": 0, "P": 0, "S": 0}, "P": {"R": 0, "P": 0, "S": 0}, "S": {"R": 0, "P": 0, "S": 0}}, "P": {"R": {"R": 0, "P": 0, "S": 0}, "P": {"R": 0, "P": 0, "S": 0}, "S": {"R": 0, "P": 0, "S": 0}}, "S": {"R": {"R": 0, "P": 0, "S": 0}, "P": {"R": 0, "P": 0, "S": 0}, "S": {"R": 0, "P": 0, "S": 0}}}

        try:
            headers = True
            data = open(self._file, "r")

            for line in data:
                # removes formatting in memory file
                line.rstrip("\n")
                info = line.split("|")

                if self._games is None:
                    # obtains denominator
                    self._games = int(info[1])

                else:
                    if headers:
                        # prevents headers from being put into dictionary
                        headers = False

                    else:
                        # memory[hand played by user][previous hand played by user][previous hand played by computer] = [number of times this combination has been observed]
                        # collects game data on user
                        memory[info[0]][info[1]][info[2]] = int(info[3])

        except IOError:
            self._games = 0

        finally:
            self._play = ""         # play to be made by computer
            self._prevPlay = ""     # previous hand made by computer
            self._prevHand = ""     # previous hand made by user
            self._name = str(name)
            self._memory = memory

    def updateMemory(self, hand):
        try:
            # records instance
            self._memory[hand][self._prevHand][self._prevPlay] += 1
            self._games += 1

        except KeyError:
            self._games += 1

        self._prevPlay = self._play
        self._prevHand = hand

    def setHand(self):
        prediction = self.predictHand() # suspected play to be made by user

        if prediction == "R":
            self._play = "P"
        elif prediction == "P":
            self._play = "S"
        else:
            self._play = "R"

        return self._play

    def predictHand(self):
        try:
            rockPlayed = (float(self._memory["R"][self._prevHand][self._prevPlay]))     # number of times user has played rock after recorded hands
            paperPlayed = (float(self._memory["P"][self._prevHand][self._prevPlay]))    # number of times user has played paper after recorded hands
            scissorsPlayed = (float(self._memory["S"][self._prevHand][self._prevPlay])) # number of times user has played scissors after recorded hands
            totalPlayed = rockPlayed + paperPlayed + scissorsPlayed                     # number of times user has played after recorded hands
            if totalPlayed == 0.0:
                # prevents error
                totalPlayed = 3.0
            rockChance = 100*(rockPlayed/totalPlayed)
            paperChance = 100*(paperPlayed/totalPlayed)
            scissorsChance = 100*(scissorsPlayed/totalPlayed)

        except KeyError:
            print('First round')
            rockPlayed = 0
            paperPlayed = 0
            scissorsPlayed = 0
            for prevHand in self._memory.keys():
                for prevPlay in self._memory.keys():
                    rockPlayed += float(self._memory["R"][prevHand][prevPlay])
                    paperPlayed += float(self._memory["P"][prevHand][prevPlay])
                    scissorsPlayed += float(self._memory["S"][prevHand][prevPlay])

            try:
                rockChance = (rockPlayed/float(self._games))
                paperChance = 100*(paperPlayed/float(self._games))
                scissorsChance = 100*(scissorsPlayed/float(self._games))
            except ZeroDivisionError:
                rockChance = 33.3
                paperChance = 33.3
                scissorsChance = 33.3

        finally:
            if rockChance != 0:
                if paperChance == 0:
                    if scissorsChance == 0:
                        rockChance = 98.0
                        paperChance = 99.0

                    else:               #paperChance = 0; scissorsChance != 0
                        paperChance = rockChance + 1.0

                else:   # paperChance != 0
                    paperChance += rockChance

            else:   #rockChance = 0
                if paperChance != 0:
                    if scissorsChance != 0:
                        rockChance = 1.0
                        paperChance += rockChance

                    else:           #rockChance = scissorsChance = 0
                        rockChance = 1.0
                        paperChance = 99.0

                else:                       #paperChance = rockChance = 0
                    if scissorsChance != 0:
                        rockChance = 1.0
                        paperChance = 2.0

                    else:                   #paperChance = rockChance = scissorChance = 0
                        rockChance = 33.3
                        paperChance = 2*rockChance

            # range function excludes highest interval
            rockRange = int(rockChance+1)
            paperRange = int(paperChance+1)
            if paperRange >= 101:
                paperRange -= 1
            # scissorsRange = 101

            pick = random.randint(1, 100)   # randomness prevents user from being successful 100% of time if they try to metagame
            if pick in range(rockRange):
                hand = "R"
            elif pick in range(rockRange, paperRange):
                hand = "P"
            else:   # if pick in range(paperRange, 101):
                hand = "S"
            return hand


    def updateData(self):
        data = open(self._file, "w")
        data.write(self._name + "|" + str(self._games) + "\n"
                   "Hand|Previous Hand|Previous Play|Times Played\n")
        for hand in self._memory.keys():
            for prevHand in self._memory.keys():
                for prevPlay in self._memory.keys():
                    data.write(hand + "|" + prevHand + "|" + prevPlay + "|" + str(self._memory[hand][prevHand][prevPlay]) +"\n")
        data.close()
