from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os



# load the environment variables
load_dotenv()

# importing key form the environment
Api_key = os.getenv("Gemini-API-Key")

# Chatbot building
# System role to act as a python instructor

system_message = """
Act as an expert Python programming instructor. Your primary function is to assist users in learning and improving their Python skills. Adhere strictly to the following guidelines:


*   **Python Focus:** ONLY discuss topics directly related to Python programming. If a question is outside this scope, politely redirect the user back to Python. For example: "That's an interesting question, but let's focus on Python. What Python-related questions do you have?"
*   **Explanations:** Provide clear, concise, and accurate explanations of Python concepts. Use examples and code snippets to illustrate your points.
*   **Code Quality:** When providing code, ensure it is functional, well-commented, and follows Python best practices. Avoid outdated or insecure code.
*   **Exercises:** Whenever appropriate, suggest exercises or small projects to reinforce learning.
*   **Tone:** Maintain a friendly, encouraging, and patient tone, as if you are teaching a student.
*   **No General Knowledge:** Do not answer general knowledge questions or engage in discussions unrelated to Python.
*   ** Always end the conversation by asking if the user has any more questions or wishes to exit. For example: "Do you wish to ask me anything more or leave by typing 'exit'?"
*   **Exit Command:** If the user types "exit," end the conversation by saying (OK!,Good bye and take care!).


Under no circumstances should you deviate from these guidelines.



"""

# creating an instance of the GoogleGenerativeAI

llm_response = GoogleGenerativeAI(model="gemini-1.5-flash",
                                  api_key= Api_key,
                                  messages=[{"role": "system", "content": system_message}],
                                  temperature = 0.0)




# variable to store the conversation history
conversation_history = []
    
# function to check if the user input is python related

def get_llm_response(user_input):
    prompt = f"{system_message}\n\nUser: {user_input}\nAssistant:"
    try:
        gemini_response = llm_response.invoke(prompt)
        return gemini_response
    except Exception as e:    
        print(f"LLM invocation error: {e}")
        return {"type": "error", "content": f"An error occurred: {e}"}
    
# main function to run the chatbot

def main():
    while True:
        user_input = input("Bot: Hello! What Python question do you have? (or type 'exit'):\n You: ")
        if user_input.lower() == "exit":
            break
        try:
            response = get_llm_response(user_input)
            chat_history = str(response)
            print("Bot:",response)
            conversation_history.append({"role":"bot","response":chat_history})
            # creating a file for chat history on local machine
            f = open("conversation_history_file.txt",'w')
            f.writelines(chat_history)
            f.close()
        except Exception as e:
            print(f"Error:{e}")
            print (" Sorry, I encountered an error:{e}.")
        continue
            # prompt = get_llm_response(input("What Python question do you have? (or type 'exit')\n You: "))
            # print(prompt)
           

if __name__ == "__main__":
    main()

