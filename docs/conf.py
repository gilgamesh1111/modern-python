"""Sphinx configuration."""

theme="sphinx_rtd_theme"
project = "modern_python"
author = "Gilgamesh"
copyright = f"2025, {author}"
language = "zh_CN"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "myst_parser",
    "sphinx_rtd_theme",]

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    'collapse_navigation': False,
}

root_doc = "index"
latex_documents = [
    (root_doc, f"{project}.tex", f"{project} Documentation", author, "howto"),
]
