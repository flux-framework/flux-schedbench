###############################################################
# Copyright 2020 Lawrence Livermore National Security, LLC
# (c.f. AUTHORS, NOTICE.LLNS, COPYING)
#
# This file is part of the Flux resource manager framework.
# For details, see https://github.com/flux-framework.
#
# SPDX-License-Identifier: LGPL-3.0
###############################################################

# Configuration file for the Sphinx documentation builder.
#
# For a full list of options see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import pathlib
import sys

import docutils.nodes
from sphinx.domains import Domain

sys.path.append(str(pathlib.Path(__file__).absolute().parent))

from manpages import man_pages

_FLUX_CORE_BASE = (
    'https://flux-framework.readthedocs.io/projects/flux-core/en/latest'
)


def _core_man_role(section):
    def role_fn(name, rawtext, text, lineno, inliner, options={}, content=[]):
        node = docutils.nodes.reference(
            rawsource=rawtext,
            text=f'{text}({section})',
            refuri=f'{_FLUX_CORE_BASE}/man{section}/{text}.html',
            **options,
        )
        return [node], []
    return role_fn


class CoreDomain(Domain):
    """Sphinx domain for cross-referencing flux-core man pages."""
    name = 'core'
    label = 'Flux Core'
    roles = {f'man{s}': _core_man_role(s) for s in [1, 3, 5, 7]}

# -- Project information -----------------------------------------------------

project = 'flux-schedbench'
copyright = '''Copyright 2026 Lawrence Livermore National Security, LLC and Flux developers.

SPDX-License-Identifier: LGPL-3.0'''

# -- General configuration ---------------------------------------------------

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

master_doc = 'index'
source_suffix = '.rst'

extensions = [
    'domainrefs',
]

domainrefs = {
    'rfc': {
        'text': 'RFC %s',
        'url': 'https://flux-framework.readthedocs.io/projects/flux-rfc/en/latest/spec_%s.html'
    },
    'linux:man1': {
        'text': '%s(1)',
        'url': 'http://man7.org/linux/man-pages/man1/%s.1.html'
    },
    'linux:man2': {
        'text': '%s(2)',
        'url': 'http://man7.org/linux/man-pages/man2/%s.2.html'
    },
    'linux:man3': {
        'text': '%s(3)',
        'url': 'http://man7.org/linux/man-pages/man3/%s.3.html'
    },
    'linux:man5': {
        'text': '%s(5)',
        'url': 'http://man7.org/linux/man-pages/man5/%s.5.html'
    },
    'linux:man7': {
        'text': '%s(7)',
        'url': 'http://man7.org/linux/man-pages/man7/%s.7.html'
    },
    'linux:man8': {
        'text': '%s(8)',
        'url': 'http://man7.org/linux/man-pages/man8/%s.8.html'
    },
    'security:man3': {
        'text': '%s(3)',
        'url': 'https://flux-framework.readthedocs.io/projects/flux-security/en/latest/man3/%s.html'
    },
    'security:man5': {
        'text': '%s(5)',
        'url': 'https://flux-framework.readthedocs.io/projects/flux-security/en/latest/man5/%s.html'
    },
    'security:man8': {
        'text': '%s(8)',
        'url': 'https://flux-framework.readthedocs.io/projects/flux-security/en/latest/man8/%s.html'
    },
}

# Disable "smartquotes" to avoid things like turning "--" into an en-dash
# in HTML output, which makes no sense for man page options.
smartquotes = False


def man_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for cross-references to man pages local to this project."""
    section = int(name[-1])
    page = None
    for man in man_pages:
        if man[1] == text and man[4] == section:
            page = man[0]
            break
    if page is None:
        inliner.reporter.warning(
            f'unknown local man page: {text}({section})'
            f' (use :core:man{section}: for flux-core pages)',
            line=lineno,
        )
        node = docutils.nodes.literal(rawsource=rawtext, text=f'{text}({section})')
        return [node], []
    node = docutils.nodes.reference(
        rawsource=rawtext,
        text=f'{text}({section})',
        refuri=f'../{page}.html',
        **options,
    )
    return [node], []


def setup(app):
    app.add_domain(CoreDomain)
    for section in [1]:
        app.add_role(f'man{section}', man_role)


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
