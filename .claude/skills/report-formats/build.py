"""テンプレートを組み立てる。

共通部品（assets/）と各テンプレートの本文（templates/*.body.html）から、
1ファイルで完結するHTMLテンプレートを作る。部品を直したら、これを実行して全テンプレートに反映する。

    python3 .claude/skills/report-formats/build.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
TPL = HERE / "templates"

HEAD = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
<style>
{css}</style>
</head>
"""

# (本文, 出力先, タイトル)
TARGETS = [
    ("strategy-brief.body.html", [TPL / "strategy-brief.html", HERE.parent / "strategy-brief" / "template.html"],
     "{{タイトル}}（戦略ブリーフ）"),
    ("prfaq.body.html", [TPL / "prfaq.html"], "{{構想の名前}}（PR/FAQ）"),
    ("adr.body.html", [TPL / "adr.html"], "{{プロジェクト名}} 決定記録"),
]


def main() -> None:
    css = (ASSETS / "base.css").read_text(encoding="utf-8") + (ASSETS / "components.css").read_text(encoding="utf-8")
    js = (ASSETS / "onepager.js.part").read_text(encoding="utf-8") + "\n" + (ASSETS / "components.js.part").read_text(encoding="utf-8")
    for body_name, outs, title in TARGETS:
        body = (TPL / body_name).read_text(encoding="utf-8").rstrip()
        html = HEAD.format(title=title, css=css) + body + "\n" + js + "\n</body>\n</html>\n"
        for out in outs:
            out.write_text(html, encoding="utf-8")
            print(f"wrote {out.relative_to(HERE.parent.parent.parent)} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
