import numpy as np

class HungarianAlgorithm():
    def __init__(self,array) -> None:
        
        self.array_original = array
        self.marked_posiitons = np.full((array.shape), False)
        self.array_current = np.copy(self.array_original)
        self.num_lines = 0
        self.zero_condition()
        print(self.array_original)
        print(self.array_current)
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
    

if __name__ == "__main__":
    # array = np.random.randint(0,10,(3,3))
    array= np.array([[8,25,50],[50,35,75],[22,48,150]])
    
    HungarianAlgorithm(array)

