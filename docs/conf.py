"""Sphinx configuration for Hutool-Python documentation."""

import os
import sys

# -- Path setup ---------------------------------------------------------------
# Add project root to sys.path so autodoc2 can import hutool
sys.path.insert(0, os.path.abspath(".."))

# -- Project information ------------------------------------------------------
project = "Hutool-Python"
copyright = "2026, Hutool-Python"
author = "Hutool-Python"
release = "1.1.1"
language = "zh_CN"

# -- General configuration ----------------------------------------------------
extensions = [
    "myst_parser",
    "autodoc2",
    "sphinx_copybutton",
    "sphinx_design",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "module.md"]

# -- MyST configuration -------------------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "substitution",
    "tasklist",
]

# -- autodoc2 configuration ---------------------------------------------------
autodoc2_packages = [
    {
        "path": "../hutool",
        "module": "hutool",
    },
]
autodoc2_render_module = True
autodoc2_module_template = "module.md"

# -- Options for HTML output ---------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = "Hutool-Python"
html_theme_options = {
    "source_repository": "https://github.com/wgp520/hutool-python",
    "source_branch": "master",
    "source_directory": "docs/",
    "navigation_with_keys": True,
}

# -- Options for copybutton ---------------------------------------------------
copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True
