from backend.character import Character


class Player(Character):

    def roll_initiative(self):
        iteration = len(self.initiative)+1
        if iteration == 1:
            iteration = "1st"
        elif iteration == 2:
            iteration = "2nd"
        else:
            iteration = f"{iteration}th"

        print(f"{self.name}'s {iteration} initiative roll:")
        return int(input())
