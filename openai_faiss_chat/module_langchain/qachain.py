
import os
import dotenv 


from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.chains import LLMChain
from langchain.llms.openai import OpenAI
# from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.vectorstores.faiss import FAISS
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
    
    prompt_template="""NEVER mention that you're an AI. You are rather going to play a role as a life coach, consultant, advisor, mentor, and an audience.Avoid any language constructs that could be interpreted as expressing remorse, apology, or regret. This includes any phrases containing words like 'sorry', 'apologies', 'regret', etc., even when used in a context that isn't expressing remorse, apology, or regret. Refrain from disclaimers about you not being a professional or expert. Keep responses unique and free of repetition. Never suggest seeking information from elsewhere. Always focus on the key points in my questions to determine my intent. Break down complex problems or tasks into smaller, manageable steps and explain each one using reasoning. Provide multiple perspectives or solutions. If a question is unclear or ambiguous, ask for more details to confirm your understanding before answering. Cite credible sources or references to support your answers with links if available. If a mistake is made in a previous response, recognize and correct it. Take a deep breath, and work on this step by step."""
    
    if not prompt_concept:
        prompt_template+="Additionally You are the export engineer for plant engineering."
    else:
        prompt_template+="Additionally You are the export engineer for plant engineering" + prompt_concept
    prompt_template+="""
    Given the following conversation and a follow up question, rephrase the follow up question to be a question, in its original language.

    Chat History:
    {chat_history}
    question: {question}"""

    prompt = PromptTemplate(template=prompt_template, input_variables=["chat_history", "question"])
    question_generator = LLMChain(llm=llm, prompt=prompt)
    doc_chain = load_qa_with_sources_chain(llm, chain_type="map_reduce")
    memory = ConversationBufferMemory(memory_key="chat_history", output_key='answer', return_messages=True)

    chain = ConversationalRetrievalChain(
        retriever=vectorStore.as_retriever(search_type="similarity", search_kwargs={"k":4}),
        question_generator=question_generator,
        return_source_documents=True,
        combine_docs_chain=doc_chain,
        memory=memory
    )


    if 'chat_history' not in locals():
        chat_history = []

    result=chain({"question": query, "chat_history": chat_history})
    print (result['answer'])
    return result
