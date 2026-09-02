import random
import tkinter as tk
from tkinter import messagebox

class GuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("420x300")
        self.root.resizable(False, False)
        self.new_game()

        tk.Label(root, text="Number Guessing Game", font=("Arial", 20, "bold")).pack(pady=15)
        tk.Label(root, text="Guess a number between 1 and 100").pack()

        self.entry = tk.Entry(root, justify="center", font=("Arial", 14))
        self.entry.pack(pady=12)
        self.entry.bind("<Return>", lambda _: self.check_guess())

        tk.Button(root, text="Guess", width=14, command=self.check_guess).pack()
        self.hint = tk.Label(root, text="You have 7 attempts.", font=("Arial", 11))
        self.hint.pack(pady=15)
        tk.Button(root, text="New Game", command=self.new_game).pack()

    def new_game(self):
        self.secret = random.randint(1, 100)
        self.attempts = 0
        if hasattr(self, "entry"):
            self.entry.delete(0, tk.END)
            self.hint.config(text="You have 7 attempts.")

    def check_guess(self):
        try:
            guess = int(self.entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a whole number.")
            return

        if not 1 <= guess <= 100:
            messagebox.showwarning("Range", "Enter a number from 1 to 100.")
            return

        self.attempts += 1
        if guess == self.secret:
            messagebox.showinfo("Congratulations", f"Correct! You won in {self.attempts} attempts.")
            self.new_game()
        elif self.attempts >= 7:
            messagebox.showinfo("Game Over", f"No attempts left. The number was {self.secret}.")
            self.new_game()
        elif guess < self.secret:
            self.hint.config(text=f"Too low! Attempts left: {7-self.attempts}")
        else:
            self.hint.config(text=f"Too high! Attempts left: {7-self.attempts}")

if __name__ == "__main__":
    root = tk.Tk()
    GuessingGame(root)
    root.mainloop()
