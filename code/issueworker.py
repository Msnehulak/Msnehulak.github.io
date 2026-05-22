import sys
import sweb
import os
import re
import redirect as rd

class IssueWorker:
    def __init__(self):
        self.form_type = None
        self.app_rd = rd.Redirect()

    def find_form_type(self):
        i = self.row_body
        c = {
                "rn": i.count("### Name of redirect"),
                "wl": i.count("### Web link"),
                "r": i.count("### Redirect")
        }

        if c["rn"] == c["wl"] == c["r"] == 1:
            self.form_type = "add_redirect"

    def format_data(self):
        data = {}
        sections = re.split(r'###\s+', self.row_body)
        
        for section in sections:
            if not section.strip():
                continue
            lines = section.split('\n', 1)
            key = lines[0].strip().lower().replace(" ", "_")
            value = lines[1].strip() if len(lines) > 1 else ""
            data[key] = value.strip()
        
        self.body = data

    def main(self):
        self.row_body = os.environ["ISSUE_BODY"]
        
        self.find_form_type()
        if self.form_type is None:
            print("invalid format")
            sys.exit(1)
        self.format_data()

        if self.form_type == "add_redirect":
            link = self.body["web_link"]
            name = self.body["name_of_redirect"]
            r = self.body["redirect"]
            self.app_rd.add_redirect(link=link, name=name, r=r)
            self.app_rd.main()

if __name__ == "__main__":
    if "ISSUE_BODY" in os.environ:
        app = IssueWorker()
        app.main()
    else:
        sweb.log_error("No ISSUE BODY!!")
 

