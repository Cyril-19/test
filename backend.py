from openai import OpenAI
import os
from dotenv import load_dotenv
# from web import create_chatbot
# from mat import get_assistant_response
load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Initialize OpenAI API key


def Tutors(question):

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are an answer generator for students and researchers. Your role is to analyze the provided {question} from the user and determine its type: logical or factual. After careful examination, provide the appropriate answer for the question.make sure that the answer is really readable and appeling to the user.if it is seem to be a question{question}which is logical or contains hard calculations, breakdown the question to make it understandable for the user with stepby step breakdown and correct explaination "},
        {"role": "user", "content": question},
        ]
        
    )
    # Extract the classification from the response
    classification = response.choices[0].message.content.strip().lower()
    return classification

# def handle_factual_query(question):
#     # Use the OpenAI API to determine the type of question
#     # question_type = identify_question_type(question)

#     if classification == "factual":
#         # Use the OpenAI agent to search the web and get the answer
#         answer = create_chatbot(question)
#         return answer
#     else:
#         answer = get_assistant_response(question)
#         # If the question is not factual, return an error message
#         return answer



