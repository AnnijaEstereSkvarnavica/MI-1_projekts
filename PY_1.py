import tkinter as tk
from random import randint

class Game:
    def __init__(self, root, length):
        self.root = root
        self.length = length
        self.sequence = [randint(1, 4) for _ in range(length)]  # Ģenerē skaitļu virkni
        self.points = 0
        self.bank_points = 0
        self.selected_index = None

        self.label = tk.Label(root, text=f"Skaitļu virkne: {self.sequence}")
        self.label.pack()

        self.points_label = tk.Label(root, text=f"Tavi punkti: {self.points}")
        self.points_label.pack()

        self.bank_points_label = tk.Label(root, text=f"Bankas punkti: {self.bank_points}")
        self.bank_points_label.pack()

        self.number_buttons = []
        for index, number in enumerate(self.sequence):
            button = tk.Button(root, text=str(number), command=lambda i=index: self.select_number(i))
            button.pack(side="left")
            self.number_buttons.append(button)

        self.add_button = tk.Button(root, text="Pievienot punktus", command=self.add_to_points)
        self.add_button.pack(side="left")

        self.split_button = tk.Button(root, text="Sadala", command=self.split_number)
        self.split_button.pack(side="right")

    def select_number(self, index):
        if self.selected_index is not None:
            self.number_buttons[self.selected_index].config(relief=tk.RAISED)
        self.selected_index = index
        self.number_buttons[index].config(relief=tk.SUNKEN)

    def add_to_points(self):
        if self.selected_index is not None:
            selected_number = self.sequence.pop(self.selected_index)
            self.points += selected_number
            self.number_buttons[self.selected_index].destroy()
            self.number_buttons.pop(self.selected_index)
            self.update_display()

    def split_number(self):
        if self.bank_points > 0 and self.selected_index is not None:
            selected_number = self.sequence[self.selected_index]
            if selected_number == 2:
                self.bank_points -= 1
                self.sequence[self.selected_index] = 1
                self.sequence.insert(self.selected_index + 1, 1)
            elif selected_number == 4:
                self.points += 2
                self.bank_points -= 1
                self.sequence[self.selected_index] = 2
                self.sequence.insert(self.selected_index + 1, 2)
            self.update_display()

    def check_winner(self):
        if not self.sequence:
            total_points = self.points + self.bank_points
            if total_points % 2 == 0:
                winner = "Pirmais spēlētājs"
            else:
                winner = "Otrais spēlētājs"
            self.label.config(text=f"Spēle beigusies! Uzvar: {winner}")

    def update_display(self):
        self.label.config(text=f"Skaitļu virkne: {self.sequence}")
        self.points_label.config(text=f"Tavi punkti: {self.points}")
        self.bank_points_label.config(text=f"Bankas punkti: {self.bank_points}")
        self.selected_index = None

        for button in self.number_buttons:
            button.destroy()
        self.number_buttons = []
        for index, number in enumerate(self.sequence):
            button = tk.Button(self.root, text=str(number), command=lambda i=index: self.select_number(i))
            button.pack(side="left")
            self.number_buttons.append(button)

        self.check_winner()

def main():
    length = randint(15, 20)  # Ģenerē skaitļu virknes garumu
    root = tk.Tk()
    root.title("Spēle ar skaitļu virkni")

    game = Game(root, length)

    root.mainloop()

if __name__ == "__main__":
    main()
