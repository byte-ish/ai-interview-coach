# core/conversational_chain.py

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain


def create_conversational_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI interview coach."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
    memory = ConversationBufferMemory(return_messages=True)

    chain = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )

    return chain
