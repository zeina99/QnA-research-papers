
from flask import Flask , render_template,flash, request, redirect, url_for
import os

from werkzeug.utils import secure_filename
from qaanswering import get_paragraphs_from_pdf_name,TfIdfVector,get_six_answers
from extract_pdf_to_db import pdf_to_db
import sqlite3

UPLOAD_FOLDER = 'pdfs'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
# file upload code from:
# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(16)

PDF_DIRECTORY = 'pdfs'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/",methods = ['POST','GET'])
def home():
    all_pdfs = os.listdir(PDF_DIRECTORY)
    
    if request.method == "GET":
        return render_template("index.html",pdfs = all_pdfs)

    if request.method == "POST":
        query =request.form.get('question')
        pdf_name = request.form.get('pdfs')
        print("pdfname: ",pdf_name)
        answers = get_ans(query=query,pdfname=pdf_name)
        return render_template("index.html", answers = answers, pdfs = all_pdfs, question = query)

@app.route('/addpdf', methods=['GET', 'POST'])
def addpdf():
    if request.method == 'POST':
        
        # check if the post request has the file part
        if 'pdffile' not in request.files:
            flash('No file part')
            
            return redirect(request.url)
        file = request.files['pdffile']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file','error')
            
            return redirect(request.url)
        # make sure file is in allowed file extensions and file does not already exist
        if file and allowed_file(file.filename) and not check_if_pdf_exists(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            two_columns_val = request.form.get('twocolumns')
            
            #has_two_columns = None
            if two_columns_val:
                has_two_columns = True
            else:
                has_two_columns = False
            
            pdf_to_db(os.path.join(UPLOAD_FOLDER,file.filename),two_columns_in_page = has_two_columns)
            flash('file added','success')
            return redirect('/')
        else:
            flash('file extension not supported or file already exists','error')
            return redirect(request.url)
    else:
        return render_template("addpdf.html")

def check_if_pdf_exists(filename):
    # list all pdfs available in the pdf directory
    pdfs_saved = os.listdir(PDF_DIRECTORY)

    if filename in pdfs_saved:
        return True
    return False

def get_ans(pdfname,query):
    paragraphs = get_paragraphs_from_pdf_name(pdfname)

    tfidf_vector = TfIdfVector(paragraphs)
    tfidf_vector.fit_transform()
    similarity_scores = tfidf_vector.get_sorted_similarity(query)
    paragraphs_most_sim = tfidf_vector.top_6_paragraphs(similarity_scores)
    answers = get_six_answers(paragraphs_most_sim,query)
    return answers


if __name__ == "__main__":
    app.run(debug=True)