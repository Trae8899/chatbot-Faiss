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
import re



OPENAI_API_KEY = None
MODEL = "text-embedding-ada-002"
try:
    load_dotenv()
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
except:
    pass

def embedding_folder(filepaths:[],openai_api=OPENAI_API_KEY,resultpath=None):
    if resultpath==None:
        resultpath=os.path.dirname(filepaths[0])
    if os.path.exists(resultpath):
        pass
    else:
        os.makedirs(resultpath)
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
        
        faissdb = FAISS.from_documents(text, embeddings)
        change_filename=re.sub(r'[<>:"/\\|?*]', '_', filename)
        directory = os.path.join(resultpath,f"{change_filename}_index")
        # directory = r"C:/Users/qkrwo/Documents/Docs/manual"  # 슬래시 사용 또는 raw string
        if not os.path.exists(directory):
            os.makedirs(directory)
        try:
            faissdb.save_local(directory)
        except:
            continue
    
        doc_list.append(filename)
        
        if faissdbs==[]:
            faissdbs=faissdb
        else:
            faissdbs.merge_from(faissdb)
    resultpath=os.path.join(resultpath,"faiss_index")
    if os.path.exists(resultpath):
        try:
            faiss_old=FAISS.load_local(resultpath)
            faissdbs.merge_from(faiss_old)
        except:
            pass
    faissdbs.save_local(resultpath)
    return doc_list