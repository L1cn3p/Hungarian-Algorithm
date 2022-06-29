import numpy as np


def min_zero_row(zero_mat, mark_zero):
    '''
    The function can be splitted into two steps:
    #1 The function is used to find the row which containing the fewest 0.
    #2 Select the zero number on the row, and then marked the element corresponding row and column as False
    '''

    # Find the row
    min_row = [99999, -1]

    for row_num in range(zero_mat.shape[0]):
        if np.sum(zero_mat[row_num] == True) > 0 and min_row[0] > np.sum(zero_mat[row_num] == True):
            min_row = [np.sum(zero_mat[row_num] == True), row_num]

    # Marked the specific row and column as False
    zero_index = np.where(zero_mat[min_row[1]] == True)[0][0]
    mark_zero.append((min_row[1], zero_index))
    zero_mat[min_row[1], :] = False
    zero_mat[:, zero_index] = False

'''
input: 
the mat obtained after every column and every row subtract its internal minimum

output: 
1、the position of the marked 0 elements 
2、marked rows
3、marked columns

for example:
input:
mat = array([[5,4,0,5,0],[0,1,4,0,8],[2,0,6,1,2],[7,0,3,4,5],[1,4,2,3,0]])
output:
1、marked_zero = [(2,1),(4,4),(0,2),(1,0)]
2、marked_rows = [0,1,4]
3、marked_cols = [1]

'''
def mark_matrix(mat):
    # Transform the matrix to boolean matrix(0 = True, others = False)
    cur_mat = mat
    zero_bool_mat = (cur_mat == 0)
    zero_bool_mat_copy = zero_bool_mat.copy()

    # Recording possible answer positions by marked_zero
    marked_zero = []
    while (True in zero_bool_mat_copy):
        min_zero_row(zero_bool_mat_copy, marked_zero)

    # Reference:
    # you can use this procedure to get the marked_rows and marked_cols:
    # 1、Mark rows that do not contain marked 0 elements and store row indexes in the non_marked_row
    # 2、Search non_marked_row element, and find out if there are any unmarked 0 elements in the corresponding column
    # 3、Store the column indexes in the marked_cols
    # 4、Compare the column indexes stored in marked_zero and marked_cols
    # 5、If a matching column index exists, the corresponding row_index is saved to non_marked_rows
    # 6、Next, the row indexes that are not in non_marked_row are stored in marked_rows
    return (marked_zero,[], [])


def adjust_matrix(mat, cover_rows, cover_cols):
    cur_mat = mat
    non_zero_element = []

    # Find the minimum value for an element that is not in marked_rows and not in marked_cols
    for row in range(len(cur_mat)):
        if row not in cover_rows:
            for i in range(len(cur_mat[row])):
                if i not in cover_cols:
                    non_zero_element.append(cur_mat[row][i])
    min_num = min(non_zero_element)

    # Subtract the elements which not in marked_rows nor marked_cols from the min_num
    for row in range(len(cur_mat)):
        if row not in cover_rows:
            for i in range(len(cur_mat[row])):
                if i not in cover_cols:
                    cur_mat[row, i] = cur_mat[row, i] - min_num

    # Add the element in marked_rows, which is also in marked_cols, to the min_num
    for row in range(len(cover_rows)):
        for col in range(len(cover_cols)):
            cur_mat[cover_rows[row], cover_cols[col]] = cur_mat[cover_rows[row], cover_cols[col]] + min_num
    return cur_mat


def hungarian_algorithm(mat):
    dim = mat.shape[0]
    cur_mat = mat

    # Step 1 & 2 - Every column and every row subtract its internal minimum
    for row_num in range(mat.shape[0]):
        cur_mat[row_num] = cur_mat[row_num] - np.min(cur_mat[row_num])

    for col_num in range(mat.shape[1]):
        cur_mat[:, col_num] = cur_mat[:, col_num] - np.min(cur_mat[:, col_num])
    zero_count = 0
    while zero_count < dim:
        # Step 3 & 4
        marked_zero, marked_rows, marked_cols = mark_matrix(cur_mat)
        zero_count = len(marked_rows) + len(marked_cols)

        if zero_count < dim:
            cur_mat = adjust_matrix(cur_mat, marked_rows, marked_cols)

    return marked_zero


def ans_calculation(mat, pos):
    total = 0
    ans_mat = np.zeros((mat.shape[0], mat.shape[1]))
    for i in range(len(pos)):
        total += mat[pos[i][0], pos[i][1]]
        ans_mat[pos[i][0], pos[i][1]] = mat[pos[i][0], pos[i][1]]
    return total, ans_mat


def main():
    '''Hungarian Algorithm:
    Finding the minimum value in linear assignment problem.
    Therefore, we can find the minimum value set in net matrix
    by using Hungarian Algorithm. In other words, the maximum value
    and elements set in cost matrix are available.'''

    # The matrix who you want to find the minimum sum
    cost_matrix = np.array([[7, 6, 2, 9, 2],
                            [1, 2, 5, 3, 9],
                            [5, 3, 9, 6, 5],
                            [9, 2, 5, 8, 7],
                            [2, 5, 3, 6, 1]])

    marked_zero = hungarian_algorithm(cost_matrix.copy())  # Get the element position.
    ans, ans_mat = ans_calculation(cost_matrix, marked_zero)  # Get the minimum or maximum value and corresponding matrix.

    # Show the result
    print(f"Linear Assignment problem result: {ans:.0f}\n{ans_mat}")


if __name__ == '__main__':
    main()