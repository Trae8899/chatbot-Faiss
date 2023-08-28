
import os
import dotenv 


from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.chains import LLMChain
from langchain.llms import OpenAI
# from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate


try:
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
except:
    pass

def ask_asme(query:str,faiss_path,chat_history=None,prompt_concept=None,openai_api=OPENAI_API_KEY,):
    if openai_api and faiss_path:
        pass
    else:
        return

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api)
    vectorStore = FAISS.load_local(faiss_path, embeddings)
    llm = OpenAI(temperature=0.3,openai_api_key=openai_api)
    
    prompt_template=""
    if prompt_concept:
        prompt_concept+="You are the engineer for plant engineering."
    prompt_template+="""
    Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:"""

    prompt = PromptTemplate(template=prompt_template, input_variables=["chat_history", "question"])
    question_generator = LLMChain(llm=llm, prompt=prompt)
    doc_chain = load_qa_with_sources_chain(llm, chain_type="map_reduce")
    memory = ConversationBufferMemory(memory_key="chat_history", output_key='answer', return_messages=True)

    chain = ConversationalRetrievalChain(
        retriever=vectorStore.as_retriever(search_type="similarity", search_kwargs={"k":2}),
        question_generator=question_generator,
        return_source_documents=True,
        combine_docs_chain=doc_chain,
        memory=memory
    )


    if 'chat_history' not in locals():
        chat_history = []
    query = query
    query += " in detail."

    result=chain({"question": query, "chat_history": chat_history})
    print (result['answer'])
    return result
