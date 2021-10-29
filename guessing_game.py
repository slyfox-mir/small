import random

from collections import namedtuple
from enum import Enum


DifficultData = namedtuple('DifficultData', [
    'start_position',
    'end_possition',
    'turns',
    'score_rate'
])


class DifficultLevel(Enum):
    HARD = DifficultData(
        start_position=1,
        end_possition=100,
        turns=10,
        score_rate=((0, 100, ''),
                    (5, 35, 'SOOOO CLOSE! '),
                    (10, 30, 'CLOSE! '),
                    (20, 20, 'Almost, '),
                    (30, 10, 'Not quite, '))
    )
    NORMAL = DifficultData(
        start_position=1,
        end_possition=10,
        turns=10,
        score_rate=((0, 10, ''),
                    (1, 3, 'CLOSE! '),
                    (2, 2, 'Almost, '),
                    (3, 1, 'Not quite, '))
    )


class GameStatus(Enum):
    CONTINUE = 0
    GAMEOVER = 1
    WIN = 2


class GameState:

    def __init__(self, difficult_lvl):
        self.score = 0
        self.user_guesses = []
        self.game_status = GameStatus.CONTINUE
        self.difficult_lvl = difficult_lvl
        self.turns = difficult_lvl.value.turns
        self.secret_number = random.randint(difficult_lvl.value.start_position,
                                            difficult_lvl.value.end_possition)

    def __str__(self):
        return (f"<GameState> score: {self.score},  "
                f"game_state: {self.game_status.name}, difficult: {self.difficult_lvl.name}, "
                f"secret number: {self.secret_number}, guesses: {self.user_guesses}")

    def apply_movement(self, turns: int, guess: int):

        if not turns or not guess:
            self.game_status = GameStatus.GAMEOVER
            return

        self.turns -= turns
        self.user_guesses.append(guess)

        if guess == self.secret_number:
            self.game_status = GameStatus.WIN
        elif self.turns <= 0:
            self.game_status = GameStatus.GAMEOVER

        guess_rate = abs(self.secret_number - guess)
        for rate, points, description in self.difficult_lvl.value.score_rate:
            if guess_rate <= rate:
                self.score += points
                print(f"{description} \nYou gained {points} points")
                break
        else:
            print("Ouch! That guess was too far away. \nYou gained 0 points")


def print_greetings():
    print("""
______________________________________________________________________________________________
                                    WELCOME TO
                                   _   _  _     __            _ 
                    |\ | | | |\/| |_) |_ |_)   /__  /\  |\/| |_ 
                    | \| |_| |  | |_) |_ | \   \_| /--\ |  | |_ 

                                  BY BASSON KOCH
______________________________________________________________________________________________                                            
        The computer will pick a number from (1 - 10 / Normal) or (1 - 100 / Hard). 
        The player will gain points for how close the guess is to the correct number.
                        Closer means more points, further less points. 

        After you guess the number, your remaining turns will act as bonus points. 

                        Solve the number faster for a higher score.

                If you have the highest score. You will become the CHAMPION!  
                                    GOODLUCK player    
______________________________________________________________________________________________        
        """)


def select_difficulty() -> DifficultLevel:

    error_msg = ("_____________________________________________\n" +
                 "ERROR:  Please type in \"normal\" or \"hard\"\n" +
                 "_____________________________________________")

    while True:
        user_input = input("Select a difficulty!  Normal/Hard  :    ")
        user_input = user_input.strip().lower()

        if user_input == "normal":
            return DifficultLevel.NORMAL
        elif user_input == "hard":
            return DifficultLevel.HARD
        else:
            print(error_msg)


def get_user_move(game_state: GameState) -> tuple:

    turn_count = 0
    print("_____________________________________________\n" 
          f"Turns Left: {game_state.turns - turn_count}\n"
          f"Total Score: {game_state.score}\n"
          "_____________________________________________")

    if game_state.user_guesses:
        print("\nYou've already guessed the numbers: {}\n".format(
            ' '.join(map(str, sorted(game_state.user_guesses)))
        ))

    while turn_count < game_state.turns:

        range_str = '{} - {}'.format(
            game_state.difficult_lvl.value.start_position,
            game_state.difficult_lvl.value.end_possition,
        )

        user_msg = f"\nGuess any number from {range_str}\n:     "
        error_msg = ("_____________________________________________\n"
                     f"ERROR: Please pick a number from {range_str}\n"
                     "_____________________________________________\n")

        user_guess = input(user_msg)

        if not user_guess or user_guess.isalpha():
            print(error_msg)
            continue

        try:
            user_guess = int(user_guess)
        except:
            continue

        if (user_guess < game_state.difficult_lvl.value.start_position or
                user_guess > game_state.difficult_lvl.value.end_possition):
            print(error_msg)

        elif user_guess in game_state.user_guesses:
            print("_____________________________________________")
            print("ERROR: You can't guess the same number twice\n \n-1 TURN AS PENALTY")
            print("_____________________________________________")

            turn_count += 1
        else:
            print("\n" * 9)
            print("_____________________________________________\n")
            print(f"YOUR GUESS: {user_guess}\n")

            turn_count += 1

            return turn_count, user_guess

    return None, None


def check_game_over(game_state: GameState) -> bool:

    if game_state.game_status == GameStatus.CONTINUE:
        return False
    if game_state.game_status == GameStatus.WIN:
        print("""\n
                      _              ___      
                 \_/ / \ | |   \    / |  |\ | 
                  |  \_/ |_|    \/\/ _|_ | \| 

                            """)

        print(f"\nYour score is: {game_state.score}")

    else:
        print("""\n
                  __            _    _        _  _  
                 /__  /\  |\/| |_   / \ \  / |_ |_) 
                 \_| /--\ |  | |_   \_/  \/  |_ | \ 

                        """)

        print(f"The correct number was:   {game_state.secret_number}")
        print(f"\nYour score is: {game_state.score}")

    return True


def play_again():

    again = input("Play again?      Type (Y/N) \n:         ")
    again = again.upper()
    while True:
        if again.lower() == "y":
            return True
        elif again.lower() == "n":
            return False
        else:
            print("_____________________________________________")
            print("ERROR:  Please type \"Y\" or \"N\"")
            print("_____________________________________________")


def main():

    print_greetings()

    is_playing = True
    while is_playing:
        difficulty = select_difficulty()
        game_state = GameState(difficulty)

        while game_state.game_status == GameStatus.CONTINUE:
            print(game_state)
            turns, user_guess = get_user_move(game_state)

            game_state.apply_movement(turns, user_guess)
            check_game_over(game_state)

        is_playing = play_again()


if __name__ == '__main__':
    main()
