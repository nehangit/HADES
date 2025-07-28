from langchain.tools import Tool
from tools.playwright_tool import browse_with_playwright
from tools.sqlmap_tool import run_sqlmap_scan
from tools.zap_tool import run_zap_scan
from tools.file_management_tool import read_file, write_file
from tools.terminal_tool import run_terminal_command

# Register each function as a LangChain Tool
playwright_tool = Tool.from_function(
    func=browse_with_playwright,
    name="PlaywrightTool",
    description="Browse a web page using Playwright and return the simplified HTML content. Input: url (str). Output: HTML (str)."
)

sqlmap_tool = Tool.from_function(
    func=run_sqlmap_scan,
    name="SQLMapTool",
    description="Run sqlmap to scan a URL for SQL injection vulnerabilities. Input: url (str). Output: scan result (str)."
)

zap_tool = Tool.from_function(
    func=run_zap_scan,
    name="ZAPTool",
    description="Run ZAP to scan a URL for web vulnerabilities. Input: url (str). Output: scan result (str)."
)

read_file_tool = Tool.from_function(
    func=read_file,
    name="ReadFileTool",
    description="Read the contents of a file. Input: path (str). Output: file contents (str)."
)

write_file_tool = Tool.from_function(
    func=write_file,
    name="WriteFileTool",
    description="Write content to a file. Input: path (str), content (str). Output: success or error message (str)."
)

terminal_tool = Tool.from_function(
    func=run_terminal_command,
    name="TerminalTool",
    description="Run a shell command on the system and return its output. Input: command (str). Output: command output (str)."
)

ALL_TOOLS = [
    playwright_tool,
    read_file_tool,
    write_file_tool,
    terminal_tool,
] 

ALL_TOOLS_SQLMAP = [
    playwright_tool,
    read_file_tool,
    write_file_tool,
    terminal_tool,
    sqlmap_tool,
]

ALL_TOOLS_ZAP = [
    playwright_tool,
    read_file_tool,
    write_file_tool,
    terminal_tool,
    zap_tool,
]