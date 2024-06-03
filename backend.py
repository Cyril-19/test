from openai import OpenAI
import os
from dotenv import load_dotenv
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Initialize OpenAI API key


def identify_question_type(question):

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are an answer generator for students and researchers. Your role is to analyze the provided {question} from the user and determine its type: logical or factual. After careful examination, provide the appropriate classification in one word.If there are more than one question {question}in the input ,analyse and clasisify each seperately."},
        {"role": "user", "content": question},]
        
    )
    # Extract the classification from the response
    classification = response.choices[0].message.content.strip().lower()
    return classification
def handle_factual_query(question):
    # Use the OpenAI API to determine the type of question
    question_type = identify_question_type(question)

    if question_type == "factual":
        # Use the OpenAI agent to search the web and get the answer
        answer = search_web(question)
        return answer
    else:
        # If the question is not factual, return an error message
        return "I'm sorry, I couldn't find the answer to that question."

# Example usage
question = "define the process of digestion in human body"

question_type = identify_question_type(question)
print(f"Question: {question}")
print( question_type)

