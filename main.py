import tkinter as tk
from tkinter import ttk
import json


class CharacterEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Drakar och Demoner Character Editor")
        self.characters = []
        self.geometry("500x300")

        try:
            self.load_characters()
        except FileNotFoundError:
            print("No characters found. Starting with an empty list.")

        self.create_widgets()

    def create_widgets(self):
        self.character_listbox = tk.Listbox(self)
        self.character_listbox.pack(fill=tk.BOTH, expand=True)
        self.populate_character_listbox()

        self.create_character_button = tk.Button(self, text="Create Character", command=self.create_character)
        self.create_character_button.pack(anchor=tk.W)

        self.edit_button = tk.Button(self, text="Edit Character", command=self.edit_character)
        self.edit_button.pack(anchor=tk.W)

        self.quit_button = tk.Button(self, text="Save and Quit", command=self.save_and_quit)
        self.quit_button.pack(anchor=tk.W)

    def create_character(self):
        name = "New Character"
        race = "Race"
        char_class = "Class"
        character = Character(name, race, char_class)
        self.characters.append(character)
        self.populate_character_listbox()


    def populate_character_listbox(self):
        self.character_listbox.delete(0, tk.END)
        for character in self.characters:
            self.character_listbox.insert(tk.END, character.name)

    def edit_character(self):
        selected_index = self.character_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            character = self.characters[selected_index]

            # Create a new window to edit character attributes
            edit_window = CharacterEditWindow(self, character)

    def save_and_quit(self):
        self.save_characters()
        self.destroy()

    def load_characters(self):
        with open("characters.json", "r") as f:
            try:
                character_data = json.load(f)

                for data in character_data:
                    character = Character(data["name"], data["race"], data["char_class"])
                    character.STY = data["STY"]
                    character.FYS = data["FYS"]
                    character.SMI = data["SMI"]
                    character.INT = data["INT"]
                    character.PSY = data["PSY"]
                    character.KAR = data["KAR"]
                    character.max_hp = data["max_hp"]
                    character.max_vp = data["max_vp"]
                    character.hp = data["hp"]
                    character.vp = data["vp"]
                    character.damage_bonus_strength = data["damage_bonus_strength"]
                    character.damage_bonus_agility = data["damage_bonus_agility"]
                    self.characters.append(character)
                print("Loaded characters from file.")
            except:
                print("no characters, continuing...")
            f.close()

    def save_characters(self):
        with open("characters.json", "w") as f:
            character_data = []
            for character in self.characters:
                character_data.append({
                    "name": character.name,
                    "race": character.race,
                    "char_class": character.char_class,
                    "STY": character.STY,
                    "FYS": character.FYS,
                    "SMI": character.SMI,
                    "INT": character.INT,
                    "PSY": character.PSY,
                    "KAR": character.KAR,
                    "max_hp": character.max_hp,
                    "max_vp": character.max_vp,
                    "hp": character.hp,
                    "vp": character.vp,
                    "damage_bonus_strength": character.damage_bonus_strength,
                    "damage_bonus_agility": character.damage_bonus_agility
                })
            json.dump(character_data, f, indent=4)
            print("characters saved")
            f.close()

class CharacterEditWindow(tk.Toplevel):
    def __init__(self, parent, character):
        super().__init__(parent)
        self.parent = parent
        self.character = character
        self.title(f"Edit Character: {character.name}")
        self.geometry("320x250")

        self.create_widgets()

    def create_widgets(self):
        # Create labels and entry fields for all attributes
        attributes = ["STY", "FYS", "SMI", "INT", "PSY", "KAR", "Name", "Race", "Class"]
        other_row = 0

        self.entry_fields = {}  # Store Entry fields in a dictionary

        for column, attribute in enumerate(attributes):
            label = tk.Label(self, text=attribute)
            if attribute in ["Name", "Race", "Class"]:
                entry = tk.Entry(self, width=12)
            else:
                entry = tk.Entry(self, width=3)

            if attribute == "Name":
                entry.insert(0, self.character.name)
            elif attribute == "Race":
                entry.insert(0, self.character.race)
            elif attribute == "Class":
                entry.insert(0, self.character.char_class)
            else:
                entry.insert(0, str(getattr(self.character, attribute)))



            if attribute in ["Name", "Race", "Class"]:
                if attribute == "Name":
                    other_row = 0
                elif attribute == "Race":
                    other_row = 1
                elif attribute == "Class":
                    other_row = 2

                entry.grid(row=other_row, column=2, columnspan=3)
                label.grid(row=other_row, column=0, columnspan=2)
            else:
                entry.grid(row=5, column=column)
                label.grid(row=4, column=column)

            self.entry_fields[attribute] = entry

        self.save_button = tk.Button(self, text="Save", command=self.save_changes)
        self.save_button.grid(row=len(attributes), columnspan=2)

    def save_changes(self):
        # Update character attributes with edited values
        self.character.name = self.entry_fields["Name"].get()
        self.character.race = self.entry_fields["Race"].get()
        self.character.char_class = self.entry_fields["Class"].get()

        for attribute in ["STY", "FYS", "SMI", "INT", "PSY", "KAR"]:
            setattr(self.character, attribute, int(self.entry_fields[attribute].get()))

        # Update listbox to reflect changes
        self.parent.populate_character_listbox()
        self.destroy()  # Close the edit window


class Character:
    def __init__(self, name, race, char_class):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.STY = 0
        self.FYS = 0
        self.SMI = 0
        self.INT = 0
        self.PSY = 0
        self.KAR = 0
        self.max_hp = 0
        self.max_vp = 0
        self.hp = 0
        self.vp = 0
        self.damage_bonus_strength = ""
        self.damage_bonus_agility = ""


if __name__ == "__main__":
    app = CharacterEditor()
    app.mainloop()
