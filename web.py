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
openai_api_key=os.getenv("OPEN_AI_KEY")


def create_chatbot(question):
   
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    chat_template = """
    Your job is to give answer to the {user_input} youu are getting.you are a knwoledge source .
    Use web search if required after anlaysing the {user_input}. Be as detailed as possible, but don't make up any information that's not correct.dont halucinate.be specific.

   """
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True,output_key="output",prompt_template=chat_template)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=False)
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
   
    
    return response




