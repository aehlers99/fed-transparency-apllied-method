from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.indexes.vectorstore import VectorstoreIndexCreator, VectorStoreIndexWrapper
from langchain.document_loaders import DirectoryLoader, TextLoader, PyPDFium2Loader
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

import openai
import os
import constants
import query as qr
import fedscrap as fs
import numpy as np
import pandas as pd

os.environ["OPENAI_API_KEY"] = constants.APIKEY

labels = fs.label_list

data_values = pd.DataFrame(index = np.arange(0,15))

for label in labels[31:41]:

    loader = PyPDFium2Loader(label)

    embeddings = OpenAIEmbeddings()

    vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())

    index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
      llm=ChatOpenAI(model="gpt-3.5-turbo"),
      retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )

    chat_history = []

    list_ofQuestions = list(qr.queries.values())

    answers = []

    for i in range(len(list_ofQuestions)):
        query = str(list_ofQuestions[i])
        result = chain({"question" : query, 'chat_history' : chat_history})
        answers.append(result['answer'])
        print(f'{i} ) {label} concluded')
    data_values[label] = answers

data_values.to_csv('data_values5.csv', index=True, header = True, encoding='utf-8-sig', sep = ';')


