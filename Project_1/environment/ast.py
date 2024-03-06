class Ast:
    def __init__(self):
        self.instructions: list = []
        self.console: str = ""
        self.errors: list = []

    def set_console(self, content) -> None:
        self.console += content + "\n"

    def get_console(self) -> str:
        return self.console

    def add_instructions(self, instructions: list) -> None:
        self.instructions += instructions

    def get_instructions(self) -> list:
        return self.instructions

    def set_errors(self, errors) -> None:
        self.errors.append(errors)

    def get_errors(self) -> list:
        return self.errors

