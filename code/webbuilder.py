import sweb
import re
import markdown

HTML_END = "</html>"

class WebBuilder:
    def __init__(self, 
                 add_start = True, 
                 add_nav = True,
                 ):
        self.content = ""
        if add_start: self.add_start()
        if add_nav: self.add_nav()

    def add_start(self, 
                  lang = "cs", 
                  title = "title", 
                  load_css = True, 
                  redirect = ""):
        if load_css:
            css = '<link rel="stylesheet" href="style.css">'
        else: css = ''

        if redirect == "": r = ""
        else:
            r = f'<meta http-equiv="refresh" content="0; url={redirect}">'
        
        web_start = f"""<!DOCTYPE html>
<html lang={lang}>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {css}
    {r}
</head>
<body>
"""
        self.content += web_start

    def add_nav(self):
        data = sweb.load_json("nav")
    
        links = ""
        for i in data["links"]:
            links += f'        <a href="{i["link"]}">{i["name"]}</a>\n'

        nav_html = f"""
<nav>
    <div class="logo">{data["logo"]["text"]}</div>
    <div class="odkazy">
{links}    </div>
</nav>
"""
        self.content += nav_html
    
    def add_footer(self):
        start_year = sweb.data.copy_right_year[0]
        end_year = sweb.data.copy_right_year[-1]
        if start_year == end_year:
            year = start_year
        else:
            year = f"{start_year} - {end_year}"
        footer = f"""
<footer>
    <p>&copy; {year} SnehulakTV</p>
</footer>
"""
        self.content += footer

    def add_head(self, text):
        header = f"""
<header>
    <h1>{text}</h1>
</header>
"""
        self.content += header
            
    def add_html(self, html):
        self.content += html

    def add_markdown(self, md):
        html = markdown.markdown(md)
        self.content += html

    def build(self, add_footer = True):
        if add_footer: self.add_footer()
        self.content += "</body>" + HTML_END

    def get_web(self, print_web = False):
        if not self.content.endswith(HTML_END): self.content += HTML_END
        if print_web: print(self.content)
        return self.content

    def save_web(self, name: str):
        if not self.content.endswith(HTML_END): self.content += HTML_END
        sweb.save_html(name, self.content)

class Frame:
    def __init__(self) -> None:
        self.content = '<section class="karta">'
        self.html_oc = {
                "main": [0, 0],
                "section": [1, 0]
        }

        self.WB = WebBuilder()
 
    def add_markdown(self, md):
        html = markdown.markdown(md)
        self.content += html
 
    def move_main(self):
        self.html_oc["main"][0] = 1
        self.content = "<main>" + self.content

    def _chck_close_html(self):
        i = self.html_oc
        if not i["section"][0] == i["section"][1]:
            self.content += "</section>"
        if not i["main"][0] == i["main"][1]:
            self.content += "</main>"

    def get_frame(self, print_frame = False):
        self._chck_close_html()
        if print_frame: print(self.content)
        return self.content


