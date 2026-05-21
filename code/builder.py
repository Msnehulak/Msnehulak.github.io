import webbuilder as wb
import sweb


def home_page():
    text = sweb.data.texts["home_page"]
    bld = wb.WebBuilder()
    bld.add_head(text["head"])
    bld.add_footer()
    bld.get_web(print_web=True)

home_page()




