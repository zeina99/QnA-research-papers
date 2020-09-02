
from sqlite3.dbapi2 import Cursor
from haystack import Finder
from text import textt
from haystack.indexing.utils import convert_files_to_dicts, fetch_archive_from_http

from haystack.reader.transformers import TransformersReader
from haystack.utils import print_answers
from haystack.retriever.sparse import TfidfRetriever
from haystack.retriever.dense import DensePassageRetriever
import sqlite3
import re
# import os
# from subprocess import Popen, PIPE, STDOUT
# es_server = Popen(['elasticsearch-7.6.2/bin/elasticsearch'],
#                    stdout=PIPE, stderr=STDOUT,
#                    #preexec_fn=lambda: os.setuid(1),  # as daemon
#                   )

# connection
# connection = sqlite3.connect('qa.db')

# cursor = connection.cursor()

# cursor.execute("SELECT text from document")

# res = cursor.fetchall()
# for result in res:
#     result = re.sub(r"\\n","",str(result))
#     print(result)
# #print(res[2])

# connection.close()

from haystack.database.sql import SQLDocumentStore
document_store = SQLDocumentStore(url="sqlite:///qa.db")


doc_dir = 'data'
# from haystack.database.elasticsearch import ElasticsearchDocumentStore
# document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")

dicts = convert_files_to_dicts(dir_path=doc_dir)
document_store.write_documents(dicts)
# RETRIEVERS
# 1

# from haystack.retriever.sparse import ElasticsearchRetriever
# retriever = ElasticsearchRetriever(document_store=document_store)
# 2
retriever = DensePassageRetriever(document_store=document_store,
                                  embedding_model="dpr-bert-base-nq",
                                  do_lower_case=True, use_gpu=True)

retriever.retrieve(query="Why did the revenue increase?")


reader = TransformersReader(model="bert-large-uncased-whole-word-masking-finetuned-squad", tokenizer="bert-large-uncased-whole-word-masking-finetuned-squad",use_gpu=-1)


finder = Finder(reader, retriever)

prediction = finder.get_answers(question="What is an attention function?", top_k_retriever=10, top_k_reader=5)

print_answers(prediction, details="minimal")