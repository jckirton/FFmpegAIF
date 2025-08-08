class Menu:
    def __init__(self, menu: str, *, menus_source: str = "menus.json"):
        """A menu that can be presented to the user.

        Args:
            menu (str): Key of the menu in the menus JSON.
            menus_source (str, optional): Relative path to the menus JSON. Defaults to "menus.json".
        """
        from json import load

        with open(menus_source, "r") as f:
            self.menu: dict = load(f)[menu]

        self.options: dict = self.menu["options"]
        self.ui: str = self.menu["ui"]

    def __str__(self):
        return f"{self.menu}"

    def prompt(
        self, *, input_note: str | None = "", err_msg: str | None = "Invalid input.\n"
    ) -> str | float | int:
        inputNote: str | None = input_note
        if "int" in self.options.keys():
            while True:
                ui: str = self.ui.format(inputNote)

                print("\n" * 20)
                userInput = input(ui)
                try:
                    userInput = int(userInput)
                    return userInput
                except Exception:
                    inputNote = err_msg
        elif "float" in self.options.keys():
            while True:
                ui: str = self.ui.format(inputNote)

                print("\n" * 20)
                userInput = input(ui)
                try:
                    userInput = float(userInput)
                    return userInput
                except Exception:
                    inputNote = err_msg
        elif "any" in self.options.keys():
            ui: str = self.ui.format(inputNote)

            print("\n" * 20)
            userInput = input(ui)
            return userInput
        else:
            while True:
                ui: str = self.ui.format(inputNote)

                print("\n" * 20)
                userInput = input(ui)

                if userInput in self.options:
                    return self.options[userInput]
                else:
                    inputNote = err_msg


# testMenu = Menu("menuInt")

# # print(testMenu)
# print(testMenu.prompt())
