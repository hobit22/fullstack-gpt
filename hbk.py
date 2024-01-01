
import re
from playwright.sync_api import Page, expect

def test(page: Page):
    
    page.goto("https://ai.matamath.net")
    
    page.goto("https://ai.matamath.net")
    
    page.fill("#id", "23-10101")
        
    page.click("#login-button")
    
    page.wait_for_selector(".dashboard")
    