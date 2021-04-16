import sys

def determinant_recursive(A, total=0):
    # Section 1: store indices in list for row referencing
    indices = list(range(len(A)))

    # Section 2: when at 2x2 submatrices recursive calls end
    if len(A) == 2 and len(A[0]) == 2:
        val = A[0][0] * A[1][1] - A[1][0] * A[0][1]
        return val

    # Section 3: define submatrix for focus column and
    #      call this function
    for fc in indices:  # A) for each focus column, ...
        # find the submatrix ...
        As = A[:]  # B) make a copy, and ...
        As = As[1:]  # ... C) remove the first row
        height = len(As)  # D)

        for i in range(height):
            # E) for each remaining row of submatrix ...
            #     remove the focus column elements
            As[i] = As[i][0:fc] + As[i][fc + 1:]

        '''
             -  +
        +[3, 4, 7]
             +  -        
        -[8, 4, 8]
             -  +
        +[2, 1, 1]
        '''

        sign = (-1) ** (fc % 2)  # F)
        # G) pass submatrix recursively
        sub_det = determinant_recursive(As)
        # H) total all returns from recursion
        total += sign * A[0][fc] * sub_det

    return total

def print_matrix(Title, M):
    print(Title)
    for row in M:
        print([round(x, 3) + 0 for x in row])

def print_matrices(Action, Title1, M1, Title2, M2):
    print(Action)
    print(Title1, '\t' * int(len(M1) / 2) + "\t" * len(M1), Title2)
    for i in range(len(M1)):
        row1 = ['{0:+7.3f}'.format(x) for x in M1[i]]
        row2 = ['{0:+7.3f}'.format(x) for x in M2[i]]
        print(row1, '\t', row2)

def zeros_matrix(rows, cols):
    A = []
    for i in range(rows):
        A.append([])
        for j in range(cols):
            A[-1].append(0.0)

    return A

def copy_matrix(M):
    rows = len(M)
    cols = len(M[0])

    MC = zeros_matrix(rows, cols)

    for i in range(rows):
        for j in range(rows):
            MC[i][j] = M[i][j]

    return MC

def matrix_multiply(A, B):
    rowsA = len(A)
    colsA = len(A[0])

    rowsB = len(B)
    colsB = len(B[0])

    if colsA != rowsB:
        print('Number of A columns must equal number of B rows.')
        sys.exit()

    C = zeros_matrix(rowsA, colsB)

    for i in range(rowsA):
        for j in range(colsB):
            total = 0
            for ii in range(colsA):
                total += A[i][ii] * B[ii][j]
            C[i][j] = total

    return C

def identity_matrix(n):
    I = []
    for i in range(n):
        I.append([])
        for j in range(n):
            if i == j:
                I[i].append(1)
            else:
                I[i].append(0)
    return I

def invert_matrix(A, tol=None):
    """
    Returns the inverse of the passed in matrix.
        :param A: The matrix to be inversed

        :return: The inverse of the matrix A
    """
    # Section 1: Make sure A can be inverted.

    # Section 2: Make copies of A & I, AM & IM, to use for row ops
    n = len(A)
    AM = copy_matrix(A)
    I = identity_matrix(n)
    IM = copy_matrix(I)

    # Section 3: Perform row operations
    indices = list(range(n))  # to allow flexible row referencing ***
    for fd in range(n):  # fd stands for focus diagonal
        fdScaler = 1.0 / AM[fd][fd]
        # FIRST: scale fd row with fd inverse.
        for j in range(n):  # Use j to indicate column looping.
            AM[fd][j] *= fdScaler
            IM[fd][j] *= fdScaler
        # SECOND: operate on all rows except fd row as follows:
        for i in indices[0:fd] + indices[fd + 1:]:
            # *** skip row with fd in it.
            crScaler = AM[i][fd]  # cr stands for "current row".
            for j in range(n):
                # cr - crScaler * fdRow, but one element at a time.
                AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
                IM[i][j] = IM[i][j] - crScaler * IM[fd][j]

    # Section 4: Make sure IM is an inverse of A with specified tolerance
    # if check_matrix_equality(I, matrix_multiply(A, IM), tol):
    return IM
    # else:
    #     raise ArithmeticError("Matrix inverse out of tolerance.")

def swap_rows(A, index):
    I = identity_matrix(len(A))
    flag = False
    for i in range(index + 1, len(A)):
        if A[index][i] != 0 and A[i][index] != 0:
            I[index], I[i] = I[i], I[index]
            A = matrix_multiply(I, A)
            flag = True
            break
    return A



def gauss_elimination_L_U(A):
    size = len(A)
    flag = True
    L = identity_matrix(size)
    for i in range(len(A)):
        dominant = A[i][i]
        for j in range(i + 1, size):
            I = identity_matrix(size)
            if dominant == 0:
                flag = swap_rows(A, i)
            if flag == False:
                raise Exception("The matrix contain 0 on the diagonal with no option to interchange rows and fix it.")
            I[j][i] = -1 * A[j][i] / dominant
            A = matrix_multiply(I, A)
            Temp = invert_matrix(I)
            L[j][i] = Temp[j][i]

    print_matrix("U", A)
    print_matrix("L", L)






b = [[1],
     [2],
     [1],
     [2]]

A = [
    [1, 2, 1, 0, 0],
    [2, 0, 1, 0 ,0],
    [1, 1, 4, 1, 1],
    [2, 3, 5, 0, 0],
    [9, 9, 0, 2, 1]
]

# print_matrix("Stam", res)

print_matrix("A", A)
print_matrix("A after changing rows 2, 3", swap_rows(A, 0))
# gauss_elimination_L_U(A)
