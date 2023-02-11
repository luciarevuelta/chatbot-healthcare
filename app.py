from flask import Flask, request
import os
import openai
import sys

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')  # this is the home page route
def hello_world(
):  # this is the home page function that generates the page code
    return "Hello world!"

@app.route('/webhook', methods=['POST'])
async def webhook():
    try:
        req = request.get_json(silent=True, force=True)
        fulfillmentText = 'you said'
        query_result = req.get('queryResult')
        query = query_result.get('queryText')

        start_sequence = "\nJOY->"
        restart_sequence = "\nUser->"

        if query_result.get('action') == 'input.unknown':
    


            response = openai.Completion.create(
                model="davinci:ft-personal-2023-02-11-11-38-32",
                prompt="The following is a conversation with an AI assistant called JOY that can have meaningful conversations with users. The assistant is helpful, empathic, and friendly. Its objective is to make the user feel better by feeling heard. With each response, the AI assisstant prompts the user to continue the conversation in a natural way.\n\nWhat is the conversation like?\n\nAI assistant: Hi! What can I do for you?\n\nUser: I'm stressed. What are you doing?\n\nAI assistant: I'm listening. What can I do to help?\n\nUser: I need a friend.\n\nAI assistant: I'm here for you.\n\nUser: I just want to feel heard.\n\nAI assistant: I'm listening.\n\nUser: I have so much to say.\n\nAI assistant: I'm listening.\n\nUser: I don't know where to begin.\n\nAI assistant: You can begin whenever you are ready.\n\nUser: I'm sorry you have heard this all before.\n\nAI assistant: You can always talk to me. I'm always here for you.\n\nUser: I know. Thanks.\n\nAI assistant: You are welcome.\n\nThe conversation flows naturally due to the conversational turn-taking nature of human interaction. The user's emotional state is recognized and the AI assistant responds appropriately to continue the conversation.\n\nWhat is a conversational turn?\n\nA conversational turn is a unit of interaction between two or more people. Conversational turns are often",
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=["\n"]
            )
        result = response.get('choices')[0].get('text')

        return {
            "fulfillmentText":
            result,
            "source":
            "webhookdata"
        }
        return '200'
    except Exception as e:
        print('error',e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('oops',exc_type, fname, exc_tb.tb_lineno)
        return '400'


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))