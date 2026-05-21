import sweb
import re

HTML_END = "</html>"

class WebBuilder:
    def __init__(self, 
                 add_start = True, 
                 add_nav = True,
                 ):
        self.web = ""
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
        self.web += web_start

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
        self.web += nav_html
    
    def add_footer(self):
        start_year = sweb.data.copy_right_year[0]
        end_year = sweb.data.copy_right_year[-1]
        if start_year == end_year:
            year = start_year
        else:
            year = f"{start_year} - {end_year}"
        footer = f"""
<footer>
    <p>&copy; {year} SnehulakTV_</p>
</footer>
"""
        self.web += footer

    def add_head(self, text):
        header = f"""
<header>
    <h1>{text}</h1>
</header>
"""
        self.web += header
        
    
    def add_text(self, text: str):
        """
        add text to web.

        use ::link(example.com): example::link:: to add link
        """
        link_pattern = r"::link\((.*?)\):\s*(.*?)::link::"
        
        safe_text = re.sub(link_pattern, r'<a href="\1">\2</a>', text)
        
        self.web += safe_text

    def build(self, add_footer = True):
        if add_footer: self.add_footer()
        self.web += "</body>" + HTML_END

    def get_web(self, print_web = False):
        if not self.web.endswith(HTML_END): self.web += HTML_END
        if print_web: print(self.web)
        return self.web

    def save_web(self, name: str):
        if not self.web.endswith(HTML_END): self.web += HTML_END
        sweb.save_html(name, self.web)


