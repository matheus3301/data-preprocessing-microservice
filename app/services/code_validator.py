import ast
from typing import List, Dict, Any, Tuple, Set

from app.core.config import settings


class CodeValidator:
    def __init__(self):
        self.allowed_imports = set(settings.ALLOWED_IMPORTS)
        self.disallowed_functions = {
            "eval", "exec", "compile", "globals", "locals", "getattr", "setattr", 
            "delattr", "open", "input", "__import__", "breakpoint", "memoryview",
            "system", "popen", "subprocess", "os.system", "os.popen", "os.execl",
            "os.execle", "os.execlp", "os.execlpe", "os.execv", "os.execve",
            "os.execvp", "os.execvpe", "os.spawn", "os.spawnl", "os.spawnle",
            "os.spawnlp", "os.spawnlpe", "os.spawnv", "os.spawnve", "os.spawnvp",
            "os.spawnvpe", "os.fork", "os.forkpty", "os.kill", "os.killpg",
            "os.plock", "os.popen", "os.popen2", "os.popen3", "os.popen4",
            "os.spawnl", "os.spawnle", "os.spawnlp", "os.spawnlpe", "os.spawnv",
            "os.spawnve", "os.spawnvp", "os.spawnvpe", "os.startfile",
        }
        self.disallowed_modules = {
            "os", "sys", "subprocess", "shutil", "socket", "requests", "urllib",
            "http", "ftplib", "telnetlib", "smtplib", "poplib", "imaplib", "nntplib",
            "builtins", "importlib", "pathlib", "io", "pickle", "shelve", "marshal",
            "dbm", "sqlite3", "zlib", "gzip", "bz2", "lzma", "zipfile", "tarfile",
            "multiprocessing", "threading", "concurrent", "asyncio", "signal",
            "mmap", "readline", "rlcompleter", "code", "codeop", "timeit", "trace",
            "tracemalloc", "distutils", "ensurepip", "venv", "zipapp", "platform",
            "inspect", "site", "cmd", "runpy", "sysconfig", "msvcrt", "winreg",
            "winsound", "posix", "pwd", "spwd", "grp", "crypt", "termios", "tty",
            "pty", "fcntl", "pipes", "resource", "nis", "syslog", "optparse",
            "imp", "gc", "traceback", "linecache", "symtable", "compileall",
            "py_compile", "modulefinder", "fileinput", "stat", "filecmp", "tempfile",
            "glob", "fnmatch", "netrc", "formatter", "email", "mailbox", "mimetypes",
            "base64", "binhex", "binascii", "quopri", "uu", "xdrlib", "ssl",
            "hashlib", "hmac", "secrets", "uuid", "ipaddress", "audioop", "aifc",
            "sunau", "wave", "chunk", "colorsys", "imghdr", "sndhdr", "ossaudiodev",
            "getpass", "curses", "logging", "getopt", "argparse", "calendar",
            "collections", "contextlib", "dataclasses", "datetime", "decimal",
            "enum", "functools", "itertools", "operator", "random", "re", "string",
            "textwrap", "unicodedata", "weakref", "types", "copy", "pprint",
            "reprlib", "time", "warnings", "atexit", "traceback", "builtins",
            "importlib", "pkgutil", "typing", "pdb", "faulthandler", "turtledemo",
            "tkinter", "ctypes", "distutils", "encodings", "unittest", "test",
            "xmlrpc", "idlelib", "lib2to3", "wsgiref", "xml", "html", "http",
            "urllib", "socketserver", "selectors", "select", "queue", "dummy_threading",
            "_thread", "sched", "cgi", "cgitb", "wsgiref", "webbrowser", "json",
            "configparser", "csv", "hashlib", "hmac", "secrets", "uuid", "ipaddress",
            "ssl", "socket", "email", "mimetypes", "base64", "binhex", "binascii",
            "quopri", "uu", "xdrlib", "zipfile", "tarfile", "copyreg", "shelve",
            "marshal", "dbm", "sqlite3", "zlib", "gzip", "bz2", "lzma", "zipfile",
            "tarfile", "csv", "configparser", "netrc", "xdrlib", "plistlib",
            "cryptography", "paramiko", "ftplib", "poplib", "imaplib", "nntplib",
            "smtplib", "smtpd", "telnetlib", "uuid", "socketserver", "http",
            "http.client", "http.server", "http.cookies", "http.cookiejar",
            "urllib", "urllib.request", "urllib.response", "urllib.parse",
            "urllib.error", "urllib.robotparser", "xmlrpc", "xmlrpc.client",
            "xmlrpc.server", "ipaddress", "asyncio", "asyncore", "asynchat",
            "signal", "mmap", "email", "mailbox", "mimetypes", "base64", "binhex",
            "binascii", "quopri", "uu", "html", "html.parser", "html.entities",
            "xml", "xml.etree.ElementTree", "xml.dom", "xml.dom.minidom",
            "xml.dom.pulldom", "xml.sax", "xml.sax.handler", "xml.sax.saxutils",
            "xml.sax.xmlreader", "xml.parsers.expat", "webbrowser", "cgi",
            "cgitb", "wsgiref", "wsgiref.simple_server", "wsgiref.handlers",
            "wsgiref.headers", "wsgiref.util", "wsgiref.validate", "urllib",
            "urllib.request", "urllib.response", "urllib.parse", "urllib.error",
            "urllib.robotparser", "http", "http.client", "http.server",
            "http.cookies", "http.cookiejar", "socketserver", "selectors",
            "select", "threading", "multiprocessing", "concurrent", "concurrent.futures",
            "subprocess", "sched", "queue", "dummy_threading", "_thread", "socket",
            "ssl", "hashlib", "hmac", "secrets", "uuid", "ipaddress", "cryptography",
            "paramiko", "ftplib", "poplib", "imaplib", "nntplib", "smtplib",
            "smtpd", "telnetlib", "uuid", "socketserver", "http", "http.client",
            "http.server", "http.cookies", "http.cookiejar", "urllib", "urllib.request",
            "urllib.response", "urllib.parse", "urllib.error", "urllib.robotparser",
            "xmlrpc", "xmlrpc.client", "xmlrpc.server", "ipaddress", "asyncio",
            "asyncore", "asynchat", "signal", "mmap", "email", "mailbox", "mimetypes",
            "base64", "binhex", "binascii", "quopri", "uu", "html", "html.parser",
            "html.entities", "xml", "xml.etree.ElementTree", "xml.dom", "xml.dom.minidom",
            "xml.dom.pulldom", "xml.sax", "xml.sax.handler", "xml.sax.saxutils",
            "xml.sax.xmlreader", "xml.parsers.expat", "webbrowser", "cgi", "cgitb",
            "wsgiref", "wsgiref.simple_server", "wsgiref.handlers", "wsgiref.headers",
            "wsgiref.util", "wsgiref.validate", "urllib", "urllib.request",
            "urllib.response", "urllib.parse", "urllib.error", "urllib.robotparser",
            "http", "http.client", "http.server", "http.cookies", "http.cookiejar",
            "socketserver", "selectors", "select", "threading", "multiprocessing",
            "concurrent", "concurrent.futures", "subprocess", "sched", "queue",
            "dummy_threading", "_thread",
        }

    def validate_code(self, code: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate the user's code for security and correctness.
        
        Args:
            code: Python code to validate
            
        Returns:
            Tuple containing a boolean indicating if the code is valid and a dictionary with validation details
        """
        try:
            # Parse the code into an AST
            tree = ast.parse(code)
            
            # Check for imports
            import_validator = ImportValidator(self.allowed_imports, self.disallowed_modules)
            import_validator.visit(tree)
            
            if import_validator.disallowed_imports:
                return False, {
                    "valid": False,
                    "error": "Disallowed imports detected",
                    "details": {
                        "disallowed_imports": list(import_validator.disallowed_imports)
                    }
                }
            
            # Check for dangerous function calls
            function_validator = FunctionValidator(self.disallowed_functions)
            function_validator.visit(tree)
            
            if function_validator.dangerous_calls:
                return False, {
                    "valid": False,
                    "error": "Dangerous function calls detected",
                    "details": {
                        "dangerous_calls": list(function_validator.dangerous_calls)
                    }
                }
            
            # Check for process function
            process_validator = ProcessFunctionValidator()
            process_validator.visit(tree)
            
            if not process_validator.has_process_function:
                return False, {
                    "valid": False,
                    "error": "No 'process' function found",
                    "details": {
                        "required": "The code must define a 'process' function that takes a DataFrame and returns a DataFrame"
                    }
                }
            
            if not process_validator.has_correct_signature:
                return False, {
                    "valid": False,
                    "error": "Invalid 'process' function signature",
                    "details": {
                        "required": "The 'process' function must take at least one parameter (DataFrame)"
                    }
                }
            
            return True, {
                "valid": True,
                "imports": list(import_validator.allowed_imports)
            }
            
        except SyntaxError as e:
            return False, {
                "valid": False,
                "error": "Syntax error in code",
                "details": {
                    "line": e.lineno,
                    "offset": e.offset,
                    "text": e.text
                }
            }
        except Exception as e:
            return False, {
                "valid": False,
                "error": f"Error validating code: {str(e)}",
                "details": {}
            }


class ImportValidator(ast.NodeVisitor):
    def __init__(self, allowed_imports: Set[str], disallowed_modules: Set[str]):
        self.allowed_imports = allowed_imports
        self.disallowed_modules = disallowed_modules
        self.allowed_imports_found: Set[str] = set()
        self.disallowed_imports: Set[str] = set()
    
    def visit_Import(self, node: ast.Import) -> None:
        for name in node.names:
            module_name = name.name.split('.')[0]
            if module_name in self.disallowed_modules:
                self.disallowed_imports.add(module_name)
            elif module_name in self.allowed_imports:
                self.allowed_imports_found.add(module_name)
            else:
                self.disallowed_imports.add(module_name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            module_name = node.module.split('.')[0]
            if module_name in self.disallowed_modules:
                self.disallowed_imports.add(module_name)
            elif module_name in self.allowed_imports:
                self.allowed_imports_found.add(module_name)
            else:
                self.disallowed_imports.add(module_name)
        self.generic_visit(node)


class FunctionValidator(ast.NodeVisitor):
    def __init__(self, disallowed_functions: Set[str]):
        self.disallowed_functions = disallowed_functions
        self.dangerous_calls: Set[str] = set()
    
    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in self.disallowed_functions:
                self.dangerous_calls.add(func_name)
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                full_name = f"{node.func.value.id}.{node.func.attr}"
                if full_name in self.disallowed_functions:
                    self.dangerous_calls.add(full_name)
        self.generic_visit(node)


class ProcessFunctionValidator(ast.NodeVisitor):
    def __init__(self):
        self.has_process_function = False
        self.has_correct_signature = False
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node.name == "process":
            self.has_process_function = True
            # Check if the function has at least one parameter (for the DataFrame)
            if node.args.args:
                self.has_correct_signature = True
        self.generic_visit(node)


# Singleton instance
code_validator = CodeValidator() 