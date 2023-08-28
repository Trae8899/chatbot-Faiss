from dotenv import load_dotenv
import openai
# PDF Loaders. If unstructured gives you a hard time, try PyPDFLoader
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import datetime
import json
import os
import glob
from uuid import uuid4
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS


OPENAI_API_KEY = None
MODEL = "text-embedding-ada-002"
try:
    load_dotenv()
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
except:
    pass

def textreader(filepaths:[],openai_api=OPENAI_API_KEY):
    openai.api_key = openai_api
    embeddings=OpenAIEmbeddings(openai_api_key=openai_api)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    texts=[]
    for filepath in filepaths:
        basename = os.path.basename(filepath)
        filenames=os.path.splitext(basename)
        ext=filenames[1]
        filename=filenames[0]
        if ext.upper()==".PDF":
            loader = PyPDFLoader(filepath)
        elif ext.upper()==".DOCX":
            loader = Docx2txtLoader(filepath)
        else:
            continue
        document = loader.load()
        text = text_splitter.split_documents(document)
        texts.extend(text)
        #metadata={'source': 'C:\\Users\\qkrwo\\Documents\\Digital\\chat_test\\Docs\\AWWA M45 3rd.pdf', 'page': 0}

    print (text)

def embedding_folder(filepaths:[],openai_api=OPENAI_API_KEY,resultpath=None):
    if resultpath==None:
        resultpath=os.path.dirname(filepaths[0])
    if os.path.exists(resultpath):
        pass
    else:
        return
    openai.api_key = openai_api
    embeddings=OpenAIEmbeddings(openai_api_key=openai_api)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    faissdbs=[]
    doc_list=[]
    for filepath in filepaths:
        basename = os.path.basename(filepath)
        filenames=os.path.splitext(basename)
        ext=filenames[1]
        filename=filenames[0]
        if ext.upper()==".PDF":
            loader = PyPDFLoader(filepath)
        elif ext.upper()==".DOCX":
            loader = Docx2txtLoader(filepath)
        else:
            continue
        document = loader.load()
        text = text_splitter.split_documents(document)

        #metadata={'source': 'C:\\Users\\qkrwo\\Documents\\Digital\\chat_test\\Docs\\AWWA M45 3rd.pdf', 'page': 0}
        faissdb = FAISS.from_documents(text, embeddings)
        faissdb.save_local(os.path.join(resultpath,f"{filename}_index"))
        doc_list.append(filename)
        if faissdbs==[]:
            faissdbs=faissdb
        else:
            faissdbs.merge_from(faissdb)
    faissdbs.save_local(os.path.join(resultpath,"faiss_index"))

    return doc_list