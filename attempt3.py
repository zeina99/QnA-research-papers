from torch import topk
from transformers import pipeline
nlp = pipeline("question-answering")
from text import textt
text = open("data/paper1.txt","r")


context = text.read()

result = nlp(question="What was it trained on?", context=textt)
print(f"Answer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}")

result = nlp(question="What is the transformer based on?", context=textt, topk=10)
print(f"Answer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}")