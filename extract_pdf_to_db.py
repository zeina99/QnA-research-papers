import pdfplumber
import sqlite3
import os




def pdf_to_db(pdf_file_path, two_columns_in_page = False):

    file = pdfplumber.open(pdf_file_path)
    # to hold the text in the whole document
    full_text_in_document = ''
    num_of_words_per_paragraph = 250

    head, tail = os.path.split(pdf_file_path)

    for page in file.pages:
        if two_columns_in_page:
            # crop the page to get the left half
            left = page.crop((0, 0, 0.5*float(page.width), page.height) )
            # crop the page to right half
            right = page.crop((0.5*float(page.width),0, page.width, page.height))
            #get the text for left and right halves
            left_text = left.extract_text(x_tolerance=1, y_tolerance=1)
            right_text = right.extract_text(x_tolerance=1, y_tolerance=1)
            #combine both left and right texts to be one string
            full_text_in_page = left_text + right_text
            # add text in page to document string
            full_text_in_document += full_text_in_page
        else:
            full_text_in_page = page.extract_text(x_tolerance=1, y_tolerance=1)

            full_text_in_document += full_text_in_page

    paragraphs_list = document_to_paragraphs(full_text_in_document,num_of_words_per_paragraph)

    # adding document to db
    #check if document already exists
    with sqlite3.connect('qa.db') as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * from documents WHERE document_name = :document_name",{"document_name": tail})
        res = cursor.fetchall()
        # if the document name already exists, raise exception
        if len(res) != 0:
            raise Exception('Filename already exists in database')
        else:
            cursor.execute("INSERT into documents (document_name, document_text) VALUES (:document_name, :document_text)",{"document_name":tail,"document_text": full_text_in_document})
            cursor.execute("SELECT id from documents WHERE document_name = :document_name",{"document_name": tail})
            document_id = cursor.fetchone()[0]
        
        # adding paragraphs to db   
        for paragraph in paragraphs_list:
            cursor.execute("INSERT INTO paragraphs (paragraph_text, document_id) VALUES (:paragraph_text, :document_id)", {"paragraph_text":paragraph, "document_id":document_id})

    

 
    connection.close()
def document_to_paragraphs(document, num_of_words_per_paragraph): 
    # split document into words
    words = document.split()

    counter = 0
    paragraphs_list = []
    paragraph = ''
    for word in words:
    
        if counter <= num_of_words_per_paragraph:
            paragraph += word + " "
            counter += 1
        else:
            paragraphs_list.append(paragraph)
            counter = 0
            paragraph = ''
    return paragraphs_list
    

#7181-attention-is-all-you-need.pdf


# page = file.pages[1]
# x0: left-x of bounding box, measured from left side of page
# top: top-y of bounding box, measured from top of page
# x1: right-x of bounding box, measured from left side of page
# bottom: bottom-y of bounding box, measured from top of page
