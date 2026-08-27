import logging
import subprocess
from datetime import datetime, timezone

from jinja2 import Template

from scripts import jija_content_vars, sweb

MAIN_LANG = sweb.site_lan


def get_git_metadata(file_path):
    cmd_last = ["git", "log", "-1", "--format=%at", "--date=iso-strict"]
    cmd_first = ["git", "log", "--format=%at", "--date=iso-strict"]

    if file_path:
        cmd_last.extend(["--", file_path])
        cmd_first.extend(["--follow", "--", file_path])

    try:
        last_modified = subprocess.check_output(cmd_last, text=True).strip()

        all_commits = subprocess.check_output(cmd_first, text=True).strip()
        created_at = all_commits.splitlines()[-1] if all_commits else last_modified

        return {"created_at": created_at, "last_modified_at": last_modified}
    except subprocess.CalledProcessError as e:
        return {"error": f"Git příkaz selhal: {e}"}
    except FileNotFoundError:
        return {"error": "Git není v systému nainstalován nebo dostupný."}


def fill_data_to_md(content_objekt):
    if hasattr(content_objekt, "_content") and content_objekt._content:
        if getattr(content_objekt, "_already_rendered_by_jinja", False):
            return

        logging.info(f"Editing Markdown: {content_objekt.source_path}")

        surovy_text = content_objekt._content

        sablona = Template(surovy_text)
        upraveny_text = sablona.render(**jija_content_vars.get_web_data())

        content_objekt._content = upraveny_text


def update_date(content_obj):
    page_path = content_obj.source_path
    metadata = get_git_metadata(page_path)
    last_update = metadata["last_modified_at"]
    create = metadata["created_at"]

    content_obj.modified_unix = last_update
    content_obj.date_unix = create

    content_obj.modified = datetime.fromtimestamp(int(last_update), tz=timezone.utc)
    content_obj.date = datetime.fromtimestamp(int(create), tz=timezone.utc)


def update_page(content_obj):
    update_date(content_obj)
    fill_data_to_md(content_obj)
