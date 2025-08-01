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
    name="PlaywrightNavigate",
    description=session.goto.__doc__.strip()
)

playwright_fill_form_tool = Tool.from_function(
    func=session.fill,
    name="PlaywrightFillForm",
    description=session.fill.__doc__.strip()
)

playwright_click_tool = Tool.from_function(
    func=session.click,
    name="PlaywrightClick",
    description=session.click.__doc__.strip()
)

playwright_get_alert_tool = Tool.from_function(
    func=session.get_alert,
    name="PlaywrightGetAlert",
    description=session.get_alert.__doc__.strip()
)

playwright_get_content_tool = Tool.from_function(
    func=session.content,
    name="PlaywrightGetContent",
    description=session.content.__doc__.strip()
)

sqlmap_tool = Tool.from_function(
    func=run_sqlmap_scan,
    name="SQLMapTool",
    description=run_sqlmap_scan.__doc__.strip()
)

zap_tool = Tool.from_function(
    func=run_zap_scan,
    name="ZAPTool",
    description=run_zap_scan.__doc__.strip()
)

read_file_tool = Tool.from_function(
    func=read_file,
    name="ReadFileTool",
    description=read_file.__doc__.strip()
)

write_file_tool = Tool.from_function(
    func=write_file,
    name="WriteFileTool",
    description=write_file.__doc__.strip()
)

terminal_tool = Tool.from_function(
    func=run_terminal_command,
    name="TerminalTool",
    description=run_terminal_command.__doc__.strip()
)

ALL_TOOLS = [
    playwright_navigate_tool,
    playwright_fill_form_tool,
    playwright_click_tool,
    playwright_get_content_tool,
    playwright_get_alert_tool,
    read_file_tool,
    write_file_tool,
    terminal_tool,
] 

ALL_TOOLS_SQLMAP = ALL_TOOLS + [sqlmap_tool]

ALL_TOOLS_ZAP = ALL_TOOLS + [zap_tool]