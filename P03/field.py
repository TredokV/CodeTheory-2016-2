from polynomial import PolynomialZ2

class GF(object):
    """ Field Fq = Zn/<f(x)> w/deg(f) <= 31"""
    def __init__(self, exponent, poly, root):
        super(GF, self).__init__()
        self.gpolynomial = PolynomialZ2(poly)
        self.alpha = PolynomialZ2(root)
        self.len = pow(2, exponent)

        if self.gpolynomial.degree != exponent or self.alpha.degree >= self.gpolynomial.degree:
            raise ValueError()

        # generate field -- just multiplicative group
        self.elements = [PolynomialZ2('1'), self.alpha]
        self.pow = {self.elements[0]: 0, self.alpha: 1}
        for i in range(2, self.len - 1):
            n = (self.elements[-1] * self.alpha) % self.gpolynomial
            self.elements.append(n) # agregar elemento
            self.pow[n] = i # potencia de la raíz
        assert((self.elements[-1] * self.alpha) % self.gpolynomial == self.elements[0])

    def each(self):
        for i in self.elements:
            yield i

    def sum(self, poly1, poly2):
        return (poly1 + poly2) % self.gpolynomial

    def gproduct(self, poly1, poly2):
        return (poly1 * poly2) % self.gpolynomial

    def product(self, poly1, poly2):
        if poly1.is_zero():
            return self.zero()
        if poly2.is_zero():
            return self.zero()

        i = self.pow[poly1]
        j = self.pow[poly2]
        return self.elements[(i + j) % (self.len - 1)]

    # creates a polynomial inside Fq
    def reduce(self, i):
        p = PolynomialZ2(i, bytestring=False)
        if p.degree >= self.gpolynomial.degree:
            p = p % self.gpolynomial
        return p

    def zero(self):
        return PolynomialZ2()

    def unity(self):
        return self.elements[0]

    def division(self, poly1, poly2):
        i = self.pow[poly1]
        j = self.pow[poly2]
        return self.elements[(i - j) % (self.len - 1)]

    def __len__(self):
        return self.len

    def __getitem__(self, key):
        return self.elements[key]

    @staticmethod
    def aes():
        return GF(8, '100011011', '11') # Generado por el polinomio usado en AES

    @staticmethod
    def primitive():
        return GF(8, '100011101', '10') # Generado por polinomio primitivo

    @staticmethod
    def qr():
        return GF(2, '111', '10')
