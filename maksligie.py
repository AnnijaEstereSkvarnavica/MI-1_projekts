import tkinter as tk
from tkinter import messagebox
from random import randint
import copy

class Game:
    def __init__(self, root):
        self.root = root
        self.length = None
        self.sequence = []
        self.points = 0
        self.bank_points = 0
        self.turn_number = 0
        self.selected_index = None
        self.player_starts = None  
        self.tree_root = None  

        self.label = tk.Label(root, text="Skaitļu virkne: ")
        self.label.pack()

        self.points_label = tk.Label(root, text="Tavi punkti: 0")
        self.points_label.pack()

        self.bank_points_label = tk.Label(root, text="Bankas punkti: 0")
        self.bank_points_label.pack()

        self.turn_label = tk.Label(root, text="Gājiens: 0")
        self.turn_label.pack()

        self.last_CPU_move_label = tk.Label(root, text="Pēdējais CPU gājiens:")
        self.last_CPU_move_label.pack()

        self.number_buttons = []

        self.add_button = tk.Button(root, text="Pievienot punktus", command=self.add_to_points, state=tk.DISABLED)
        self.add_button.pack(side="left")

        self.split_button = tk.Button(root, text="Sadala", command=self.split_number, state=tk.DISABLED)
        self.split_button.pack(side="right")

        self.start_button_player = tk.Button(root, text="Spēlētājs sāk", command=lambda: self.set_player_starts(True))
        self.start_button_player.pack()

        self.start_button_cpu = tk.Button(root, text="CPU sāk", command=lambda: self.set_player_starts(False))
        self.start_button_cpu.pack()

        self.length_label = tk.Label(root, text="Ievadiet cik skaitļu vēlaties generēt (no 15 līdz 20):")
        self.length_label.pack()

        self.length_entry = tk.Entry(root)
        self.length_entry.pack()

        self.set_length_button = tk.Button(root, text="Iestatīt garumu", command=self.set_length)
        self.set_length_button.pack()

        self.tree_root = TreeNode([], 0, 0)  # Create the game tree root node


    def set_length(self):
        try:
            length = int(self.length_entry.get())
            if 15 <= length <= 20:
                self.length = length
                self.sequence = [randint(1, 4) for _ in range(length)]
                self.update_display()
            else:
                messagebox.showerror("Kļūda", "Skaitļu skaits ir jābūt no 15 līdz 20.")
        except ValueError:
            messagebox.showerror("Kļūda", "Lūdzu, ievadiet skaitli.")

    def set_player_starts(self, player_starts):
        self.player_starts = player_starts
        self.start_button_player.config(state=tk.DISABLED)
        self.start_button_cpu.config(state=tk.DISABLED)
        self.length_entry.config(state=tk.DISABLED)  # Disable the length entry
        self.set_length_button.config(state=tk.DISABLED)  # Disable the set length button
        if player_starts:
            for button in self.number_buttons:
                button.config(state=tk.NORMAL)
            self.add_button.config(state=tk.NORMAL)
            self.split_button.config(state=tk.NORMAL)
        else:
            self.cpu_turn()


    def select_number(self, index):
        if self.selected_index is not None:
            self.number_buttons[self.selected_index].config(relief=tk.RAISED)
        self.selected_index = index
        self.number_buttons[index].config(relief=tk.SUNKEN)
        self.add_button.config(state=tk.NORMAL)
        self.split_button.config(state=tk.NORMAL)

    def add_to_points(self):
        if self.selected_index is not None:
            selected_number = self.sequence.pop(self.selected_index)
            self.points += selected_number
            self.number_buttons[self.selected_index].destroy()
            self.number_buttons.pop(self.selected_index)
            self.turn_number += 1
            self.update_display()
            self.update_game_tree()

    def split_number(self):
        if self.selected_index is not None:
            selected_number = self.sequence[self.selected_index]
            if selected_number == 2:
                self.bank_points += 1
                self.sequence[self.selected_index] = 1
                self.sequence.insert(self.selected_index + 1, 1)
                self.turn_number += 1
            elif selected_number == 4:
                self.points += 2
                self.sequence[self.selected_index] = 2
                self.sequence.insert(self.selected_index + 1, 2)
                self.turn_number += 1
            self.update_display()
            self.update_game_tree() 

    def check_winner(self):
        if not self.sequence:
            if self.points % 2 == 0 and self.bank_points % 2 == 0:
                winner = "Pirmais spēlētājs"
            elif self.points % 2 == 1 and self.bank_points % 2 == 1:
                winner = "Otrais spēlētājs"
            else:
                winner = "Neizšķirts"
            self.label.config(text=f"Spēle beigusies! Uzvar: {winner}")

    def update_display(self):
        self.label.config(text=f"Skaitļu virkne: {self.sequence}")
        self.points_label.config(text=f"Tavi punkti: {self.points}")
        self.bank_points_label.config(text=f"Bankas punkti: {self.bank_points}")
        self.turn_label.config(text=f"Gājiens: {self.turn_number}")
        self.selected_index = None

        for button in self.number_buttons:
            button.destroy()
        self.number_buttons = []
        for index, number in enumerate(self.sequence):
            button = tk.Button(self.root, text=str(number), command=lambda i=index: self.select_number(i))
            button.pack(side="left")
            self.number_buttons.append(button)
        
        self.check_winner()
        if self.sequence:
            self.select_player_turn()

    def cpu_turn(self):
        if len(self.sequence) > 1:
            choice = randint(1,len(self.sequence)-1)
        else:
            choice = 0
        self.select_number(choice)
        selected_number = self.sequence[self.selected_index]
        
        if selected_number == 2 or selected_number == 4:
            doSplit = randint(1,2)
            if doSplit == 1:
                self.last_CPU_move_label.config(text=f"Pēdējais CPU gājiens: sadalīt skaitli {selected_number}")
                self.split_number()
            else:
                self.last_CPU_move_label.config(text=f"Pēdējais CPU gājiens: pievienot punktus {selected_number}")
                self.add_to_points()
        else:
            self.last_CPU_move_label.config(text=f"Pēdējais CPU gājiens: pievienot punktus {selected_number}")
            self.add_to_points()
        self.update_game_tree() 

    def select_player_turn(self):
        if self.player_starts is None:
            return  # Don't proceed until player chooses who starts
        if (self.player_starts and self.turn_number % 2 == 0) or (not self.player_starts and self.turn_number % 2 == 1):
            self.turn_label.config(text=f"Gājiens: {self.turn_number} (Spēlētājs)")
        else:
            self.turn_label.config(text=f"Gājiens: {self.turn_number} (CPU)")
            self.cpu_turn()

    def update_game_tree(self):
        # Update game tree with new state
        if self.tree_root:
            depth = 3 + self.turn_number // 2  # Increase depth every two turns
            self.tree_root = TreeNode(self.sequence, self.bank_points, self.points)
            TreeNode.generate_game_tree(self.tree_root, depth)
            #TreeNode.print_tree(self.tree_root)  # Print updated game tree

