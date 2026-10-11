from collections import Counter
from enum import Enum
from pathlib import Path
import random


words_list_file = Path.home() / "projects/wordle-stuff/guesses.txt"
answer_list_file = Path.home() / "projects/wordle-stuff/answers.txt"
words_list = []
answers_list = []

with open(words_list_file, "r") as file1:
    words_list = [word.strip().upper() for word in file1 if len(word.strip()) == 5]

with open(answer_list_file, "r") as file2:
    answers_list = [word.strip().upper() for word in file2 if len(word.strip()) == 5]


MAX_TRIES = 6
WORD_LENGTH = 5


class Status(Enum):
    WRONG = 1
    IN_WORD = 2
    CORRECT = 3


COLORS = {
    Status.WRONG: "\033[90m",  # Gray
    Status.IN_WORD: "\033[33m",  # Yellow
    Status.CORRECT: "\033[32m",  # Green
}

RESET = "\033[0m"


class Wordle:
    def __init__(self, target_word=None):
        if target_word:
            self.target_word = target_word.upper()
        else:
            self.target_word = random.choice(answers_list)

        self.tries = 0
        self.win_condition = False

    def display_guess(self, guess_status, guess):
        for index, status in enumerate(guess_status):
            color = COLORS[status]
            letter = guess[index].upper()
            print(f"{color}[{letter}]{RESET}", end=" ")

        print("\n")

    def guess(self, guess):
        guess = guess.upper()
        self.tries += 1

        guess_status = [Status.WRONG] * WORD_LENGTH
        remaining_letters = Counter(self.target_word)

        # Pass 1: check letters if they exist in the word, and are in the correct position
        for index in range(WORD_LENGTH):
            letter = guess[index]

            if letter == self.target_word[index]:
                guess_status[index] = Status.CORRECT
                remaining_letters[letter] -= 1

        # Pass 2: check the indexes that have been skipped over to mark as IN_WORD or WRONG
        for index in range(WORD_LENGTH):
            if guess_status[index] == Status.CORRECT:
                continue

            letter = guess[index]

            if remaining_letters[letter] > 0:
                guess_status[index] = Status.IN_WORD
                remaining_letters[letter] -= 1

        self.display_guess(guess_status, guess)

        if guess == self.target_word:
            self.win_condition = True
            print("YOOOO YOU GOT THE WORD!!!!")
        elif self.tries == MAX_TRIES:
            print(f"u lost bro, the word was {self.target_word}")

    def start(self):
        print(
            "GREEN - Correct position and letter! \nGREY - Wrong letter! \nYELLOW - Correct letter!"
        )

        while not self.win_condition and self.tries < MAX_TRIES:
            user_guess = input("what's ur guess? ").strip().upper()

            if len(user_guess) != WORD_LENGTH or not user_guess.isalpha():
                print("enter a five-letter word")
                continue

            if not user_guess in words_list:
                print("enter a valid word")
                continue

            self.guess(user_guess)


game = Wordle()
game.start()
