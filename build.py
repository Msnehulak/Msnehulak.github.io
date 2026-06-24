import subprocess
from pathlib import Path
from code.osu import Osu

def build_website():
    # 1. Spustíme osu worker, který zkontroluje expiraci cache a případně stáhne nová data
    osu_app = Osu()
    osu_app.load_data() # Toto interně zavolá sweb.cache.get a případný _update()

    # 2. Načteme aktuální data z cache pro vložení do stránky
    data = osu_app.data

    if data:
        # Vytvoříme přehledný seznam/tabulku v Markdownu
        md_content = f"""
- **Rank:** #{data.get('rank', 'N/A')}
- **PP:** {data.get('pp', 'N/A')}
- **Přesnost:** {data.get('acc', 0):.2f}%
- **Obrázek:** ![Avatar]({data.get('avatar', '')})
"""
    else:
        md_content = "Data se nepodařilo načíst."

    # 3. Přečteme šablonu, nahradíme placeholder a uložíme finální verzi pro Pelican
    template_path = Path("content/osu.md.template") # Přejmenuj původní osu.md na .template
    output_path = Path("content/osu.md")

    if template_path.exists():
        text = template_path.read_text(encoding="utf-8")
        final_text = text.replace("{OSU_DATA}", md_content)
        output_path.write_text(final_text, encoding="utf-8")

    # 4. Spustíme Pelican build
    print("Spouštím Pelican build...")
    subprocess.run(["pelican", "content", "-s", "pelicanconf.py"])

if __name__ == "__main__":
    build_website()
