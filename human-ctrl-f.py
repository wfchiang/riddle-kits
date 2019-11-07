import os
import random 

# ====
# Globals 
# ====
CHARS = [] 
CHARS = CHARS + map((lambda x:chr(x)), range(ord('A'), ord('Z')+1))

QUIZS = []
QUIZS.append(['GOD', 'IS', 'LOVE'])

OCEAN_SIZE = 500

def randomlyCut (n_cuts, victim_list_len): 
    assert(type(n_cuts) is int)
    assert(type(victim_list_len) is int)
    assert(n_cuts >= 0)
    assert(n_cuts < victim_list_len)

    if (n_cuts == 0): 
        return victim_list[:]
    
    indexs = [] 
    while (len(indexs) < n_cuts): 
        this_id = random.choice(range(0, victim_list_len))
        if (this_id not in indexs): 
            indexs.append(this_id)
    
    indexs.sort()
    return indexs

def makeCharOcean (n_chars, this_quiz): 
    assert(type(n_chars) is int)
    assert(type(this_quiz) is list)
    assert(n_chars > 0)

    cocean = '' 
    for i in range(0, n_chars): 
        cocean += random.choice(CHARS) 
    
    cut_indexs = randomlyCut(len(this_quiz), len(cocean))

    final_string = ''
    prev_id = 0

    for i in range(0, len(this_quiz)):
        final_string = final_string + cocean[prev_id:cut_indexs[i]] + this_quiz[i]
        prev_id = cut_indexs[i]
    
    final_string = final_string + cocean[prev_id:]

    prev_id = -1

    for i in range(0, len(this_quiz)): 
        this_id = final_string.find(this_quiz[i])
        assert(this_id >= 0)
        assert(prev_id < this_id)
        prev_id = this_id

    return final_string

def getQuizString (this_quiz): 
    assert(type(this_quiz) is list)

    final_string = 'Keywords: '
    for i in range(0, len(this_quiz)): 
        final_string = final_string + this_quiz[i] + ' '
    
    return final_string.strip()

# ====
# Main 
# ====
if __name__ == '__main__': 
    for i in range(0, 1): 
        this_quiz = random.choice(QUIZS)
        quiz = makeCharOcean(OCEAN_SIZE, this_quiz)

        print (getQuizString(this_quiz))
        print ('')
        print (quiz)
        print ('')