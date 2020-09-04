
import sqlite3
from numpy.lib.function_base import vectorize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering


tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")



# QUERY = 'What is language modeling usually framed as?'

# PDF_NAME = "language-models.pdf"

def get_paragraphs_from_pdf_name(pdf_name):
    with sqlite3.connect('qa.db') as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT id from documents WHERE document_name = :document_name",(pdf_name,))
        
        try:
            document_id = cursor.fetchone()[0]
        except Exception as e:
            raise e 
            

        cursor.execute("SELECT paragraph_text from paragraphs WHERE document_id = :document_id",{"document_id":document_id})
        paragraphs = cursor.fetchall()
        #since paragraphs is a list of tuples, 
        paragraphs_list = []
        for paragraph in paragraphs:
            paragraphs_list.append(paragraph[0])
        
    connection.close()
    return paragraphs_list

# paragraphs = get_paragraphs_from_pdf_name(pdf_name==PDF_NAME)

class TfIdfVector():
    def __init__(self,paragraphs):
        #paragraphs: 1d array that has all paragraphs in a pdf document

        self.vector = TfidfVectorizer()
        self.paragraphs = paragraphs
    
    def fit_transform(self):
        
        self.tfidf_docs = self.vector.fit_transform(self.paragraphs)
        return self.tfidf_docs

    def get_sorted_similarity(self, query):
        query_tfidf = self.vector.transform([query])
        # print(query_tfidf)
        cosineSimilarities = cosine_similarity(query_tfidf, self.tfidf_docs, dense_output=True)
        # ex:  [[0.0344344  0.04934151 0.05119006 0.16013789 0.10203791 0.10613493
        #   0.05569845 0.1477758  0.05020448 0.12808981 0.11151897 0.07922314
        #   0.11449221 0.02382642 0.05825266 0.05613239 0.03143356 0.06109101
        #   0.00460069 0.03276561]]
        #sorting from smallest to largest according to cosineSimilarities indices

        # sorted by index -> [[18 13 16 19  0  1  8  2  6 15 14 17 11  4  5 10 12  9  7  3]] 
        return cosineSimilarities.argsort() 

    def top_6_paragraphs(self,similarities):
        '''
        returns top 6 similar paragraphs.
        if similarities are less than 6, return all
        else return top 6
        ---------------
        similarities: 2d array returned from get_sorted_similarity() that represents similarity scores sorted by indices from smallest to largest
        
        '''
        top_6_paragraphs = []
        if len(similarities[0]) <= 6:
            sorted_indices = similarities
        else:
            #get the last six elements and reverese elements to have them from largest to smallest
            sorted_arr = similarities[0][-6:]
            sorted_indices = sorted_arr[::-1]
        # get the paragraph by index from the top 6 sorted indices 
        for index in range(len(sorted_indices)):
            top_6_paragraphs.append(self.paragraphs[index])
        
        return top_6_paragraphs


# tfidf_vector = TfIdfVector(paragraphs)
# tfidf_vector.fit_transform()
# sim = tfidf_vector.get_sorted_similarity(QUERY)


# paragraphs_most_sim = tfidf_vector.top_6_paragraphs(sim)


def get_six_answers(top_6_paragraphs,query):
    # list to hold all 6 question and answers
    question_answers = []

    for paragraph in top_6_paragraphs:
        inputs = tokenizer(query, paragraph, add_special_tokens=True, return_tensors="pt")
        input_ids = inputs["input_ids"].tolist()[0]
        
        text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
        answer_start_scores, answer_end_scores = model(**inputs)
        answer_start = torch.argmax(
            answer_start_scores
        )  # Get the most likely beginning of answer with the argmax of the score
        answer_end = torch.argmax(answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
        # print(f"Question: {QUERY}")
        # print(f"Answer: {answer}")
        question_answers.append(
            {"question" : query,
            "answer" : answer}
        )
    return question_answers



# questions:  
# What is language modeling usually framed as?