from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json 
from .kits.intarith import QuizRequest as intarithRequest
from .kits.intarith import QuizResponse as intarithResponse 

def home (http_request): 
    return render(http_request, 'index.html', {})

def intarith (http_request):
    json_reqt = json.loads(http_request.body)
    print ('> int-arith get request: ' + str(json_reqt))

    max_int = None 
    if ('max_int' in json_reqt.keys()):
        max_int = int(json_reqt['max_int'])
    quiz_length = None 
    if ('quiz_length' in json_reqt.keys()): 
        quiz_length = int(json_reqt['quiz_length'])

    quiz_reqt = intarithRequest(max_int=max_int, quiz_length=quiz_length)
    quiz_resp = intarithResponse(quiz_reqt.createRandomQuiz())
    print ('> int-arith response: ' + str(quiz_resp))
    
    return JsonResponse({
        "str_question": quiz_resp.str_question, 
        "str_answer": quiz_resp.str_answer})