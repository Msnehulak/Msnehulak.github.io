import webbuilder as wb
import sweb

def projects_page():
    text = sweb.data.texts["projects"]
    bld = wb.WebBuilder()
    bld.add_head(text["head"])

    abutf = wb.Frame()
    abutf.add_markdown(text["text"])
    abutf.move_main()
    bld.add_html(abutf.get_frame()) 

    bld.build()
    bld.save_web("projects")
    print("projects web is saved")

def home_page():
    text = sweb.data.texts["home_page"]
    bld = wb.WebBuilder()
    bld.add_head(text["head"])

    abutf = wb.Frame()
    abutf.add_markdown(text["text"])
    abutf.move_main()
    bld.add_html(abutf.get_frame()) 

    bld.build()
    bld.save_web("index")

projects_page()
home_page()




