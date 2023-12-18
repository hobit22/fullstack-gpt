from dotenv import load_dotenv
import asyncio
from langchain.chat_models import ChatOpenAI
from langchain.tools import StructuredTool
from langchain.agents import initialize_agent, AgentType
# This import is required only for jupyter notebooks, since they have their own eventloop
import nest_asyncio
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.tools.playwright.utils import (
    create_async_playwright_browser,  # A synchronous browser is available, though it isn't compatible with jupyter.
)

from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import JSONAgentOutputParser

from langchain.agents import AgentExecutor

load_dotenv()
nest_asyncio.apply()

async_browser = create_async_playwright_browser()
browser_toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
tools = browser_toolkit.get_tools()

from langchain import hub

prompt = hub.pull("hwchase17/react-multi-input-json")

from langchain.tools.render import render_text_description_and_args

prompt = prompt.partial(
    tools=render_text_description_and_args(tools),
    tool_names=", ".join([t.name for t in tools]),
)

llm = ChatOpenAI(temperature=0.1)

llm_with_stop = llm.bind(stop=["Observation"])

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    }
    | prompt
    | llm_with_stop
    | JSONAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

async def test():
    response = await agent_executor.ainvoke(
        {"input": "Browse to blog.langchain.dev and summarize the text, please."}
    )
    return response["output"]


loop = asyncio.get_event_loop()

res = loop.run_until_complete(test())

print(res)

