"""
Abstractions for creating and rendering svelte component from python.
"""

import re
from inspect import Parameter, Signature

import numpy as np

from pysvelte import config, utils
from pysvelte.html import Html


class ArgumentHandler:
    signature = None
    docstring = None
    validate_and_process_args = None
    
    @staticmethod
    def infer_from_src_file(path):
        params = ArgumentHandler.get_params_from_src_file(path)
        
        def validate_and_process_args(**kwargs):
            return kwargs
        
        argument_handler = ArgumentHandler()
        argument_handler.signature = Signature(parameters=params, return_annotation=Html)
        argument_handler.validate_and_process_args = validate_and_process_args
        return argument_handler
        
    @staticmethod
    def get_params_from_src_file(path):
        with open(path, "r") as stream:
            file = stream.read()
        
        variables = re.findall(r"export let (.*?);", file)
        
        params = []
        for variable in variables:
            if "=" in variable:
                name = variable.split("=")[0]
                params.append(Parameter(name=name, kind=Parameter.KEYWORD_ONLY, default=None))
            else:
                params.append(Parameter(name=variable, kind=Parameter.KEYWORD_ONLY))
                
        return params
        


class SvelteComponent:
    def __init__(self, name: str):
        self.name = name
        src_path = utils.get_component_path(name)
        self.argument_handler = ArgumentHandler.infer_from_src_file(src_path)
        self.__signature__ = self.argument_handler.signature
        if self.argument_handler.docstring:
            self.__doc__ = self.argument_handler.docstring
    
    def __call__(self, **data) -> Html:
        data = self.argument_handler.validate_and_process_args(**data)
        return self.html(data)
    
    def __repr__(self):
        return f"<SvelteComponent {self.name}>"
    
    def html(self, data):
        element = self.name.lower()
        element_id = f"{self.name}-{hex(np.random.randint(10 ** 8))[2:16]}"
        attributes = [f"elem.setAttribute('{k}', '{v}');\n" for k, v in data.items()]
        
        html_str = f"""
        <{element}-element id='{element_id}' />
        
        <script>
            (() => {{
                elem = document.getElementById('{element_id}');
                {"".join(attributes)}
            }})();
        </script>
        """
        
        script_tags = [f"{self.name}.iife.js"]
        return Html(html_str, script_tags=script_tags)
        
    @staticmethod
    def autogenerate():
        components = []
        for src_path in config.SRC.rglob("*.svelte"):
            name = src_path.stem
            components.append(SvelteComponent(name))
        return components