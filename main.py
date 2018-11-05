from math import inf


class IsNotRegular(Exception):
    pass


class Result:
    def __init__(self, sub, pref, suf, word):
        self.sub = sub
        self.pref = pref
        self.suf = suf
        self.word = word


class Operator:
    def val(self):
        pass

    def do(self, *args):
        pass


class BadLetter(Operator):
    def val(self):
        return 0

    def do(self):
        return Result(0, 0, 0, -inf)


class GoodLetter(Operator):
    def val(self):
        return 0

    def do(self):
        return Result(1, 1, 1, 1)


class One(Operator):
    def val(self):
        return 0

    def do(self):
        return Result(0, 0, 0, 0)


class Mul(Operator):
    def val(self):
        return 2

    def do(self, a : Result, b : Result):
        return Result(max(a.sub, b.sub, a.suf + b.pref),
                      max(a.pref, a.word + b.pref),
                      max(b.suf, b.word + a.suf),
                      a.word + b.word)


class Sum(Operator):
    def val(self):
        return 2

    def do(self, a : Result, b : Result):
        return Result(max(a.sub, b.sub),
                      max(a.pref, b.pref),
                      max(a.suf, b.suf),
                      max(a.word, b.word))


class Star(Operator):
    def val(self):
        return 1

    def do(self, a : Result):
        if (a.word > 0):
            return Result(inf, inf, inf, inf)
        else:
            return Result(max(a.sub, a.pref + a.suf),
                          a.pref, a.suf, a.word)


def operator_by_sym(c, x):
    if (c == '1'):
        return One()
    elif (c == '.'):
        return Mul()
    elif (c == '+'):
        return Sum()
    elif (c == '*'):
        return Star()
    elif (c in {'a', 'b', 'c'}):
        if c == x:
            return GoodLetter()
        else:
            return BadLetter()
    else:
        raise IsNotRegular()


def solve(alpha, x):
    stack = []

    for c in alpha:
        op = operator_by_sym(c, x)
        if len(stack) < op.val():
            raise IsNotRegular()
        args = [stack.pop() for i in range(op.val())]
        args.reverse()
        res = op.do(*args)
        stack.append(res)

    if (len(stack) != 1):
        raise IsNotRegular()
    else:
        return stack[0].sub


if __name__ == "__main__":
    args = input().split()
    try:
        print(str(solve(*args)).upper())
    except IsNotRegular:
        print("ERROR")
