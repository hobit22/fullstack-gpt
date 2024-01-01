from langchain.agents import initialize_agent, AgentType
from langchain.tools import StructuredTool
from playwright.async_api import async_playwright

path = "example.png"
data =""

async def get_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        return page, browser

async def click_action(selector):
    page, browser = await get_page()
    await page.click(selector)
    await page.screenshot(path=path)
    return page

async def input_action(selector, text):
    page, browser = await get_page()
    await page.fill(selector, text)
    await page.screenshot(path=path)
    return page

async def navigate_action(url):
    page, browser = await get_page()
    await page.goto(url)
    await page.screenshot(path=path)
    return page

async def wait_for_selector_action(selector):
    page, browser = await get_page()
    await page.wait_for_selector(selector)
    await page.screenshot(path=path)
    return page


async def login_action(url, username_selector, username, password_selector, password, login_button_selector):
    page, browser = await get_page()
    await page.goto(url)
    await page.fill(username_selector, username)
    await page.fill(password_selector, password)
    await page.click(login_button_selector)
    await page.screenshot(path=path)
    return page
    
# def click_action(selector):
#     global data
#     data += f'''
#     page.click("{selector}")
#     '''
#     print(data)
#     return data

# def input_action(selector, text):
#     global data
#     data += f'''
#     page.fill("{selector}", "{text}")
#     '''
#     print(data)
#     return data
# def navigate_action(url):
#     global data
#     data += f'''
#     page.goto("{url}")
#     '''
#     print(data)
#     return data
# def wait_for_selector_action(selector):
#     global data
#     data += f'''
#     page.wait_for_selector("{selector}")
#     '''
#     print(data)
#     return data

# def login_action(url, username_selector, username, password_selector, password, login_button_selector):
#     global data
#     data +=f'''
#     page.goto("{url}")
#     page.fill("{username_selector}", "{username}")
#     page.fill("{password_selector}", "{password}")
#     page.click("{login_button_selector}")
# '''
#     print(data)
#     return data
# def create_pytest():
#     global data
#     data +=f"""
# import re
# from playwright.sync_api import Page, expect

# def test(page: Page):
#     """
#     print(data)
#     return data

# def make_file():
#     global data
#     return data

def create_agent(llm):
    agent = initialize_agent(
        llm=llm, 
        verbose=True,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        tools=[
            # StructuredTool.from_function(
            #     func=get_page,
            #     name="get page tool",
            #     description="""
            #     This tool initializes and returns a new Playwright page object.
            #     Use this tool to start a browser session and get a page object for further operations.
            #     """,
            # ),
            StructuredTool.from_function(
                func=click_action,
                name="click action tool",
                description="""
                This tool performs a click action on a specified element on the web page. 
                Provide the selector of the element to perform the click.
                """,
            ), 
            StructuredTool.from_function(
                func=input_action,
                name="input action tool",
                description="""
                This tool inputs text into a specified field on a web page. 
                Provide the selector of the input field and the text to be entered.
                """,
            ),
            StructuredTool.from_function(
                func=navigate_action,
                name="navigation action tool",
                description="""
                This tool navigates to a specified URL. 
                Provide the URL to navigate to.
                """,
            ),
            StructuredTool.from_function(
                func=wait_for_selector_action,
                name="wait for selector action tool",
                description="""
                This tool waits for a specified element to be present on the web page before performing further actions.
                Provide the selector of the element to wait for.
                """,
            )
        ],   
    )
    return agent