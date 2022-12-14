from jinja2 import Template


class JinjaTemplate:
    # Classe para redenrização de template

    @staticmethod
    def template(root_path: str, datas=None, totais=None) -> str:
        # método para renderizar o template
        # method to render the template
        with open(root_path, "rb") as html:
            template = Template(html.read().decode("UTF-8"))
            message_body = template.render(datas=datas, totais=totais)
            return message_body
