#!/usr/bin/env python3
from copy import deepcopy
import re

def print_matrix(matrix):
    '''Print the elements of a matrix enclosed in |'''
    for row in matrix:
        print('|', end='')
        for element in row:
            print(element, end=' ')
        print('|')

def input_matrix(size=(0,0)):
    '''Input a matrix, prompting for size if necessary''' 
    if not size[0]:
        size = [int(num) for num in re.split('\D', input('What size is the matrix?\n'))]
    
    # finds elements sequentially
    print('Input the elements of the martix in order')
    nums = []
    while len(nums) < size[0]*size[1]:
        nums.extend([int(num) for num in re.findall(r'-?\d+', input())])
    # returns 2D list representing matrix
    return [nums[size[1]*row:size[1]*(row+1)] for row in range(size[0])]
    
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
        sum += (-1 if ind%2 else 1)*row[0]*determinant(deepcopy(matrix), ind, 0)
        print(sum)
    return sum

if __name__ == '__main__':
    # calculate determinant
    print(determinant(input_matrix()))
