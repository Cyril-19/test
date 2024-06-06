from openai import OpenAI
import openai
import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferMemory
from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain_community.callbacks.manager import get_openai_callback
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent,create_react_agent, create_openai_functions_agent
from langchain.prompts import PromptTemplate
from langchain.agents.agent_types import AgentType
from langchain.chains import LLMMathChain, LLMChain
from langchain.chains import LLMMathChain
from langchain_community.llms import OpenAI

load_dotenv()
openai.api_key =os.getenv("OPENAI_API_KEY")


# Initialize OpenAI API key


def Tutors(question):

    response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an assistant. Answer the following question as best as you can.you should expect multiple choice questions,and even many questions as single input.so anlyse the question carefully and answer accordingly"},
        {"role": "user", "content": question}
        ]
        
    )
    # Extract the classification from the response
    classification = response.choices[0].message.content.strip().lower()
    return classification

# Function to perform web search using an agent
def create_chatbot(question):
   
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    chat_template = """
    Your job is to give answer to the {user_input} you are getting.you are a knwoledge source .
    Use web search if required after anlaysing the {user_input}. you can expect muliple choice questions and  many questions in a single input{user_input}.so analyse the questions carefully and answer it accordingly.Be as detailed as possible, but don't make up any information that's not correct.dont halucinate.be specific.give the answers without any error .

   """
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True,output_key="output",prompt_template=chat_template)
    
    llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=openai.api_key, streaming=False)
    tools = [DuckDuckGoSearchRun(name="Search")]
    chat_agent = ConversationalChatAgent.from_llm_and_tools(llm=llm, tools=tools)
    
    executor = AgentExecutor.from_agent_and_tools(
        agent=chat_agent,
        tools=tools,
        memory=memory,
        return_intermediate_steps=False,
        handle_parsing_errors=True,
    )
    
    with get_openai_callback() as cb:
        response = executor.invoke(question)
        total_tokens = cb.total_tokens
        print(f"Total cost: {(total_tokens/1000)*.002}")
   
    
    return response["output"]

def classify_need_for_web_search(question):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant. Determine if the following question requires a web search to find the answer. Reply with 'web search' or 'no web search'."},
            {"role": "user", "content": question}
        ]
    )
    response
    return response.choices[0].message.content.strip().lower()

# Main solver function
def main_solver(question):
    classification = classify_need_for_web_search(question)
    if classification == "web search":
        return create_chatbot(question)
    else:
        return Tutors(question)

# Example Usage
question = "Who won the Best film in can film festival in  2024 from inida?"
print(main_solver(question))
