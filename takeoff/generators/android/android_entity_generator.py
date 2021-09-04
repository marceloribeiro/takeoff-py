import os
from jinja2 import Template
from .android_base_generator import AndroidBaseGenerator
from pathlib import Path
from shutil import copyfile

class AndroidEntityGenerator(AndroidBaseGenerator):

    def __init__(self, name, options):
        super().__init__(name, options)
        self.entity_name = self.options.pop(0)
        self.entity_attributes = []
        self.associations = []

    def entity_class_name(self):
        return self.camelize(self.entity_name)

    def run(self):
        self.setup()
        print(f">>> Running Android Entity Generator: {self.name}")
        self.load_attributes()
        self.write_entity_file()
        self.write_service_file()

    def load_attributes(self):
        for attribute in self.options:
            parts = attribute.split(':')
            if len(parts) == 1:
                parts.append('string')

            self.entity_attributes.append({
                'name': parts[0], 
                'type': parts[1], 
                'class': self.attribute_class(parts[1])
            })

            if parts[1] == 'belongs_to':
                self.associations.append({
                    'name': parts[0], 
                    'class_name': self.camelize(parts[0])
                })
        
        self.entity_attributes.append({
            'name': 'created_at',
            'type': 'datetime',
            'class': 'Date'
        })

        self.entity_attributes.append({
            'name': 'updated_at',
            'type': 'datetime',
            'class': 'Date'
        })

    def attribute_class(self, type):
        switcher = { 
            'string': 'String',
            'text': 'String',
            'integer': 'Int',
            'float': 'Float',
            'boolean': 'Boolean',
            'date': 'Date',
            'datetime': 'Date'
        }
        return switcher.get(type, 'String')
    
    def write_from_template(self, source, destination):
        with open(source) as f:
            template_contents = f.read()

        template = Template(template_contents)
        contents = template.render(generator=self)
        
        with open(destination, 'w') as f:
            f.write(contents)

    def write_entity_file(self):
        package_path = self.android_prefix.replace('.', '/')
        template_path = f"{self.templates_path}/app/src/main/java/models/Entity.kt.template"
        destination_folder = f"{self.project_folder()}/app/src/main/java/{package_path}/models"
        destination = f"{destination_folder}/{self.camelize(self.entity_name)}.kt"
        self.write_from_template(template_path, destination)
    
    def write_service_file(self):
        package_path = self.android_prefix.replace('.', '/')
        template_path = f"{self.templates_path}/app/src/main/java/services/Service.kt.template"
        destination_folder = f"{self.project_folder()}/app/src/main/java/{package_path}/services"
        destination = f"{destination_folder}/{self.camelize(self.entity_name)}Service.kt"
        self.write_from_template(template_path, destination)