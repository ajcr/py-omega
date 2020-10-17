from copy import deepcopy
from functools import total_ordering


def is_non_negative_int(n):
    return n >= 0 and isinstance(n, int)


@total_ordering
class Ordinal:
    r"""
    An infinite ordinal less than \epsilon_0.

    """
    def __init__(self, exponent=1, coefficient=1, addend=0):
        self.exponent = exponent
        self.coefficient = coefficient
        self.addend = addend
        
    def _repr_latex_(self):
        return rf"${self}$"

    def __repr__(self):
        term = "w"

        if self.exponent != 1:
            term += f"^({self.exponent})"

        if self.coefficient != 1:
            term += rf"*{self.coefficient}"

        if self.addend != 0:
            term += f" + {self.addend}"

        return f"({term})"

    def __str__(self):
        term = r"\omega"

        if self.exponent != 1:
            term += f"^{{{self.exponent}}}"

        if self.coefficient != 1:
            term += rf"\cdot{self.coefficient}"

        if self.addend != 0:
            term += f"+{self.addend}"

        return term

    def __eq__(self, other):
        try:
            return (
                self.exponent == other.exponent and
                self.coefficient == other.coefficient and
                self.addend == other.addend
            )
        except AttributeError:
            return False

    def __lt__(self, other):
        if is_non_negative_int(other):
            return False
        try:
            return (
                self.exponent < other.exponent or
                self.coefficient < other.coefficient or
                self.addend < other.addend
            )
        except AttributeError:
            raise NotImplemented

    def __gt__(self, other):
        if is_non_negative_int(other):
            return True
        try:
            return (
                self.exponent > other.exponent or
                self.coefficient > other.coefficient or
                self.addend > other.addend
            )
        except AttributeError:
            raise NotImplemented

    def __add__(self, other):
        if is_non_negative_int(other) or self.exponent > other.exponent:
            return Ordinal(
                exponent=deepcopy(self.exponent),
                coefficient=self.coefficient,
                addend=self.addend + other,
            )

        elif self.exponent == other.exponent:

            if isinstance(self.addend, int):
                new_addend = deepcopy(other.addend)
            else:
                new_addend = self.addend + other.addend

            return Ordinal(
                exponent=deepcopy(self.exponent),
                coefficient=self.coefficient + other.coefficient,
                addend=new_addend,
            )

        return deepcopy(other)

    def __radd__(self, other):
        if is_non_negative_int(other):
            return deepcopy(self)
        raise NotImplemented

    def __mul__(self, other):
        if other == 0:
            return 0

        if is_non_negative_int(other):
            return Ordinal(
                exponent=deepcopy(self.exponent),
                coefficient=self.coefficient * other,
                addend=deepcopy(self.addend),
            )

        return Ordinal(
            exponent=self.exponent + other.exponent,
            coefficient=other.coefficient,
            addend=self.addend * other.addend + self * other.addend,
        )

    def __rmul__(self, other):
        if other == 0:
            return 0
        elif is_non_negative_int(other):
            return deepcopy(self)
        raise NotImplemented

    def __pow__(self, other):
        if other == 0:
            return 1

        if is_non_negative_int(other):
            return Ordinal(
                exponent=self.exponent * other,
                coefficient=self.coefficient,
                addend=self.addend * self,
            )

        return

    def __rpow__(self, other):
        return other ** self
