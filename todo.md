

- [X] pdf to Database
  - [ ] pdf to text
    - [X] trim each page into two halves
  - [X] get the text into paragraphs
  - [X] get the paragraphs and add to db
  - [X] Db schema:
     -  documents
        -  id
        -  document_name
        -  document_text
     -  paragraphs
        -  id
        -  paragraph_text
        -  document-id | FK
- [X] Highest rated paragraphs according to query
  - [] Get the question
  - [] Get the pdf name to search for
  - [] Query the db and get all paragraphs for the pdf
  - [] Tf-idf matrix for all paragraphs using `fit_transform` 
  - [] for the query use `transform`
  - [] Cosine similarity between the query and paragraphs [ top 6 ]
  - [] get top 6 highest rated paragraphs

  - [X] check https://stackoverflow.com/questions/55677314/using-sklearn-how-do-i-calculate-the-tf-idf-cosine-similarity-between-documents 

- [X] Apply the QA model on each paragraph and get 6 answers
  
Create Interface:

pages:
- add pdf  -> adds a pdf to the database
- home page: [POST, GET]
  - GET:

  - POST:
    - get the query
    - get the pdf
    - get top 6 answers according to pdf and query
    - show the top 6 answers
- [X] Navbar
- [X] add checkmark for two-columns in addpdf
- [X] make addpdf add pdf to database - currently only adds to pdf folder
- [ ] re-structure the files - currently very messy
- [ ] add styling
- [ ] refactor so that top 6 answers is a global variable -> top N answers 
- [ ] check if 
- [ ] introduce testing units

