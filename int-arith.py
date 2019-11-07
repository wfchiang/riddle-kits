import sys
import os 
import random

# ====
# Globals 
# ====
OPTS = ['+', '-', '*', '/']
MAX_INT = 10 
N_QUIZS = 5 
QUIZ_LENGTHS = [20] 

dump_file = open('dump_file', 'w')

# ====
# Class
# ====
class Clause (object): 
    opt = None 
    lhs = None 
    rhs = None 

    def __init__ (self, opt, lhs, rhs): 
        self.opt = opt
        self.lhs = lhs
        self.rhs = rhs

    def isInt (self): 
        return (self.opt is None) and (type(self.lhs) is int) and (self.rhs is None)

    def isComposite (self): 
        return (self.opt in OPTS) and isinstance(self.lhs, Clause) and isinstance(self.rhs, Clause)
    
    def isValid (self): 
        return self.isInt() or self.isComposite() 

    def eval (self): 
        if (self.isInt()): 
            return float(self.lhs)
        elif (self.isComposite()): 
            if (self.opt == '+'): 
                return float(self.lhs.eval()) + float(self.rhs.eval())
            elif (self.opt == '-'):
                return float(self.lhs.eval()) - float(self.rhs.eval())
            elif (self.opt == '*'):
                return float(self.lhs.eval()) * float(self.rhs.eval()) 
            elif (self.opt == '/'): 
                return float(self.lhs.eval()) / float(self.rhs.eval()) 
            else: 
                assert(False), "Invalid operator"
        else: 
            assert(False), "Invalid Clause"

    def clone (self): 
        opt = None 
        if (self.opt is not None): 
            opt = self.opt 
        lhs = None 
        if (self.lhs is not None): 
            if (type(self.lhs) is int): 
                lhs = self.lhs
            else: 
                lhs = self.lhs.clone() 
        rhs = None 
        if (self.rhs is not None): 
            if (type(self.rhs) is int): 
                rhs = self.rhs 
            else: 
                rhs = self.rhs.clone()
        return Clause(opt, lhs, rhs)

    def refine (self):
        if (self.isInt()): 
            return self.clone() 

        new_opt = self.opt 
        new_lhs = self.lhs.refine() 
        new_rhs = self.rhs.refine()

        new_me = Clause(new_opt, new_lhs, new_rhs) 

        if (self.opt in ['+', '-', '*']): 
            return Clause(new_opt, new_lhs, new_rhs)

        elif (self.opt == '/'):
            if (new_me.isGood()): 
                return new_me 
            candidates = range(1, MAX_INT+1)
            random.shuffle(candidates)
            for c in candidates: 
                new_me.rhs = Clause(None, c, None) 
                if (new_me.isGood()): 
                    return new_me
            assert(False), 'Failed to refine division...' 
        else: 
            assert(False), 'Invalid operator'

    def isGood (self): 
        eval_result = self.eval()
        return eval_result == int(eval_result)

    def __str__ (self): 
        if (self.isInt()): 
            return str(self.lhs)
        elif (self.isComposite()): 
            return str(self.lhs) + self.opt + str(self.rhs)
    
    def dump (self): 
        if (self.isInt()): 
            return str(self.lhs)
        elif (self.isComposite()): 
            return '(' + str(self.lhs) + self.opt + str(self.rhs) + ')'

# ====
# Routines
# ====
def parseStringToClause (string_clause): 
    assert(type(string_clause) is str)

    for opt in OPTS: 
        string_clause = string_clause.replace(opt, ' '+opt+' ')
    
    literals = list(filter((lambda x: len(x.strip())>0), string_clause.split(' ')))
    assert((len(literals)-1) % 2 == 0)

    lhs = Clause(None, int(literals[0]), None) 
    i_curr = 1

    plus_minus_list = []  

    while (i_curr < len(literals)): 
        opt = literals[i_curr]
        rhs = Clause(None, int(literals[i_curr+1]), None)
        i_curr += 2

        if (opt in ['+', '-']): 
            plus_minus_list.append(lhs)
            plus_minus_list.append(opt)
            lhs = rhs
        else: 
            lhs = Clause(opt, lhs, rhs) 
        
    plus_minus_list.append(lhs) 
    i_curr = 1
    assert((len(plus_minus_list)-1) % 2 == 0)

    lhs = plus_minus_list[0]

    while (i_curr < len(plus_minus_list)): 
        opt = plus_minus_list[i_curr]
        rhs = plus_minus_list[i_curr+1]
        i_curr += 2

        lhs = Clause(opt, lhs, rhs) 

    return lhs

def createRandomQuiz (n_ints): 
    assert(type(n_ints) is int)
    assert(n_ints >= 1)

    quiz = str(random.randint(1, MAX_INT))

    for i in range(1, n_ints): 
        quiz += random.choice(OPTS) + str(random.randint(1, MAX_INT))
    
    return quiz 

def createRefinedRandomQuiz (n_ints): 
    assert(type(n_ints) is int)
    assert(n_ints >= 1)

    random_quiz = createRandomQuiz(n_ints)
    random_clause = parseStringToClause(random_quiz)
    
    refined_random_clause = random_clause.refine()
    return str(refined_random_clause)

def beautifyQuiz (string_quiz): 
    string_quiz = string_quiz.replace('+', ' + ')
    string_quiz = string_quiz.replace('-', ' - ')
    string_quiz = string_quiz.replace('*', ' x ')
    string_quiz = string_quiz.replace('/', ' / ')
    string_quiz = string_quiz.replace('/', '\xc3\xb7')
    return string_quiz

# ====
# Main
# ====
if __name__ == '__main__': 
    quiz_answer_set = [] 
    
    for id_quiz in range(1, N_QUIZS+1): 
        refined_random_quiz = createRefinedRandomQuiz( random.choice(QUIZ_LENGTHS) )
        quiz_clause = parseStringToClause(refined_random_quiz)
        assert(quiz_clause.isGood())
        quiz_answer = quiz_clause.eval()
        assert(int(quiz_answer) == quiz_answer)
        quiz_answer_set.append([int(quiz_answer), str(quiz_clause)])

    print ('Questions')
    for i in range(0, len(quiz_answer_set)):
        print ('')
        print ('(' + str(i+1) + ') ' + beautifyQuiz(quiz_answer_set[i][1]))

    print ('')

    print ('Answers')
    for i in range(0, len(quiz_answer_set)):
        print ('')
        print ('(' + str(i+1) + ') ' + str(quiz_answer_set[i][0]))

    dump_file.close()