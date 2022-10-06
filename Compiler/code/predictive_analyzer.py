# 构造预测分析器

from first_follow import FirstFollowParser
import prettytable


class PredictiveAnalyzer(object):
    def __init__(self, flparser:FirstFollowParser):
        self.flparser:FirstFollowParser = flparser
        self.nonterms:list = list(self.flparser.nonterms)
        self.terms:list = list(self.flparser.terms)
        self.nonterms.sort()
        self.terms.sort()
        self.pa_table = []
        for _ in range(len(self.nonterms)):
            tmp = []
            for _ in range(len(self.terms)):
                tmp.append(None)
            self.pa_table.append(tmp)

        self.gen_pa_table()
        self.print_pa_table()


    def get_first(self, gram:str):
        first = set()
        is_nullable = False

        right_syms = [s for s in gram.split(" ") if s]
        if not right_syms:
            # 特殊处理 "S -> " 右侧为空的产生式
            is_nullable = True
        for sym in right_syms:
            first_of_sym = self.flparser.tab[sym]["FIRST"]
            nullable = self.flparser.tab[sym]["nullable"]
            for i in first_of_sym:
                first.add(i)
            print(sym, self.flparser.tab[sym])
            if not nullable:
                break
            else:
                is_nullable = True
        if gram.strip() == "B b S":
            print("-------- ", first)
        return first, is_nullable

    def gen_pa_table(self):
        """
        LL(1)预测分析表的构造算法
        对文法G的每个产生式A->α 执行如下步骤：
        1. 对每个a∈First(α)，把 A->α 加入M[A,a]
        2. 若 ε∈First(α), 则对任何b∈Follow(A) ,把 A-> ε加至M[A,b]中
        """
        for gram in self.flparser.grammars:
            l_gram, r_gram = gram.split("->")
            l_gram = l_gram.strip()
            first, is_nullable = self.get_first(r_gram)
            # print(first, is_nullable)
            for x in first:
                i = self.nonterms.index(l_gram)
                j = self.terms.index(x)
                if self.pa_table[i][j] != None:
                    print("[{}, {}] multi rules: {}, {}".format(i, j, self.pa_table[i][j], gram))
                else:
                    self.pa_table[i][j] = gram
            if is_nullable:
                for b in self.flparser.tab[l_gram]["FOLLOW"]:
                    i = self.nonterms.index(l_gram)
                    j = self.terms.index(b)
                    rule = "{} -> ε".format(l_gram,)
                    if self.pa_table[i][j] != None:
                        print("[{}, {}] multi rules: {}, {}".format(i, j, self.pa_table[i][j], rule))
                    else:
                        self.pa_table[i][j] = rule


    def print_pa_table(self):
        pt = prettytable.PrettyTable()
        field = ["NONTERM"]
        field.extend(self.terms)
        pt.field_names = field
        for index, nonterm in enumerate(self.nonterms):
            row = [nonterm]
            row.extend(self.pa_table[index])
            for i in range(len(row)):
                if row[i] == None:
                    row[i] = ""
            pt.add_row(row)
        print()
        print(pt)


grammars = [
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

grammars2 = [
    "S -> A a S",
    "S -> B b S",
    "S -> d",
    "A -> a",
    "B -> ",
    "B -> c",
]

parser = FirstFollowParser(grammars2)
PredictiveAnalyzer(parser)