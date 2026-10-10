from pysvelte import utils


class Html:
    def __init__(self, chunks, script_tags, title=None, description=None):
        self.chunks = [chunks]
        self.script_tags = script_tags
        self.title = title
        self.description = description
        
    def __repr__(self):
        return self.html_str()
        
    def html_str(self):
        return "\n".join(self.chunks)
        
    def inline_html_str(self):
        return f"""
        {self.get_script_tags()}
        {self.html_str()}
        """
    
    def _repr_html_(self):
        return self.inline_html_str()
        
    def get_script_tags(self):
        return "\n".join([utils.get_script_tag(tag) for tag in self.script_tags])
    
    def show(self):
        try:
            from IPython.display import display

            return display(self)
        except ImportError:
            return self.html_str()