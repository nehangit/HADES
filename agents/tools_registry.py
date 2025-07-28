from langchain.tools import Tool
from tools.sqlmap_tool import run_sqlmap_scan
from tools.zap_tool import run_zap_scan
from tools.file_management_tool import read_file, write_file
from tools.terminal_tool import run_terminal_command
from tools.playwright_tool import PlaywrightSession

# Shared playwright session across all tools
session = PlaywrightSession()

playwright_navigate_tool = Tool.from_function(
    func=session.goto,
    name="PlaywrightNavigate"
)

playwright_fill_form_tool = Tool.from_function(
    func=session.fill,
    name="PlaywrightFillForm"
)

playwright_click_tool = Tool.from_function(
    func=session.click,
    name="PlaywrightClick"
)

playwright_get_content_tool = Tool.from_function(
    func=session.content,
    name="PlaywrightGetContent"
)

sqlmap_tool = Tool.from_function(
    func=run_sqlmap_scan,
    name="SQLMapTool",
)

zap_tool = Tool.from_function(
    func=run_zap_scan,
    name="ZAPTool",
)

read_file_tool = Tool.from_function(
    func=read_file,
    name="ReadFileTool",
)

write_file_tool = Tool.from_function(
    func=write_file,
    name="WriteFileTool",
)

terminal_tool = Tool.from_function(
    func=run_terminal_command,
    name="TerminalTool",
)

ALL_TOOLS = [
    playwright_navigate_tool,
    playwright_fill_form_tool,
    playwright_click_tool,
    playwright_get_content_tool,
    read_file_tool,
    write_file_tool,
    terminal_tool,
] 

ALL_TOOLS_SQLMAP = ALL_TOOLS + [sqlmap_tool]

ALL_TOOLS_ZAP = ALL_TOOLS + [zap_tool]