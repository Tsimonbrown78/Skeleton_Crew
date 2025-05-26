import nltk
import re
from nltk.chat.util import Chat, reflections
import openai
from openai import OpenAI

# OpenAI API key
client = OpenAI(api_key='insert your key here')


#Responses for the chatbot to use when user prompts them
responses = [
    [r"hi|hello|hey", ["Hello! How can I help you today?", "Hi there! How may I assist you?"]],
    [r"my name is (.*)", ["Hello %1! How can I assist you today?"]],
    [r"(.*) your name?", ["I am your friendly chatbot!"]],
    [r"what (.*) want ?",["Make me an offer I can't refuse",]],
    [r"(.*) you can't solve ?",["That is a secret",]],
    [r"how (.*) today?",["You would know if you went outside.",]],
    [r"how (.*) health(.*)",["I'm a computer program, so I'm always healthy ",]],
    [r"how are you?", ["I'm just a bot, but I'm doing well. How about you?"]],
    [r"tell me a joke", ["Why don't skeletons fight each other? They don't have the guts!"]],
    [r"(.*) (help|assist) (.*)", ["Sure! How can I assist you with %3?"]],
    [r"bye|exit", ["Goodbye! Have a great day!", "See you later!"]],
    [r"(.*)", ["I'm sorry, I didn't understand that. Let me get another response from gpt bot."]]
    ]

#ChatGPT responses for those that are not already in regular chat
def gpt_responses(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful chatbot assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I had trouble reaching GPT. ({e})"

class RuleBasedChatbot:
    def __init__(self, pairs):
        self.chat = Chat(responses, reflections)

    def respond(self, user_input):
        response = self.chat.respond(user_input)
        if response == "I'm sorry, I didn't understand that. Let me get another response from gpt bot.":
            gpt_response = gpt_responses(user_input)
            return "\n" + gpt_response
        return response

def chat_with_bot():
    print("Hello, I am your chatbot! Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye! Have a nice day!")
            break
        response = chatbot.respond(user_input)
        print(f"Chatbot: {response}")

chatbot = RuleBasedChatbot(responses)
chat_with_bot()
