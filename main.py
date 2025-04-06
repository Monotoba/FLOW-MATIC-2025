import sys
import os
import platform
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Callable
from enum import Enum, auto


class ValueType(Enum):
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    DATE = auto()
    TIME = auto()
    DATETIME = auto()
    RECORD = auto()
    COLLECTION = auto()
    NULL = auto()


class FlowMaticValue:
    def __init__(self, value: Any, type: ValueType):
        self.value = value
        self.type = type

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"FlowMaticValue({self.value}, {self.type})"


class PlatformAdapter:
    @staticmethod
    def get_line_ending() -> str:
        if platform.system() == 'Windows':
            return '\r\n'
        return '\n'

    @staticmethod
    def clear_screen():
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def get_encoding() -> str:
        if platform.system() == 'Windows':
            return 'cp1252'
        return 'utf-8'


class Extension(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def register_statements(self) -> Dict[str, Callable]:
        pass

    @abstractmethod
    def initialize(self, interpreter: 'FlowMaticInterpreter'):
        pass


class ExtensionManager:
    def __init__(self):
        self.extensions: Dict[str, Extension] = {}
        self.registered_statements: Dict[str, Callable] = {}

    def register_extension(self, extension: Extension):
        name = extension.get_name()
        if name in self.extensions:
            raise ValueError(f"Extension {name} already registered")
        self.extensions[name] = extension

    def initialize_extensions(self, interpreter: 'FlowMaticInterpreter'):
        for ext in self.extensions.values():
            ext.initialize(interpreter)
            self.registered_statements.update(ext.register_statements())

    def is_extension_loaded(self, name: str) -> bool:
        return name in self.extensions

    def get_statement_handler(self, statement: str) -> Optional[Callable]:
        return self.registered_statements.get(statement)


class FlowMaticInterpreter:
    def __init__(self):
        self.variables: Dict[str, FlowMaticValue] = {}
        self.labels: Dict[str, int] = {}
        self.current_line = 0
        self.program: List[str] = []
        self.running = False
        self.extension_manager = ExtensionManager()
        self.text_encoding = 'utf-8'
        self.error_handler = None
        self.output_device = sys.stdout
        self.input_device = sys.stdin

        self.core_statements = {
            'INPUT': self.handle_input,
            'READ': self.handle_input,
            'OUTPUT': self.handle_output,
            'WRITE': self.handle_output,
            'COMPARE': self.handle_compare,
            'MOVE': self.handle_move,
            'SET': self.handle_set,
            'JUMP': self.handle_jump,
            'DEFINE': self.handle_define,
            'CODE': self.handle_code_constant,
            'STOP': self.handle_stop,
            'USE': self.handle_use_extensions
        }

    def load_program(self, program_text: str):
        self.program = program_text.splitlines()
        self._parse_labels()

    def _parse_line(self, line: str) -> tuple:
        """Parse a line into (line_number, label, statement, comment)"""
        line = line.strip()
        if not line or line.startswith('*'):
            return (None, None, None, None)

        # Extract line number (4 digits at start)
        line_number = None
        if len(line) >= 4 and line[:4].isdigit():
            line_number = int(line[:4])
            line = line[4:].lstrip()

        # Extract comment
        comment = None
        if '*' in line:
            line, comment = line.split('*', 1)
            line = line.rstrip()
            comment = comment.strip()

        # Extract label (ends with colon)
        label = None
        parts = line.split()
        if parts and parts[0].endswith(':'):
            label = parts[0][:-1]
            line = ' '.join(parts[1:])

        return (line_number, label, line.strip(), comment)

    def _parse_labels(self):
        for i, line in enumerate(self.program):
            _, label, _, _ = self._parse_line(line)
            if label:
                self.labels[label] = i

    def run(self):
        self.running = True
        self.current_line = 0

        while self.running and self.current_line < len(self.program):
            line = self.program[self.current_line]
            _, label, statement, _ = self._parse_line(line)

            if label:
                self.labels[label] = self.current_line

            if statement:
                try:
                    self._execute_statement(statement)
                except Exception as e:
                    if self.error_handler:
                        self.error_handler(e, self.current_line)
                    else:
                        print(f"Error at line {self.current_line + 1}: {str(e)}", file=sys.stderr)
                    self.running = False

            self.current_line += 1

    def _execute_statement(self, statement: str):
        parts = statement.split()
        if not parts:
            return

        stmt = parts[0]

        # Check core statements first
        handler = self.core_statements.get(stmt)
        if handler:
            handler(statement)
            return

        # Check extension statements
        ext_handler = self.extension_manager.get_statement_handler(stmt)
        if ext_handler:
            ext_handler(statement)
            return

        # Check for arithmetic assignment
        if ':=' in statement:
            self.handle_arithmetic(statement)
            return

        raise ValueError(f"Unknown statement: {stmt}")

    def handle_input(self, line: str):
        if '"' in line:
            # Format with prompt
            prompt_start = line.find('"')
            prompt_end = line.find('"', prompt_start + 1)
            prompt = line[prompt_start + 1:prompt_end]
            remaining = line[prompt_end + 1:].strip().split()

            if len(remaining) < 3 or remaining[0] != 'FROM' or remaining[2] != 'TO':
                raise ValueError("Invalid INPUT statement syntax with prompt")

            device = remaining[1]
            variable = remaining[3]

            if device == 'CONSOLE':
                print(prompt, end='', flush=True)
                value = input()
                self.variables[variable] = FlowMaticValue(value, ValueType.STRING)
        else:
            # Format without prompt
            parts = line.split()
            if len(parts) < 4 or parts[1] != 'FROM' or parts[3] != 'TO':
                raise ValueError("Invalid INPUT statement syntax")

            device = parts[2]
            variables = ' '.join(parts[4:]).split(',')

            if device == 'CONSOLE':
                for var in variables:
                    var = var.strip()
                    if var:
                        value = input()
                        self.variables[var] = FlowMaticValue(value, ValueType.STRING)

    def handle_output(self, line: str):
        # Handle both formats:
        # 1. WRITE "text" TO CONSOLE
        # 2. WRITE variable TO CONSOLE
        parts = line.split()
        if len(parts) < 4 or parts[-2] != 'TO' or parts[-1] != 'CONSOLE':
            raise ValueError("Invalid WRITE statement syntax")

        content = ' '.join(parts[1:-2])

        if '"' in content:
            # Direct string output
            text = content.strip('"')
            print(text, end='', file=self.output_device, flush=True)
        else:
            # Variable output
            value = self.variables.get(content, FlowMaticValue('', ValueType.STRING))
            print(value.value, end='', file=self.output_device, flush=True)

    def handle_compare(self, line: str):
        parts = line.split()
        if len(parts) < 4 or parts[2] != 'TO':
            raise ValueError("Invalid COMPARE statement")

        var = parts[1]
        value = parts[3]

        var_value = self.variables.get(var)
        if not var_value:
            raise ValueError(f"Variable {var} not defined")

        if value in self.variables:
            compare_value = self.variables[value]
        else:
            try:
                compare_value = FlowMaticValue(float(value) if '.' in value else int(value), ValueType.NUMBER)
            except ValueError:
                if value.startswith('"') and value.endswith('"'):
                    compare_value = FlowMaticValue(value[1:-1], ValueType.STRING)
                else:
                    compare_value = FlowMaticValue(value, ValueType.STRING)

        self.variables['__COMPARE_RESULT'] = FlowMaticValue(
            var_value.value == compare_value.value,
            ValueType.BOOLEAN
        )

    def handle_move(self, line: str):
        parts = line.split()
        if len(parts) < 4 or parts[2] != 'TO':
            raise ValueError("Invalid MOVE statement")

        src = parts[1]
        dest = parts[3]

        src_value = self.variables.get(src)
        if not src_value:
            raise ValueError(f"Variable {src} not defined")

        self.variables[dest] = src_value

    def handle_set(self, line: str):
        parts = line.split()
        if len(parts) < 4 or parts[2] != 'TO':
            raise ValueError("Invalid SET statement")

        var = parts[1]
        value = ' '.join(parts[3:])

        if value in self.variables:
            self.variables[var] = self.variables[value]
        else:
            try:
                num_value = float(value) if '.' in value else int(value)
                self.variables[var] = FlowMaticValue(num_value, ValueType.NUMBER)
            except ValueError:
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                self.variables[var] = FlowMaticValue(value, ValueType.STRING)

    def handle_jump(self, line: str):
        parts = line.split()
        if len(parts) < 3 or parts[1] != 'TO':
            raise ValueError("Invalid JUMP statement")

        label = parts[2]

        if 'UNLESS' in parts:
            unless_index = parts.index('UNLESS')
            if unless_index + 1 < len(parts):
                condition_var = parts[unless_index + 1]
                if self.variables.get('__COMPARE_RESULT', FlowMaticValue(False, ValueType.BOOLEAN)).value:
                    return

        if label in self.labels:
            self.current_line = self.labels[label] - 1

    def handle_define(self, line: str):
        parts = line.split()
        if len(parts) < 4 or parts[2] != 'AS':
            raise ValueError("Invalid DEFINE statement")

        if parts[1] == 'RECORD':
            pass
        else:
            var = parts[1]
            value = ' '.join(parts[3:])
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            self.variables[var] = FlowMaticValue(value, ValueType.STRING)

    def handle_code_constant(self, line: str):
        parts = line.split()
        if len(parts) < 5 or parts[1] != 'CONSTANT' or parts[3] != 'IS':
            raise ValueError("Invalid CODE CONSTANT statement")

        name = parts[2]
        value = ' '.join(parts[4:])

        if value == 'CR':
            self.variables[name] = FlowMaticValue('\r', ValueType.STRING)
        elif value == 'LF':
            self.variables[name] = FlowMaticValue('\n', ValueType.STRING)
        elif value == 'CRLF':
            self.variables[name] = FlowMaticValue('\r\n', ValueType.STRING)
        else:
            self.variables[name] = FlowMaticValue(value, ValueType.STRING)

    def handle_stop(self, line: str):
        self.running = False

    def handle_use_extensions(self, line: str):
        parts = line.split()
        if len(parts) < 3 or parts[1] != 'EXTENSIONS':
            raise ValueError("Invalid USE EXTENSIONS statement")

        extensions = [ext.rstrip(',') for ext in parts[2:]]
        for ext in extensions:
            if ext == 'CONSOLE-IO':
                self.extension_manager.register_extension(ConsoleIOExtension())
            print(f"Loaded extension: {ext}")
        self.extension_manager.initialize_extensions(self)

    def handle_arithmetic(self, line: str):
        var, expr = line.split(':=')
        var = var.strip()
        expr = expr.strip()

        try:
            safe_dict = {k: v.value for k, v in self.variables.items() if isinstance(v.value, (int, float))}
            safe_dict.update({'__builtins__': None})
            result = eval(expr, safe_dict)
            self.variables[var] = FlowMaticValue(result, ValueType.NUMBER)
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {expr} - {str(e)}")


class ConsoleIOExtension(Extension):
    def get_name(self) -> str:
        return "CONSOLE-IO"

    def register_statements(self) -> Dict[str, Callable]:
        return {
            'CONFIG': self.handle_config_console,
            'CLEAR': self.handle_clear_console
        }

    def initialize(self, interpreter: FlowMaticInterpreter):
        self.interpreter = interpreter

    def handle_config_console(self, line: str):
        parts = line.split()
        if len(parts) < 2:
            raise ValueError("Invalid CONFIG statement")

        if parts[1] == 'TEXT-ENCODING':
            if len(parts) > 2:
                self.interpreter.text_encoding = parts[2]

    def handle_clear_console(self, line: str):
        PlatformAdapter.clear_screen()


def main():
    if len(sys.argv) < 2:
        print("Usage: flowmatic <program_file>")
        return

    program_file = sys.argv[1]
    try:
        with open(program_file, 'r', encoding='utf-8') as f:
            program_text = f.read()
    except FileNotFoundError:
        print(f"Error: File {program_file} not found")
        return

    interpreter = FlowMaticInterpreter()
    interpreter.load_program(program_text)
    interpreter.run()


if __name__ == "__main__":
    main()