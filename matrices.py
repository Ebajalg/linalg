from math import floor, ceil


def dot_product(v1, v2):
    if len(v1) == len(v2):
        return sum([a * b for a, b in zip(v1, v2)])
    else:
        error_string = "Can't find dot product between two vectors as they are not in the same dimension: v1 - {len(" \
                       "v1)}, v2 - {len(v2)} "
        raise ValueError(error_string)


class Matrix:
    def __init__(self, rows, cols, values=None, reduced_matrix=False, transposed_matrix=False):
        self.tr = 0
        self.rank = 0
        self.e_values = []
        self.c_poly = {}
        self.dims = (rows, cols)
        self.values = [[0 for i in range(self.dims[1])]
                       for i in range(self.dims[0])]

        if values is None:
            self.input_values()
        else:
            if (len(values) == rows) and (len(values[0]) == cols):
                if list(map(len, values)) == [cols for i in range(rows)]:
                    self.values = values
                else:
                    error_string = "Inputted matrix is not uniform"
                    raise ValueError(error_string)
            else:
                error_string = f"""Number of rows and columns does not match dimensions of inputted matrix: 
                Number of rows: {rows}
                Number of columns: {cols}
                Inputted matrix dimensions: {len(values)}x{len(values[0])}"""
                raise ValueError(error_string)

        self.det = self.determinant()

        # TODO: fix function calling loop when new functions are made
        # if not reduced_matrix:
        #    self.r_m = self.reduce()

        # if not transposed_matrix:
        #    self.t_m = self.transpose()

    # Code of addition of two matrix objects
    def __add__(self, other):
        if isinstance(other, Matrix):
            if self.dims == other.dims:
                new_values = [[a + b for a, b in zip(self.values[i], other.values[i])]
                              for i in range(self.dims[0])]
                output_matrix = Matrix(*self.dims, values=new_values)
                output_matrix.show()
                return output_matrix
            else:
                error_string = f"Dimesions of the matrices do not match: Matrix1{self.dims} != Matrix2{other.dims}"
                raise ValueError(error_string)
        else:
            error_string = f"Object of type {type(other)} is not compatible with type Matrix for addition"
            raise ValueError(error_string)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.dims[1] == other.dims[0]:
                other_M_T = other.transpose()
                output_values = [[dot_product(a, b) for a in other_M_T.values]
                                 for b in self.values]
                output_matrix = Matrix(self.dims[0], other.dims[1], values=output_values)
        elif isinstance(other, int) or isinstance(other, float):
            output_values = [[other * a for a in self.values[i]]
                             for i in range(len(self.values))]
            output_matrix = Matrix(self.dims[0], self.dims[1], values=output_values)
        else:
            error_string = f"Object of type {type(other)} is not compatible with type Matrix for multiplication"
            raise ValueError(error_string)

        return output_matrix

    def transpose(self):
        t_M = Matrix(self.dims[1],
                     self.dims[0],
                     [[self.values[i][j] for i in range(self.dims[0])] for j in range(self.dims[1])],
                     transposed_matrix=True)
        return t_M

    def determinant(self):
        if self.dims[0] == self.dims[1]:
            if self.dims == (2, 2):
                det = self.values[0][0] * self.values[1][1] - self.values[0][1] * self.values[1][0]
            else:
                det = sum([self.values[0][i] * ((-1) ** (i + 2)) * Matrix(self.dims[0] - 1,
                                                               self.dims[1] - 1,
                                                               [[a[b] for b in range(len(a)) if b != i] for r, a in
                                                                zip(range(len(self.values)), self.values) if r != 0]
                                                               ).determinant()
                           for i in range(len(self.values[0]))
                           if self.values[0][i] != 0])
        else:
            raise ValueError("Matrix is not square hence a determinant cannot be found")
        return det

    def adjugate(self):
        a_M = Matrix(*self.dims,
                     [[self.values[i][j] for i in range(self.dims[0])] for j in range(self.dims[1])])
        for i in range(a_M.dims[0]):
            for j in range(a_M.dims[1]):
                a_M.values[i][j] = ((-1) ** (i + j + 2)) * Matrix(self.dims[0] - 1,
                                          self.dims[1] - 1,
                                          [[a[b] for b in range(len(a)) if b != j] for r, a in
                                          zip(range(len(self.values)), self.values) if r != i]
                                          ).determinant()
        return a_M

    def inverse(self):
        i_M = self.adjugate() * (1/self.det)
        return i_M

    # Returns row echelon form of the matrix
    def reduce(self):
        r_M = Matrix(self.dims[0],
                     self.dims[1],
                     self.values.copy(),
                     reduced_matrix=True)
        l_1_rs = []
        for i in range(r_M.dims[1]):
            for j in range(r_M.dims[0]):
                if (r_M.values[j][i] != 0) and not (j in l_1_rs):
                    r_M.values[j] = list(map(lambda x: x / r_M.values[j][i], r_M.values[j]))
                    for a in range(r_M.dims[0]):
                        if a != j:
                            r_M.values[a] = [v2 - r_M.values[a][i] * v1
                                             for v1, v2 in zip(r_M.values[j], r_M.values[a])]
                    l_1_rs.append(j)
        self.rank = len(l_1_rs)
        return r_M

    # Outputs visualisation of matrix
    def show(self):
        max_val_length = max(list(map(lambda y: max(list(map(lambda x: len(str(x)), y))), self.values)))
        for i in self.values:
            print("|", " ".join(list(map(lambda x: (' ' * floor((max_val_length * 2 - len(str(x))) / 2)) +
                                                   str(x) +
                                                   (' ' * ((ceil((max_val_length * 2 - len(str(x))) / 2)) - 1))
                                         , i))), "|")

    # Allows for the input of values in human-readable form
    def input_values(self):
        for i in range(self.dims[0]):
            for j in range(self.dims[1]):
                self.values[i][j] = 'X'
                self.show()
                val = input(">: ")
                while not val.replace(".", "").replace("-", "").isnumeric():
                    print(f"'{val}' is not numeric")
                    val = input(">: ")
                self.values[i][j] = float(val)
