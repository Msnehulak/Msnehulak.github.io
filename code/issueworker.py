import sys
import sweb
import os
import json
import build
import redirect as rd

class IssueWorker:
    def __init__(self):
        self.form_type = None
        self.app_rd = rd.Redirect()

    def find_form_type(self):
        required_keys = ["Name of redirect", "Web link", "Redirect"]
        if all(key in self.body for key in required_keys):
            self.form_type = "add_redirect"

    def main(self):
        raw_env = os.environ.get("ISSUE_JSON", "")
        
        try: 
            self.body = json.loads(raw_env)
        except json.JSONDecodeError:
            print("Chyba: ISSUE_JSON neobsahuje validní JSON.")
            sys.exit(1)
        
        self.find_form_type()
        if self.form_type is None:
            print("invalid format")
            sys.exit(1)

        if self.form_type == "add_redirect":
            link = self.body["Web link"]
            name = self.body["Name of redirect"]
            r = self.body["Redirect"]
            self.app_rd.add_redirect(link=link, name=name, r=r)
            build.build()

if __name__ == "__main__":
    if "ISSUE_JSON" in os.environ:
        app = IssueWorker()
        app.main()
    else:
        sweb.log_error("No ISSUE BODY!!")


