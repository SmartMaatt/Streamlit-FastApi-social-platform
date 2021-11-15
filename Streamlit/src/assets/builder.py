def read_file(file_path: str):
    with open(file_path) as f:
        return f.read()


def generate_html_obj(content: str, tag: str):
    return '\n<' + tag + '>\n' + content + '\n</' + tag + '>\n'


class Builder:
    def __init__(self, styles_path: str, styles: list, scripts_path: str, scripts: list):
        self.styles = [styles_path + style for style in styles]
        self.scripts = [scripts_path + script for script in scripts]

    @property
    def generate_style_component(self):
        component_source = ""
        for style in self.styles:
            component_source += generate_html_obj(read_file(style), 'style')
        return component_source

    @property
    def generate_script_component(self):
        component_source = ""
        for script in self.scripts:
            component_source += generate_html_obj(read_file(script), 'script')
        return component_source
