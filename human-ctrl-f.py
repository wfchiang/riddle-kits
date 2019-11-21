import os
import random 

# ====
# Globals 
# ====
CHARS = [] 
CHARS = CHARS + map((lambda x:chr(x)), range(ord('A'), ord('Z')+1))

QUIZS = []
QUIZS.append(['GOD', 'IS', 'LOVE'])
QUIZS.append(['FATHER', 'SON', 'SPIRIT'])
QUIZS.append(['JESUS', 'GOOD', 'SHEPHERD'])
QUIZS.append(['LAMB', 'OF', 'GOD'])
QUIZS.append(['BY', 'GRACE', 'THROUGH', 'FAITH'])

OCEAN_WIDTH  = 75 
OCEAN_HEIGHT = 15

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

def makeCharOcean (): 
    cocean = []

    for r in range(0, OCEAN_HEIGHT): 
        ocean_row = ''
        for w in range(0, OCEAN_WIDTH): 
            ocean_row += random.choice(CHARS)
        cocean.append(ocean_row)

    return cocean 

def hideTreeIntoForest (forest, tree): 
    assert(type(forest) is str)
    assert(type(tree) is str)

    assert(len(forest) >= len(tree))
    assert(len(tree) > 0)

    starting_index = random.choice(range(0, (len(forest)-len(tree)+1)))

    return forest[0:starting_index] + tree + forest[starting_index+len(tree):]

def hideQuizIntoOcean (cocean=[], quiz=[]): 
    assert(len(cocean) >= len(quiz))
    assert(len(quiz) > 0)

    candidate_row_indices = []
    while (len(candidate_row_indices) < len(quiz)): 
        this_index = random.choice(range(0, len(cocean)))
        if (this_index not in candidate_row_indices): 
            candidate_row_indices.append(this_index)
    candidate_row_indices.sort()

    for i in range(0, len(candidate_row_indices)):
        forest_index = candidate_row_indices[i]
        cocean[forest_index] = hideTreeIntoForest(cocean[forest_index], quiz[i])

    return cocean

def validate (cocean, quiz): 
    row_index = 0
    for q in quiz:
        while (True): 
            if (q in cocean[row_index]): 
                row_index += 1
                break
            else: 
                row_index += 1
                if (row_index >= len(cocean)): 
                    return False
    return True 

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
    for i in range(0, 10): 
        this_quiz = random.choice(QUIZS)
        cocean = hideQuizIntoOcean(makeCharOcean(), this_quiz)

        assert(validate(cocean, this_quiz))

        print (getQuizString(this_quiz))
        print ('')
        for r in cocean: 
            print (r)
        print ('')
        print ('')
        print ('')