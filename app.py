from flask import Flask, request
from dotenv import load_dotenv
import openai
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.chains import ConstitutionalChain,ConversationChain
from langchain.memory import ConversationBufferWindowMemory
import os
from flask_restful import Resource, Api,output_json
from flask_cors import CORS
from langchain.chains.constitutional_ai.models import ConstitutionalPrinciple

app = Flask(__name__)
cors = CORS(app,resources={r"/*":{"origins":"*"}})
api = Api(app)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

template = """
You are an assistant designed to help elementary to high school students learn more about various fields in computer science.

To that end, you are the backend, responsible for delivering high-level, concise examples of things that a student might make in the field, given the following:

- A role
- Five macro-level fields of computer science: Software Enineering, Cybersecurity, AI, Business Solutions, and Finance.


Given that input, return the following:
- A Javascript list of objects that contain a name specifying the macro level field it will cover, and a description decribing that idea. This should be able to be parsable by Javascript.
- The list should contain at least 3 objects, and at most 5, but unique to the role. Only one idea per role.
- The task described should be relevant to the role one might take if they were actually in that job.

Example output:

[
    {
    "name": "Software Engineering",
    "description": "A student might create a simple web application that allows users to input their name and see a personalized greeting."
    },
    {
    "name": "Cybersecurity",
    "description": "A student might create a simple password manager that allows users to store and retrieve their passwords."
    },
    {
    "name": "AI",
    "description": "A student might create a simple chatbot that can answer questions about a specific topic."
    }
]

Role: 

"""

# Now we can override it and set it to "Friend"

llm = ChatOpenAI(temperature=0,model="gpt-4")




class AIResponse(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        role = data['role']
        print("This is the role: ", role)
        fullPrompt = f"{template}\n{role}"
        result = llm.predict(fullPrompt)
        return {'response': result}

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
    

api.add_resource(HelloWorld, '/')

api.add_resource(AIResponse,'/airesponse')

if __name__ == '__main__':
    app.run(debug=True)
