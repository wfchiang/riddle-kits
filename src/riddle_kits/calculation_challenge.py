import click 
from typing import List, Union
import random 


# ====
# Globals
# ====
OPTS = {
    '+': (lambda x,y: (x+y)), 
    '-': (lambda x,y: (x-y)), 
    'x': (lambda x,y: (x*y)), 
    '/': (lambda x,y: int(x/y))
}

RANGE = 200


# ====
# Utils 
# ====
def get_randint (): 
    return random.randint(1, 9)

def _eval_add_sub (quiz :List[Union[str, int]]): 
    assert(len(quiz) > 0)

    if (len(quiz) == 1): 
        assert(type(quiz[0]) is int) 
        return quiz 

    assert(len(quiz) != 2)

    lhs = quiz[0]
    opt = quiz[1]
    rhs = quiz[2] 

    assert(type(lhs) is int)
    assert(type(opt) is str and opt in ['+', '-'])
    assert(type(rhs) is int)

    quiz = [OPTS[opt](lhs, rhs)] + quiz[3:]
    
    return _eval_add_sub(quiz)

def _eval_mul_div (quiz :List[Union[str, int]]): 
    assert(len(quiz) > 0)

    if (len(quiz) == 1): 
        assert(type(quiz[0]) is int)
        return quiz

    assert(len(quiz) != 2)

    lhs = quiz[0]
    opt = quiz[1]
    rhs = quiz[2] 

    assert(type(lhs) is int)
    assert(type(opt) is str and opt in OPTS)
    assert(type(rhs) is int)

    if (opt in ['+', '-']): 
        head = [lhs, opt]
        tail = _eval_mul_div(quiz[2:])
        if (tail is None): 
            return None 
        return head + tail 

    elif (opt == 'x'): 
        quiz = [OPTS['x'](lhs, rhs)] + quiz[3:]
        return _eval_mul_div(quiz)

    elif (opt == '/'): 
        if (lhs % rhs != 0): 
            return None 
        quiz = [OPTS['/'](lhs, rhs)] + quiz[3:]
        return _eval_mul_div(quiz)

    else: 
        assert(False)

def eval (quiz :List[Union[str, int]]): 
    rel_mul_div = _eval_mul_div(quiz)
    return (None if (rel_mul_div is None) else _eval_add_sub(rel_mul_div))


def random_gen (head :List[Union[str, int]], n_numbers :int): 
    assert(n_numbers >= 0) 
    
    if (n_numbers == 0): 
        return head 

    if (len(head) == 0): 
        head = [get_randint()]
        return random_gen(head, (n_numbers-1))

    while (True): 
        opt = random.choice(list(OPTS.keys()))
        rhs = get_randint()
        rel = eval(head + [opt, rhs])

        if (rel is None): 
            continue

        assert(len(rel) == 1)
        rel = rel[0] 

        if (abs(rel) > RANGE): 
            continue 

        head = head + [opt, rhs]
        break 

    return random_gen(head, (n_numbers-1))
    

# ====
# Main 
# ====
@click.command() 
@click.argument('n_questions', type=int)
@click.argument('n_numbers', type=int)
def main (
    n_questions :int, 
    n_numbers :int 
): 
    questions = [] 
    answers = [] 

    for i in range(0, n_questions): 
        quiz = random_gen([], n_numbers)
        assert(quiz is not None)

        ans = eval(quiz)
        assert(type(ans) is list and len(ans) == 1)
        ans = ans[0]
        assert(type(ans) is int)

        questions.append(quiz)
        answers.append(ans)

    for i in range(0, n_questions): 
        quiz = list(map(lambda x: str(x), questions[i]))
        print('Challenge ({}):  '.format(i+1) + ' '.join(quiz))
        print('')
        print('')
        print('')
        print('')

    print('')

    for i in range(0, n_questions): 
        print('Answer ({}):  {}'.format(i+1, answers[i]))
        print('')


# ====
# Entry 
# ====
if __name__ == '__main__': 
    main() 