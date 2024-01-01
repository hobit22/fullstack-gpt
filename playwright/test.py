from actions.my_agent import create_agent
from langchain.chat_models import ChatOpenAI
import os

location = os.getcwd();
print(location)

llm = ChatOpenAI(
    temperature=0.3,
    # model="gpt-4",
    openai_api_key = ""
    )

# create_pytest()
agent = create_agent(llm)

prompt = """
go to ai.matamath.net and login id : 23-10101, pw : 12345
"""

agent.invoke(prompt)


# text = make_file()
# f = open("hbk.py", 'w')
# f.write(text)

