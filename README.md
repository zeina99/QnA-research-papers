# QnA-research-papers

## About
A Question Answering Web application that takes in a question from a user and returns the top 6 answers according to the question.
It uses a pretrained BERT QA model to perform extractive question answering on text.
## Installation
1. clone the repo by running: `git clone https://github.com/zeina99/QnA-research-papers.git` 
2. cd into the directory into the cloned repo
3. to install the requirements:
   1. make sure python is installed
   2.  ```pip install -r requirements.txt``` 
   
        OR 
        ```
        pip install transformers flask torch scikit-learn numpy pdfplumber
        ```

4. run the app:
   
   ```python app.py```

## How it works:
Adding a pdf file:

PDF -> text extraction -> document ,paragraphs -> DB

Asking a question:

Question, pdf chosen -> top 6 paragraphs -> top 6 answers

### 1. Pdf to database
- when pdf gets added
  - text is extracted from the pdf
  - text is added to the database
  - the text is iterated over and gets divided into paragraphs. a paragraph is set to have a max of 250 words
  - list of paragraphs get added to database along with docuemnt-id they belong to
### 2. Ask a question 
- When the desired pdf is selected and the question is entered, cosine-similarity is applied on all paragaraphs according to the pdf selected and the top 6 paragraphs that could hold the answer are returned.
- pretrained BERT QA model on 6 paragraphs
  - the pretrained BERT QA model is applied on all 6 paragraphs so we end up with 6 possible answers.

## Technologies used:
- Pretrained question answering bert model 
- sqlite db
- pdfplumber
## Difficulties faced:
- pretrained BERT QA model doesnt work well on large amounts of text:
  - solution:
  - break down research papers into paragraphs and add them to the database
  - get the top 6 most similar paragraphs against the user query using cosine similarity
  - apply the pretrained BERT QA model on the top 6 paragraphs which results in 6 possible answers
- pdf plumber reads text from left to right, top to bottom and research papers have 2 columns of text
  - solution:
  - crop each page into two halves, extract text from left half then right half and combine them
  
### Future improvements:
- find a way to ignore subscripts when extracting text from pdfs as it is causing problems
- divide paragraphs as present in pdf document, instead of a fixed word count
- implement a login system where each user can view their own pdfs


## Screenshots

1. Adding a pdf: 
![Adding a new pdf to the database](screenshots/addpdf.png)

2. Preparing a question to ask related to the pdf content: 

- Question: What is the most competitive neural sequence transduction models have? 
- Answer: an encoder-decoder structure
![Preparing a question to ask related to the pdf content](screenshots/pdfquestion.jpg)

3. Getting top 6 answers according to the question. 
![Getting top 6 answers according to the question](screenshots/QAdemo.jpg)
