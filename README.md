# QnA-research-papers

## About
A Question Answering program that takes in a question from a user and returns the top 6 answers according to the question

## How it works:
---
### pdf to database
- when pdf gets added
  - text is extracted from the pdf
  - text is added to the database
  - the text is iterated over and gets divided into paragraphs. a paragraph is set to have a max of 250 words
  - list of paragraphs get added to database along with docuemnt-id they belong to
### Ask a question 
- When the desired pdf is selected and the question is entered, cosine-similarity is applied on all paragaraphs according to the pdf selected and the top 6 paragraphs that could hold the answer are returned.
- QA model on 6 paragraphs
  - the QA model is applied on all 6 paragraphs so we end up with 6 possible answers.

## Technologies used:
- QA model from hugging face
- sqlite db
- pdfplumber
## Difficulties faced:
- QA model doesnt work well on large amounts of text:
  - solution:
  - break down research papers into paragraphs and add them to the database
  - get the top 6 most similar paragraphs against the user query using cosine similarity
  - apply the QA model on the top 6 paragraphs which results in 6 possible answers
- pdf plumber reads text from left to right, top to bottom and research papers have 2 columns of text
  - solution:
  - crop each page into two halves, extract text from left half then right half and combine them
  
### Future improvements:
- find a way to ignore subscripts when extracting text from pdfs as it is causing problems
- implement a login system