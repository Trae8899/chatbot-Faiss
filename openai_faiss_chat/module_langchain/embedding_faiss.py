import dotenv 
import openai
# PDF Loaders. If unstructured gives you a hard time, try PyPDFLoader
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS



MODEL = "text-embedding-ada-002"
OPENAI_API_KEY = None
try:
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
except:
    pass

def textfile2faiss(filepath:str,openai_api=OPENAI_API_KEY,resultpath=None)->str: 
    if resultpath==None or resultpath=='':
        resultpath=os.path.dirname(filepath)
    if os.path.exists(resultpath):
        pass
    else:
        return
    embeddings=OpenAIEmbeddings(openai_api_key=openai_api)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    
    basename = os.path.basename(filepath)
    filenames=os.path.splitext(basename)
    ext=filenames[1]
    filename=filenames[0]
    if ext.upper()==".PDF":
        loader = PyPDFLoader(filepath)
    elif ext.upper()==".DOCX":
        loader = Docx2txtLoader(filepath)
    else:
        return
    document = loader.load()
    text = text_splitter.split_documents(document)
    faissdb = FAISS.from_documents(text, embeddings)
    resultfilepath=os.path.join(resultpath,f"{filename}_index")
    if os.path.exists(resultfilepath):
        pass
    else:
        pass
    faissdb.save_local(resultfilepath)
    return filename

def merge_faiss(faisspaths:[],openai_api=OPENAI_API_KEY,resultpath=None,name=None):
    embeddings=OpenAIEmbeddings(openai_api_key=openai_api)
    if name==None:
        name="faiss_index"    
    if resultpath==None:
        resultpath=os.path.dirname(faisspaths[0])

    faissdbs=[]
    for faisspath in faisspaths:
        try:
            faissdb = FAISS.load_local(faisspath,embeddings=embeddings)
            faissdbs.append(faissdb)
        except Exception as err:
            print (err)
            continue

    faissdb_index=None
    faissdb_index = faissdbs[0]
    for faissdb in faissdbs[1:]:
        faissdb_index.merge_from(faissdb)
    
    result_faiss_path = os.path.join(resultpath,name)
    os.makedirs(result_faiss_path, exist_ok=True)
    faissdb_index.save_local(result_faiss_path)
    
    return [result_faiss_path,faissdbs]