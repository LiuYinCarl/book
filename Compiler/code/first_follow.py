# 计算 first 集和 follow 集


from prettytable import PrettyTable


class Parser(object):
    def __init__(self, grammars:list):
        self.grammars = grammars
        self.terms = set() # 终结符
        self.nonterms = set() # 非终结符

        self.parse_symbol()
        self.calc_first_and_follow()
        self.print()

        
    def parse_symbol(self):
        """分析文法，找出终结符和非终结符."""
        for grammar in self.grammars:
            # 文法左侧的一定是非终结符
            # 小写的一定是终结符，大写的一定是非终结符
            gram = grammar.split("->")
            left_sym = gram[0].strip()
            self.nonterms.add(left_sym)
            right_syms = [s for s in gram[1].split(" ") if s]
            for sym in right_syms:
                if sym.isupper():
                    self.nonterms.add(sym)
                else:
                    self.terms.add(sym)


    def calc_first_and_follow(self):
        self.tab = {}
        for sym in self.terms:
            self.tab[sym] = { "nullable": False, "FIRST": set(), "FOLLOW": set() }
            self.tab[sym]["FIRST"].add(sym)
        for sym in self.nonterms:
            self.tab[sym] = { "nullable": False, "FIRST": set(), "FOLLOW": set() }

        change = True
        while change:
            change = False
            for grammar in self.grammars:
                gram = grammar.split("->")
                l_sym = gram[0].strip()
                r_syms = [s for s in gram[1].split(" ") if s]
                # 计算 nullable
                res = filter(lambda sym: self.tab[sym]["nullable"], r_syms)
                if len(r_syms) == len(list(res)) and not self.tab[l_sym]["nullable"]:
                    self.tab[l_sym]["nullable"] = True
                    change = True


                for i in range(len(r_syms)):
                    res = filter(lambda sym: self.tab[sym]["nullable"], r_syms[0:i])
                    if len(r_syms[0:i]) == len(list(res)):
                        l_first = self.tab[l_sym]["FIRST"]
                        r_first = self.tab[r_syms[i]]["FIRST"]
                        if l_first != l_first.union(r_first):
                            self.tab[l_sym]["FIRST"] = l_first.union(r_first)
                            change = True


                    res = filter(lambda sym: self.tab[sym]["nullable"], r_syms[i+1:])
                    if len(r_syms[i+1:]) == len(list(res)):
                        l_follow = self.tab[l_sym]["FOLLOW"]
                        r_follow = self.tab[r_syms[i]]["FOLLOW"]
                        if r_follow != r_follow.union(l_follow):
                            self.tab[r_syms[i]]["FOLLOW"] = r_follow.union(l_follow)
                            change = True

                for i in range(len(r_syms)):
                    for j in range(i+1, len(r_syms)):
                        res = filter(lambda sym: self.tab[sym]["nullable"], r_syms[i+1:j])
                        if len(r_syms[i+1:j]) == len(list(res)):
                            i_follow = self.tab[r_syms[i]]["FOLLOW"]
                            j_first = self.tab[r_syms[j]]["FIRST"]
                            if i_follow != i_follow.union(j_first):
                                self.tab[r_syms[i]]["FOLLOW"] = i_follow.union(j_first)
                                change = True
                                
    def print(self):
        print("TERM: {}".format(self.terms))
        print("NONTERM: {}".format(self.nonterms))

        tb = PrettyTable()
        tb.field_names = ["SYM", "nullable", "FIRST", "FOLLOW"]
        tab = sorted(self.tab.items(), key=lambda d: d[0])
        for sym, v in tab:
            if sym.isupper():
                tb.add_row([sym, v["nullable"], " ".join(v["FIRST"]), " ".join(v["FOLLOW"])])
        print(tb)
                

# 定义文法
grammars = [
    "Z -> d",
    "Z -> X  Y Z",
    "Y -> ",
    "Y -> c",
    "X -> Y",
    "X -> a",
]

grammars2 = [
    "S -> A B",
    "S -> b C",
    "A -> ",
    "A -> b",
    "B -> ",
    "B -> a D",
    "C -> A D",
    "C -> b",
    "D -> a S",
    "D -> c",
]

grammars3 = [
    "E -> E + T",
    "E -> E - T",
    "E -> T",
    "T -> T * F",
    "T -> T / F",
    "T -> F",
    "F -> id",
    "F -> num",
    "F -> ( E )",
]

grammars4 = [
    "S -> E $",
    "E -> T E'",
    "E' -> + T E'",
    "E' -> - T E'",
    "E' -> ",
    "T -> F T'",
    "T' -> * F T'",
    "T' -> / F T'",
    "T' -> ",
    "F -> id",
    "F -> num",
    "F -> ( E )",
]

parser = Parser(grammars4)
