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
        self.nodeEval = 0
        self.firstPlayer = True
        self.selected_index = None
        self.player_starts = None  
        self.tree_root: TreeNode = None  
        self.currentNode: TreeNode = None
        self.isMinMax = True


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

        self.node_eval = tk.Label(root, text="Pēdējā lauka vērtība: ")
        self.node_eval.pack()

        self.number_buttons = []

        self.add_button = tk.Button(root, text="Pievienot punktus", command=lambda: self.add_to_points(True), state=tk.DISABLED)
        self.add_button.pack(side="left")

        self.split_button = tk.Button(root, text="Sadala", command=lambda: self.split_number(True), state=tk.DISABLED)
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

        
        self.tree_root = TreeNode([], 0, 0, None, False)  # Create the game tree root node
        self.currentNode = self.tree_root
        


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
            self.update_game_tree() 
            self.cpu_turn()


    def select_number(self, index):
        if self.selected_index is not None:
            self.number_buttons[self.selected_index].config(relief=tk.RAISED)
        self.selected_index = index
        self.number_buttons[index].config(relief=tk.SUNKEN)
        self.add_button.config(state=tk.NORMAL)
        self.split_button.config(state=tk.NORMAL)

    def add_to_points(self, player: bool):
        if self.selected_index is not None:
            selected_number = self.sequence.pop(self.selected_index)
            self.points += selected_number
            self.number_buttons[self.selected_index].destroy()
            self.number_buttons.pop(self.selected_index)
            self.turn_number += 1
            if player:
                self.advanceNode(False, selected_number)
            self.update_display()
            #self.update_game_tree()

    def split_number(self, player: bool):
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
            if player:
                self.advanceNode(True, selected_number)
            self.update_display()
            #self.update_game_tree() 

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
        '''
        if len(self.sequence) > 1:
            choice = randint(1,len(self.sequence)-1)
        else:
            choice = 0
        self.select_number(choice)
        selected_number = self.sequence[self.selected_index]
        split = False

        if selected_number == 2 or selected_number == 4:
            doSplit = randint(1,2)
            if doSplit == 1:
                self.last_CPU_move_label.config(text=f"Pēdējais CPU gājiens: sadalīt skaitli {selected_number}")
                split = True
                self.split_number(True)
            else:
                self.last_CPU_move_label.config(text=f"Pēdējais CPU gājiens: pievienot punktus {selected_number}")
                split = False
                self.add_to_points(True)
        else:
            self.last_CPU_move_label.config(text=f"Pēdējais CPU gājiens: pievienot punktus {selected_number}")
            split = False
            self.add_to_points(True)
        '''

        bestResult: TreeNode = None
        if self.player_starts:
            # CPU is minimiser
            bestResult = self.CPUMinimiser()
        else:
            # CPU is maximiser
            bestResult = self.CPUMaximiser()

        for index, number in enumerate(self.sequence):
            if number == bestResult.lastNum:
                if bestResult.lastSplit == True:
                    self.select_number(index)
                    selected_number = number
                    self.split_number(True)
                    split = True
                    self.last_CPU_move_label.config(text=f"Pēdējais CPU gājiens: sadalīt skaitli {selected_number}")
                    break
            self.select_number(index)
            selected_number = number
            self.add_to_points(True)
            split= False
            self.last_CPU_move_label.config(text=f"Pēdējais CPU gājiens: pievienot punktus {selected_number}")
            break

        self.advanceNode(split,selected_number)

        #self.update_game_tree() 
    def CPUMaximiser(self):
        bestResult: TreeNode = None
        if len(self.currentNode.field) == 1:
            if self.currentNode.field[0] == 2 or self.currentNode.field[0] == 4:
                return self.currentNode.children[0]
            else:
                return self.currentNode.children[0]
        for child in self.currentNode.children:
            print(child.field)
            if bestResult is None: # empty
                bestResult = child
            if bestResult.eval <= child.eval:
                bestResult = child # atrod node ar augstāko vērtējumu
        print("================")
        return bestResult
        
    def CPUMinimiser(self):
        bestResult: TreeNode = None
        if len(self.currentNode.field) == 1:
            if self.currentNode.field[0] == 2 or self.currentNode.field[0] == 4:
                return self.currentNode.children[0]
            else:
                return self.currentNode.children[0]
        for child in self.currentNode.children:
            print(child.field)
            if bestResult is None: # empty
                bestResult = child
            if bestResult.eval >= child.eval:
                bestResult = child # atrod node ar augstāko vērtējumu
        return bestResult

    def advanceNode(self, split: bool, number):
        for node in self.currentNode.children:
            if split == node.lastSplit:
                if number == node.lastNum:
                    self.currentNode = node
                    self.firstPlayer = not self.firstPlayer
                    self.update_game_tree()
                    self.nodeEval = self.currentNode.eval
                    self.node_eval.config(text=f"Pēdējā lauka vērtība: {self.nodeEval}")
                    break
                else:
                    continue
            else:
                continue

    def select_player_turn(self):
        self.update_game_tree()
        if self.player_starts is None:
            return  # Don't proceed until player chooses who starts
        if (self.player_starts and self.turn_number % 2 == 0) or (not self.player_starts and self.turn_number % 2 == 1):
            self.turn_label.config(text=f"Gājiens: {self.turn_number} (Spēlētājs)")
        else:
            self.turn_label.config(text=f"Gājiens: {self.turn_number} (CPU)")
            self.cpu_turn()

    def update_game_tree(self):
        # Update game tree with new state
        # self.tree_root
        if self.currentNode:
            depth = 3 #+ self.turn_number // 2  # Increase depth every two turns
            self.currentNode = TreeNode(self.sequence, self.bank_points, self.points, None, False)
            TreeNode.generate_game_tree(self.currentNode, depth)
            #TreeNode.print_tree(self.currentNode)  # Print updated game tree
        TreeNode.giveValue(self.currentNode, self.isMinMax, self.firstPlayer)

