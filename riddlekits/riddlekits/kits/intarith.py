import sys
import os 
import random

# ====
# Globals 
# ====
OPTS = ['+', '-', '*', '/']

# ====
# Class
# ====
class QuizResponse (object): 
    str_question = None 
    str_answer   = None 

    def __init__ (self, quiz_clause): 
        assert(isinstance(quiz_clause, Clause))
        assert(quiz_clause.isGood())
        self.str_question = self.beautifyQuizString(str(quiz_clause))
        self.str_answer = str(int(quiz_clause.eval()))

    def beautifyQuizString (self, string_quiz): 
        string_quiz = string_quiz.replace('+', ' + ')
        string_quiz = string_quiz.replace('-', ' - ')
        string_quiz = string_quiz.replace('*', ' x ')
        string_quiz = string_quiz.replace('/', ' / ')
        string_quiz = string_quiz.replace('/', '\xc3\xb7')
        return string_quiz
    
    def __str__ (self): 
        return '{ \"str_question\": \"' + self.str_question + '\", \"str_answer\": \"' + self.str_answer + '\"}'
        
class QuizRequest (object): 
    max_int = 10
    quiz_length = 20 

    def parseStringToClause (self, string_clause): 
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

    def createRandomQuiz (self): 
        assert(type(self.max_int) is int and self.max_int > 0), "Invalid self.max_int: "+str(self.max_int)
        assert(type(self.quiz_length) is int and self.quiz_length > 0), "Invalid self.quiz_length: "+str(self.quiz_length)

        str_quiz = str(random.randint(1, self.max_int))
        for i in range(1, self.quiz_length): 
            str_quiz += random.choice(OPTS) + str(random.randint(1, self.max_int))

        clause = self.parseStringToClause(str_quiz).refine(self.max_int)
        assert(clause.isGood())

        return clause

    def __init__ (self, max_int = None, quiz_length = None): 
        if (type(max_int) is int): 
            self.max_int = max_int
        if (type(quiz_length) is int): 
            self.quiz_length = quiz_length

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

    def refine (self, max_int):
        assert(type(max_int) is int and max_int > 0), "Invalid max_int: "+str(max_int)
        if (self.isInt()): 
            return self.clone() 

        new_opt = self.opt 
        new_lhs = self.lhs.refine(max_int) 
        new_rhs = self.rhs.refine(max_int)

        new_me = Clause(new_opt, new_lhs, new_rhs) 

        if (self.opt in ['+', '-', '*']): 
            return Clause(new_opt, new_lhs, new_rhs)

        elif (self.opt == '/'):
            if (new_me.isGood()): 
                return new_me 
            candidates = list(range(1, max_int+1))
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
# Main
# ====
if __name__ == '__main__': 
    quiz_request = QuizRequest(max_int = 10, quiz_length = 5)
    quiz_response = QuizResponse(quiz_request.createRandomQuiz())
    print ('>question: ' + quiz_response.str_question)
    print ('>answer: ' + quiz_response.str_answer)