class TreeNode:
    def __init__(self, field, bank_points, points):
        self.field = field
        self.bank_points = bank_points
        self.points = points
        self.children = []
        self.eval = None  # Placeholder for the evaluation function

    @staticmethod
    def generate_game_tree(root, depth):
        if depth == 0 or not root.field:
            return

        for i in range(len(root.field)):
            if root.field[i] == 2:
                child_field = root.field[:i] + [1, 1] + root.field[i+1:]
                child_bank_points = root.bank_points + 1
            elif root.field[i] == 4:
                child_field = root.field[:i] + [2, 2] + root.field[i+1:]
                child_points = root.points + 2
            else:
                child_field = root.field[:i] + root.field[i+1:]
                child_points = root.points + root.field[i]

            child = TreeNode(child_field, root.bank_points, root.points)
            root.children.append(child)

            TreeNode.generate_game_tree(child, depth - 1)

    @staticmethod
    """def print_tree(node, depth=0):
        print("  " * depth, f"Field: {node.field}, Bank Points: {node.bank_points}, Points: {node.points}")
        for child in node.children:
          TreeNode.print_tree(child, depth + 1)"""


def main():
    root = tk.Tk()
    root.title("Spēle ar skaitļu virkni")

    game = Game(root)

    root_node = TreeNode([], 0, 0)  # Assuming the initial state of the game tree is an empty field

    # Generating the game tree
    TreeNode.generate_game_tree(root_node, 2)  # Generating a game tree with depth 5 for example

    # Printing the game tree
    TreeNode.print_tree(root_node)

    root.mainloop()

if __name__ == "__main__":
    main()