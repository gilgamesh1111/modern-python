"""Sphinx configuration."""

theme = "sphinx_rtd_theme"
project = "modern_python"
author = "Gilgamesh"
copyright = f"2025, {author}"
language = "zh_CN"
extensions = [
    "myst_parser",
    "sphinx_rtd_theme",
    "autodoc2",
]

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "collapse_navigation": False,
}

root_doc = "index"
latex_documents = [
    (root_doc, f"{project}.tex", f"{project} Documentation", author, "howto"),
]

autodoc2_packages = [
    {
        "path": "../src/modern_python",  # 从 conf.py 到您的包的相对路径
        "auto_mode": True,
    },
]
