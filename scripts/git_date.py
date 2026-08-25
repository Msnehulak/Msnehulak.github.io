import subprocess
from typing import Dict, Optional


def get_git_metadata(file_path: Optional[str] = None) -> Dict[str, str]:
    """Vrátí ISO řetězce pro datum vytvoření a datum poslední úpravy z Git logu.

    :param file_path: Volitelná cesta ke konkrétnímu souboru. Pokud je None,
    vrátí data pro celý repozitář.
    """
    cmd_last = ["git", "log", "-1", "--format=%at", "--date=iso-strict"]
    cmd_first = ["git", "log", "--format=%at", "--date=iso-strict"]

    if file_path:
        cmd_last.extend(["--", file_path])
        cmd_first.extend(["--follow", "--", file_path])

    try:
        # Poslední úprava (nejnovější commit)
        last_modified = subprocess.check_output(cmd_last, text=True).strip()

        # Vytvoření (nejstarší/první commit)
        all_commits = subprocess.check_output(cmd_first, text=True).strip()
        created_at = all_commits.splitlines()[-1] if all_commits else last_modified

        return {"created_at": created_at, "last_modified_at": last_modified}
    except subprocess.CalledProcessError as e:
        return {"error": f"Git příkaz selhal: {e}"}
    except FileNotFoundError:
        return {"error": "Git není v systému nainstalován nebo dostupný."}


if __name__ == "__main__":
    file_meta = get_git_metadata("content/index/cs.md")
    print(file_meta)
