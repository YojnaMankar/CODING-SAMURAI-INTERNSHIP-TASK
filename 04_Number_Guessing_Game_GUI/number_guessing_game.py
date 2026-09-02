import tkinter as tk
from tkinter import messagebox
import random


class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Number Guessing Game")
        self.root.geometry("450x500")
        self.root.resizable(False, False)

        self.number = random.randint(1, 100)
        self.attempts = 0

        title = tk.Label(
            root,
            text="🎯 Number Guessing Game",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=25)

        instruction = tk.Label(
            root,
            text="Guess a number between 1 and 100",
            font=("Arial", 13)
        )
        instruction.pack(pady=10)

        self.entry = tk.Entry(
            root,
            font=("Arial", 18),
            justify="center",
            width=12
        )
        self.entry.pack(pady=15)

        guess_button = tk.Button(
            root,
            text="🎯 Guess",
            font=("Arial", 14, "bold"),
            width=15,
            command=self.check_guess
        )
        guess_button.pack(pady=10)

        self.result_label = tk.Label(
            root,
            text="Enter your guess!",
            font=("Arial", 14),
            wraplength=350
        )
        self.result_label.pack(pady=20)

        self.attempt_label = tk.Label(
            root,
            text="Attempts: 0",
            font=("Arial", 12)
        )
        self.attempt_label.pack(pady=5)

        reset_button = tk.Button(
            root,
            text="🔄 New Game",
            font=("Arial", 12),
            width=15,
            command=self.reset_game
        )
        reset_button.pack(pady=20)

        self.entry.focus()

    def check_guess(self):
        user_input = self.entry.get().strip()

        if not user_input:
            messagebox.showwarning(
                "Input Required",
                "Please enter a number."
            )
            return

        try:
            guess = int(user_input)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid whole number."
            )
            self.entry.delete(0, tk.END)
            return

        if guess < 1 or guess > 100:
            messagebox.showwarning(
                "Out of Range",
                "Please enter a number between 1 and 100."
            )
            return

        self.attempts += 1
        self.attempt_label.config(
            text=f"Attempts: {self.attempts}"
        )

        if guess < self.number:
            self.result_label.config(
                text="📈 Too low! Try a higher number."
            )

        elif guess > self.number:
            self.result_label.config(
                text="📉 Too high! Try a lower number."
            )

        else:
            self.result_label.config(
                text=f"🎉 Correct! The number was {self.number}."
            )

            messagebox.showinfo(
                "Congratulations! 🎉",
                f"You guessed the number in {self.attempts} attempts!"
            )

            self.entry.config(state="disabled")

        self.entry.delete(0, tk.END)

    def reset_game(self):
        self.number = random.randint(1, 100)
        self.attempts = 0

        self.attempt_label.config(
            text="Attempts: 0"
        )

        self.result_label.config(
            text="Enter your guess!"
        )

        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus()


if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()