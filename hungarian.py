import numpy as np

class HungarianAlgorithm():
    def __init__(self,array) -> None:
        
        self.array_original = array
        self.marked_cells = []
        self.array_current = np.copy(self.array_original)
        self.num_lines = 0
        self.zero_condition()
        self.least_zero_row()
        print(self.marked_cells)
        print(self.bool_mat)
    
    def row_reduction(self):
        for row in range(self.array_current.shape[0]):
            self.array_current[row] = np.subtract(self.array_current[row], np.amin(self.array_current[row]))
        self.zero_condition(called_from='row_reduction')

    def column_reduction(self):
        for column in range(self.array_current.shape[1]):
            self.array_current[:, column] = np.subtract(self.array_current[:, column], np.amin(self.array_current[:, column]))
        self.zero_condition(called_from='column_reduction')

    # this method will make sure that theres a zero in each column and in each row
    def zero_condition(self, called_from=None):
        if called_from == 'column_reduction':
            return self.boolean_matrix()
        
        for row in range(self.array_current.shape[0]):
            if 0 not in self.array_current[row]:
                return self.row_reduction()
        if called_from == 'row_reduction':
            for column in range(self.array_current.shape[1]):
                if 0 not in self.array_current[:, column]:
                    return self.column_reduction()
        return self.boolean_matrix()
        
    # creates a boolean matrix of current array with 0's as True
    def boolean_matrix(self):
        self.bool_mat = (self.array_current == 0)

    def least_zero_row(self):
        # find the row with the least trues
        # if the bool matrix is fully false go to a different step
        if np.array_equal(self.bool_mat , np.full(self.bool_mat.shape, False)):
            self.bool_mat = np.full(self.bool_mat.shape, False)
            for i in self.marked_cells:
                self.bool_mat[i[0],i[1]] = True
            return
        min_val = self.bool_mat.shape[0]
        min_idx = None
        for i, row in enumerate(self.bool_mat):
            
            if sum(row) == 0:
                continue
            elif sum(row) < min_val:
                min_val = sum(row)
                min_idx = i
                if sum(row) == 1:
                    return self.mark_elements(min_idx)
        return self.mark_elements(min_idx)
    
    def mark_elements(self, min_idx):
        if min_idx is None:
            self.bool_mat = np.full(self.bool_mat.shape, False)
            for i in self.marked_cells:
                self.bool_mat[i[0],i[1]] = True
            return
        for column, value in enumerate(self.bool_mat[min_idx]):
            if value == True:
                self.marked_cells.append([min_idx, column])
                self.clean_up()

    def clean_up(self):
        for i in self.marked_cells:
            row = i[0]
            column = i[1]
            self.bool_mat[row] = False
            self.bool_mat[:,column] = False
        self.least_zero_row()

    

if __name__ == "__main__":
    # array = np.random.randint(0,10,(3,3))
    array= np.array([[8,25,50],[50,35,75],[22,48,150]])
    
    HungarianAlgorithm(array)

