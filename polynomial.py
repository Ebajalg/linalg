
class Polynomial:
    def __init__(self, equation):
        # TODO: Add error messages for invalid equation inputs
        equation_terms = list(filter(''.__ne__, equation.replace('+', ',').replace('-', ',-').split(',')))
        self.powers = [float(term[term.index('x')+2:len(term)]) if ('^' in term)
                       else (1 if ('x' in term)
                             else 0)
                       for term in equation_terms]

        self.constants = [float({'': '1', '-': '-1'}.get(term[0:term.index('x')], term[0:term.index('x')]))
                          if ('x' in term)
                          else (float(term) if (term != '') else 0)
                          for term in equation_terms]

        self.p_cs = {a:b for a,b in zip(self.powers, self.constants)}

    # TODO: Add functionality for multiple types of other
    def __mul__(self, other):
        output_p = Polynomial("")
        output_p.p_cs = {}
        if isinstance(other, Polynomial):
            for i in self.p_cs.keys():
                for j in other.p_cs.keys():
                    if (i + j) in output_p.p_cs.keys():
                        output_p.p_cs[i + j] = output_p.p_cs[i + j] + self.p_cs[i]*other.p_cs[j]
                    else:
                        output_p.p_cs[i + j] = self.p_cs[i]*other.p_cs[j]
        elif isinstance(other, float) or isinstance(other, int):
            output_p = self * Polynomial(str(other))
        else:
            error_message = f"Type {type(other)} is not supported for multiplication with a polynominal object"
            raise TypeError(error_message)
        output_p.powers = list(output_p.p_cs.keys())
        output_p.constants = list(output_p.p_cs.values())
        return output_p

    def __add__(self, other):
        output_p = Polynomial("")
        if isinstance(other, Polynomial):
            output_p.powers = list(set(self.powers + other.powers))
            output_p.p_cs = {i: self.p_cs.get(i, 0) + other.p_cs.get(i, 0) for i in output_p.powers}
        elif isinstance(other, float) or isinstance(other, int):
            output_p = self + Polynomial(str(other))
        else:
            error_message = f"Type {type(other)} is not supported for addition with a polynominal object"
            raise TypeError(error_message)
        for i in list(output_p.p_cs.keys()).copy():
            print(i)
            if output_p.p_cs[i] == float(0):
                del output_p.p_cs[i]
                output_p.powers.remove(i)
        output_p.constants = output_p.p_cs.values()
        return output_p

    def __sub__(self, other):
        output_p = Polynomial("")
        if isinstance(other, Polynomial):
            output_p.powers = list(set(self.powers + other.powers))
            output_p.p_cs = {i: self.p_cs.get(i, 0) - other.p_cs.get(i, 0) for i in output_p.powers}
            output_p.constants = output_p.p_cs.values()
        elif isinstance(other, float) or isinstance(other, int):
            output_p = self - Polynomial(str(other))
        else:
            error_message = f"Type {type(other)} is not supported for subtraction with a polynominal object"
            raise TypeError(error_message)
        for i in list(output_p.p_cs.keys()).copy():
            print(i)
            if output_p.p_cs[i] == float(0):
                del output_p.p_cs[i]
                output_p.powers.remove(i)
        output_p.constants = output_p.p_cs.values()
        return output_p

    __rmul__ = __mul__
    __radd__ = __add__

    def __rsub__(self, other):
        print(self)
        print(other)
        return Polynomial(str(other)) - self

    # TODO: Add functionality for __rsub__

    def f(self, x):
        return sum(self.p_cs[i]*(x**i) for i in self.p_cs)

    def show(self):
        print('+'.join([f"{self.p_cs[i]}x^{i}"
                        for i in self.p_cs.keys()]
                       ).replace('+-', '-').replace('x^0', ''))