class TreeNode:
    def __init__(self, field, bank_points, points, lastNum, lastSplit):
        self.field = field
        self.bank_points = bank_points
        self.points = points
        self.lastNum = lastNum
        self.lastSplit = lastSplit
        self.children = []
        self.eval = None  # Placeholder for the evaluation function

    @staticmethod
    def generate_game_tree(root, depth):
        if depth == 0 or not root.field:
            return
        split = False
        for i in range(len(root.field)):
            if root.field[i] == 2:
                
                child_field2 = root.field[:i] + [1, 1] + root.field[i+2:]
                split2 = True
                child_bank_points2 = root.bank_points + 1
                child_points2 = root.points

                child2 = TreeNode(child_field2, child_bank_points2, child_points2, root.field[i], split2)
                root.children.append(child2)
                TreeNode.generate_game_tree(child2, depth - 1)
                # if not split
                child_field = root.field[:i] + root.field[i+1:]
                split = False
                child_points = root.points + root.field[i]
                child_bank_points = root.bank_points
                child = TreeNode(child_field, child_bank_points, child_points, root.field[i], split)
                root.children.append(child)

            elif root.field[i] == 4:
                child_field2 = root.field[:i-1] + [2, 2] + root.field[i+1:]
                split2 = True
                child_points2 = root.points + 2
                child_bank_points2 = root.bank_points

                child2 = TreeNode(child_field2, child_bank_points2, child_points2, root.field[i], split2)
                root.children.append(child2)
                TreeNode.generate_game_tree(child2, depth - 1)
                # if not split
                child_field = root.field[:i] + root.field[i+1:]
                split = False
                child_points = root.points + root.field[i]
                child_bank_points = root.bank_points
                child = TreeNode(child_field, child_bank_points, child_points, root.field[i], split)
                root.children.append(child)
            else:
                child_field = root.field[:i] + root.field[i+1:]
                split = False
                child_points = root.points + root.field[i]
                child_bank_points = root.bank_points
                child = TreeNode(child_field, child_bank_points, child_points, root.field[i], split)
                root.children.append(child)

            #child = TreeNode(child_field, child_bank_points, child_points, root.field[i], split)
            #root.children.append(child)

            TreeNode.generate_game_tree(child, depth - 1)

    @staticmethod
    def giveValue(root, minMax: bool, maximisingPlayer: bool):
        if minMax:
            TreeNode.minMax(root, maximisingPlayer)
        else:
            TreeNode.alphaBeta(root, -9999, 9999, maximisingPlayer)

    @staticmethod
    def alphaBeta(root, alpha, beta, maximisingPlayer):
        if not root.children:
            return TreeNode.evaluate(root)
        if maximisingPlayer:
            maxEval = -99999
            for child in root.children:
                evaluation = TreeNode.alphaBeta(child, alpha, beta, False)
                maxEval = max(maxEval, evaluation)
                alpha = max(alpha, evaluation)
                
                if beta <= alpha:
                    break
            root.eval = maxEval
            return maxEval
        else:
            minEval = 99999
            for child in root.children:
                evaluation = TreeNode.alphaBeta(child, alpha, beta, True)
                minEval = min(minEval, evaluation)
                beta = min(beta, evaluation)
                
                if beta <= alpha:
                    break
            root.eval = minEval
            return minEval
        
    @staticmethod
    def minMax(root, maximisingPlayer):
        if not root.children:
            return TreeNode.evaluate(root)
        if maximisingPlayer:
            maxEval = -99999
            for child in root.children:
                evaluation = TreeNode.minMax(child, False)
                maxEval = max(maxEval, evaluation)
            root.eval = maxEval
            return maxEval
        else:
            minEval = 99999
            for child in root.children:
                evaluation = TreeNode.minMax(child, True)
                minEval = min(minEval, evaluation)
            root.eval = minEval
            return minEval
        
    @staticmethod
    def evaluate(root):
        if root.field:
            if root.lastSplit == True:
                value = len(root.field) + 30
            else:
                value = len(root.field)

        else:
            if root.points % 2 == 1 and root.bank_points % 2 == 1:
                value = 100
            elif root.points % 2 == 1 or root.bank_points % 2 == 1:
                value = 0
            else:
                value = -100
        return value
    #@staticmethod
    '''
    def print_tree(node, depth=0):
        print("  " * depth, f"Field: {node.field}, Bank Points: {node.bank_points}, Points: {node.points}")
        for child in node.children:
          TreeNode.print_tree(child, depth + 1)
    '''

def main():
    root = tk.Tk()
    root.title("Spēle ar skaitļu virkni")

    game = Game(root)

    #root_node = TreeNode([], 0, 0, None, False)  # Assuming the initial state of the game tree is an empty field

    # Generating the game tree
    #TreeNode.generate_game_tree(root_node, 2)  # Generating a game tree with depth 5 for example

    # Printing the game tree
    #TreeNode.print_tree(root_node)

    root.mainloop()

if __name__ == "__main__":
    main()