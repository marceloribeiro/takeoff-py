import os
import json
from .android_component_builder import AndroidComponentBuilder

class ButtonBuilder(AndroidComponentBuilder):
    # https://stackoverflow.com/questions/17192104/changing-button-style-in-the-whole-application

    def __init__(self, options, component):
        super().__init__(options, component)
        self.constraints = {}
        self.name = ''
        self.text = ''
        self.text_align = 'center'
        self.text_color = '#ffffff'
        self.lines = []        
        self.load_attributes()

    def load_lines(self):
        self.lines = [
            '   <Button',
            f"      android:id=\"@+id/{self.name}\"",
            f"      android:text=\"{self.text}\"",
            f"      android:textAlignment=\"{self.text_align}\"",
            f"      android:textColor=\"{self.text_color}\""
        ]
        self.lines += self.constraint_lines()
        self.lines += ["      />\n"]

        return ("\n").join(self.lines)