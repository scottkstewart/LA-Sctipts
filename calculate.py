#!/usr/bin/env python3
import linalg
if __name__ == '__main__':
    resp = input("What would you like to do?\n1)Find an inverse\n2)Find a determinant\n3)Solve a linear system of equations"
                 "\n4)Multiply two matrices\n5)Find LU Decomposition\n6)Find dominant eigenvalue with accompanying eigenvector\n")
    if resp == '1':
        linalg.print_matrix(linalg.inverse(linalg.input_matrix()))
    elif resp == '2':
        print(linalg.determinant(linalg.input_matrix()))
    elif resp == '3':
        print_matrix(linalg.linear_system())
    elif resp == '4':
        linalg.print_matrix(linalg.product(linalg.input_matrix(prompt='Input left matrix in order'), linalg.input_matrix(prompt='Input right matrix in order')))
    elif resp == '5':
        lu = linalg.lu_decomposition(linalg.input_matrix())
        linalg.print_matrix(lu[0])
        linalg.print_matrix(lu[1])
    elif resp == '6':
        lu = linalg.lu_decomposition(linalg.input_matrix())
        value, vector = linalg.power_method(lu, int(input('How many iterations?\n')), linalg.input_matrix((len(lu[0]),1), 'Input an estimate'))
        print('Eigenvalue: {}\nEigenvector: {}'.format(value, [row[0] for row in vector]))
    else:
        print('selection not valid')
