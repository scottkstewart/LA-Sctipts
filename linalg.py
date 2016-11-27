#!/usr/bin/env python3
import re
import copy

def print_matrix(matrix):
    '''Print the elements of a matrix enclosed in |'''
    for row in matrix:
        print('|', end='')
        for element in row:
            print('{:.1f}'.format(element) if element else '0.0', end=' ')
        print('|')

def input_matrix(size=(0,0), prompt='Input the elements of the matrix in order'):
    '''Input a matrix, prompting for size if necessary''' 
    if not size[0]:
        size = [int(num) for num in re.split('\D', input('What size is the matrix?\n'))]
    
    # finds elements sequentially
    print(prompt)
    nums = []
    while len(nums) < size[0]*size[1]:
        nums.extend([float(num) for num in re.findall(r'-?\d+\.?\d*', input())])
    # returns 2D list representing matrix
    return [nums[size[1]*row:size[1]*(row+1)] for row in range(size[0])]

identity = lambda size: [[1 if i == j else 0 for j in range(size)] for i in range(size)]

def product(left, right):
    '''Multiply two matrices'''
    # check that the matrices are able to be multiplied
    assert len(left[0]) == len(right)
   
    if not hasattr(right[0], '__iter__'):
        right = [[element] for element in right]

    matrix = [[0 for j in range(len(right[0]))] for i in range(len(left))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            for k in range(len(right)):
                matrix[i][j] += left[i][k]*right[k][j]

    return matrix

def determinant(matrix, minor_row=None, minor_col=None):
    '''Recursively calculate determinant based on expansion by cofactors on the first column'''
    # make sure matrix is square 
    assert len(matrix) == len(matrix[0])
   
    # make minor if necessary
    if minor_row is not None:
        del matrix[minor_row]
        for row in matrix:
            del row[minor_col]
    
    # base case; element of 1x1 matrix is determinant
    if len(matrix) == 1:
        return matrix[0][0]

    # recursively sum cofactors based on the exuation sum (-1)^i+j * aij * muij(A)
    sum = 0
    for ind, row in enumerate(matrix):
        sum += (-1 if ind%2 else 1)*row[0]*determinant(copy.deepcopy(matrix), ind, 0)
    return sum

def inverse(matrix):
    '''Calculates inverse using determinant'''
    det = determinant(matrix)
   
    # check invertability
    assert det != 0
    
    # return the inverse based on the cofactor/determinant
    return [[(-1 if (row+col)%2 else 1)*determinant(copy.deepcopy(matrix), row, col)/det for row in range(len(matrix))] for col in range(len(matrix))]

# separated for efficiency in case of several right vectors
solve = lambda left, right: product(inverse(left), right)

def linear_system():
    '''Return the solution to a requested linear system of equations using multiplication by the inverse'''
    size = [int(num) for num in re.split('\D', input('What size is the system? (equations x unknowns)\n'))]
    left_equations = input_matrix(size, 'Input the coefficients for the left side of the system:')
    right_equations = input_matrix((size[0], 1), 'Input the right side of the system:')
    return solve(left_equations, right_equations)

def row_plus_another(recipient, donor, coefficient):
    '''Modifies one row in-place to add a coefficient times another'''
    assert len(recipient) == len(donor)
    for ind in range(len(recipient)):
        recipient[ind] += coefficient*donor[ind]

def lu_decomposition(matrix):
    '''Returns a tuple representing the LU decomposition of a particular matrix'''
    lower = identity(len(matrix))
    upper = copy.deepcopy(matrix)
    for pivot_ind in range(len(upper)-1):
        pivot_reciprocal = 1/upper[pivot_ind][pivot_ind]
        for row in range(pivot_ind+1, len(upper)):
            if upper[row][pivot_ind]:
                coefficient = upper[row][pivot_ind]*pivot_reciprocal
                row_plus_another(upper[row], upper[pivot_ind], 0-coefficient)
                lower[row][pivot_ind] = coefficient
    return (lower, upper)

def power_method(lu, iterations=5, estimate=None):
    '''Returns the dominant eigenvalue and accompanying eigenvector of a matrix with supplied LU decoposition,
    given the nxn matrix has n linearly independent eigenvectors, and a single real dominant eigenvalue.'''
    # give basic estimate if not supplied
    if estimate == None:
        estimate = [1 for i in range(len(lu[0]))]
    
    # refine estimate vector over the supplied number of iterations
    for i in range(iterations):
        estimate = solve(lu[1], solve(lu[0], estimate))

        eigenvalue = 0
        for row in estimate:
            for member in row:
                if abs(member) > abs(eigenvalue):
                    eigenvalue = member
       
        for row in estimate:
            row[0] /= eigenvalue

    return (1/eigenvalue, estimate)
