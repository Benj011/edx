import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        mines = set()

        if self.count == len(self.cells):
            return self.cells
        else:
            return mines


        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safes = set()

        if self.count == 0:
            return self.cells
        else:
            return safes

        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        if cell in self.cells and self.count > 0:
            self.cells.remove(cell)
            self.count -= 1
        
        return
        

        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        if cell in self.cells:
            self.cells.remove(cell)

        return

        raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

        return

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

        return

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        print("Start of add knowlege")
        print(cell)
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # going through the knowledge base and changing the sentences that hold the cell

        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.mark_safe(cell)


        if count == 0:

            i = cell[0]
            j = cell[1]

            # checking the cells around the cell that was clicked on

            # checking i - 1
            if i - 1 >= 0 and j - 1 >= 0:
                self.mark_safe((i - 1, j - 1))
            if i - 1 >= 0:
                self.mark_safe((i - 1, j))
            if i - 1 >= 0 and j + 1 < self.width:
                self.mark_safe((i - 1, j + 1))

            # checking i
            if j - 1 >= 0:
                self.mark_safe((i, j - 1))
            if j + 1 < self.width:
                self.mark_safe((i, j + 1))

            # checking i + 1
            if i + 1 < self.height and j - 1 >= 0:
                self.mark_safe((i + 1, j - 1))
            if i + 1 < self.height:
                self.mark_safe((i + 1, j))
            if i + 1 < self.height and j + 1 < self.width:
                self.mark_safe((i + 1, j + 1))
                
                


        Sentence_cells = set()

        print("Start of Sentence_cells")
        # iterating through every cell and deeing if they have already 
        # been marked or moved to

        for i in range(self.height - 1):
            for j in range(self.width - 1):
                if (i,j) in self.mines:
                    count -= 1
                elif (i,j) in self.safes:
                    continue
                elif (i,j) in self.moves_made:
                    continue
                else:
                    Sentence_cells.add((i,j))


        # making a new sentence with new info

        print("Start of new sentence")

        new_sentence = Sentence(Sentence_cells, count) 
        self.knowledge.append(new_sentence)


        # going through the knowledge base and checking each sentence for sure mines and safes
        print("Start of checking for mines and safes")
        safes_to_mark = set()
        mines_to_mark = set()

        for sentence in self.knowledge:
            if sentence.count == 0:
                for cell in sentence.cells:
                    safes_to_mark.add(cell)
            elif sentence.count == len(sentence.cells):
                for cell in sentence.cells:
                    mines_to_mark.add(cell)

        # now adding to self.knowledge becuase im not iterating over it    
        print("Start of marking safes and mines")
        for cell in safes_to_mark:
            self.mark_safe(cell)
        for cell in mines_to_mark:
            self.mark_mine(cell)

        # subset method now
        print("Start of subset method")

        sentencesToAdd = []

        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 == sentence2:
                    continue
                if sentence1.cells.issubset(sentence2.cells):
                    new_sentence = Sentence(sentence2.cells - sentence1.cells, sentence2.count - sentence1.count)
                    if new_sentence in sentencesToAdd:
                        continue
                    else:
                        sentencesToAdd.append(new_sentence)
                    
        for sentence in sentencesToAdd:
            self.knowledge.append(sentence)        
        
        print("End of add knowlege")
        return

        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        for move in self.safes:
            if move not in self.moves_made:
                return move

        return None
    
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        random_moves = []

        # making a random move from neighbors of cells that have been clicked on

        if len(self.moves_made) != 0:
            for cell in self.moves_made:
                i = cell[0]
                j = cell[1]
                for x in range(i - 1, i + 2):
                    for y in range(j - 1, j + 2):
                        if x >= 0 and y >= 0 and x < self.height and y < self.width:
                            if (x,y) not in self.moves_made and (x,y) not in self.mines:
                                random_moves.append((x,y))

        else:
            return (random.randint(0, self.height - 1), random.randint(0, self.width - 1))
        
        while True:
            random_int = random.randint(0, len(random_moves) - 1)
            if random_moves[random_int] not in self.moves_made and random_moves[random_int] not in self.mines:
                break
            else:
                random_moves.remove(random_moves[random_int])

        return random_moves[random_int]

        raise NotImplementedError


# current problems is that i am adding cells wrong somehow