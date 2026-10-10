from pathlib import Path

from pysvelte import utils


class Html:
    def __init__(self, chunks, script_paths, title=None, description=None):
        self.chunks = [chunks]
        self.script_paths = script_paths
        self.title = title
        self.description = description
        
    def __repr__(self):
        return self.html_str()
        
    def html_str(self):
        return "\n".join(self.chunks)
        
    def inline_html_str(self):
        return f"""
        {utils.get_script_tags(self.script_paths)}
        {self.html_str()}
        """
    
    def _repr_html_(self):
        return self.inline_html_str()
        
    # def get_script_tags(self, dev_mode=False):
    #     return "\n".join([utils.get_script_tag(tag, dev_mode) for tag in self.script_paths])
    
    def show(self):
        try:
            from IPython.display import display

            return display(self)
        except ImportError:
            return self.html_str()
        
    def save(self, path: Path | str, dev_mode=False):
        path = Path(path) if isinstance(path, str) else path
        path.parent.mkdir(exist_ok=True, parents=True)
        
        with open(path, "w") as file:
            file.write(
                f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Document</title>
                </head>
                <body>
                    {self.get_script_tags(dev_mode=dev_mode)}

                    {self.html_str()}
                </body>
                </html>
                """
            )