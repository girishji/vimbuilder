"""Vim-help Sphinx builder."""

from __future__ import annotations

from datetime import datetime
from os import path
from pathlib import Path
from re import sub
from typing import TYPE_CHECKING, Any

from docutils import nodes
from docutils.utils import column_width

from sphinx.addnodes import desc_signature
from sphinx.builders.text import TextBuilder
from sphinx.locale import __
from sphinx.util import logging
from sphinx.writers.text import TextTranslator, STDINDENT, MAXWIDTH

if TYPE_CHECKING:
    from docutils.nodes import Element
    from docutils.nodes import Node
    from sphinx.application import Sphinx

logger = logging.getLogger(__name__)

class VimHelpTranslator(TextTranslator):
    "Custom docutils/sphinx translator for vim help files"

    def __init__(self, document: nodes.document, builder: TextBuilder) -> None:
        super().__init__(document, builder)
        self.tag_prefix = self.config.vimhelp_tag_prefix
        self.tag_suffix = self.config.vimhelp_tag_suffix
        self.format_desc = self.config.vimhelp_format_desc
        self.tag_filename = self.config.vimhelp_tag_filename
        self.filename_suffix = self.config.vimhelp_filename_suffix

    def add_text_nonl(self, text: str):
        # Each 'state' item is a list of (indent, str | lines)
        if self.states[-1] and self.states[-1][-1]:
            ilevel, lines = self.states[-1][-1]
            if type(lines) is list and not lines[-1]: # empty line
                lines.pop()
            self.states[-1].append((-sum(self.stateindent), text))

    def visit_literal_block(self, node: Element) -> None:
        self.add_text_nonl('>')
        super().visit_literal_block(node)

    def depart_literal_block(self, node: Element) -> None:
        super().depart_literal_block(node)
        self.add_text_nonl('<')

    def visit_inline(self, node: Element) -> None:
        if 'xref' in node['classes'] or 'term' in node['classes']:
            self.add_text('_')

    def depart_inline(self, node: Element) -> None:
        if 'xref' in node['classes'] or 'term' in node['classes']:
            self.add_text('_')

    def visit_emphasis(self, node: Element) -> None:
        self.add_text('_')

    def depart_emphasis(self, node: Element) -> None:
        self.add_text('_')

    def visit_literal_emphasis(self, node: Element) -> None:
        self.add_text('_')

    def depart_literal_emphasis(self, node: Element) -> None:
        self.add_text('_')

    def visit_title_reference(self, node: Element) -> None:
        self.add_text('_')

    def depart_title_reference(self, node: Element) -> None:
        self.add_text('_')

    def get_vim_tag(self, text: str) -> str:
        return f'*{self.tag_prefix}{text}{self.tag_suffix}*'

    def visit_document(self, node: Element) -> None:
        super().visit_document(node)
        fpath = self.document['source']
        assert fpath
        fname = Path(fpath).name.replace(' ', '_').split('.')
        if len(fname) > 1:
            fname.pop()
        self.filename = ''.join(fname) + '.txt' + self.filename_suffix
        tagname = self.get_vim_tag(self.filename)
        timestamp = 'Last change: ' + datetime.today().strftime('%Y %b %d')
        spaces = ' ' * max(MAXWIDTH - len(tagname) - len(timestamp), 2)
        self.states[0].append((0, [tagname + spaces + timestamp, '']))

    def depart_document(self, node: Element) -> None:
        super().depart_document(node)
        footer = 'vim:tw=78:ts=8:ft=help:norl:'
        self.body += self.nl + footer

    def extract_tag(self, text: str) -> str:
        return re.sub(r'\(.*\)?', '()', text).replace(' ', '_')

    def visit_desc(self, node: Element) -> None:
        desc = node[node.first_child_matching_class(desc_signature)]
        assert desc
        if self.format_desc:
            dtype = node['desctype'] if node.hasattr('desctype') else ''
            formatted = self.format_desc(desc.astext(), dtype)
        elif desc.hasattr('_toc_name'):
            formatted = desc['_toc_name'].replace(' ', '_')
        else:
            formatted = self.extract_tag(desc.astext())
        if self.tag_filename:
            formatted += f'..{self.filename}'
        self.add_text_nonl(['', ' ' * (MAXWIDTH - len(formatted) - 2) + self.get_vim_tag(formatted)])


class VimHelpBuilder(TextBuilder):
    name = 'vimhelp'
    format = 'text'
    epilog = __('The vim help files are in %(outdir)s.')

    out_suffix = '.txt'
    allow_parallel = True
    default_translator_class = VimHelpTranslator

def setup(app: Sphinx) -> dict[str, Any]:
    app.add_builder(VimHelpBuilder)

    app.add_config_value('vimhelp_tag_prefix', '', 'env')
    app.add_config_value('vimhelp_tag_suffix', '', 'env')
    app.add_config_value('vimhelp_format_desc', None, 'env')
    app.add_config_value('vimhelp_tag_filename', True, 'env')
    app.add_config_value('vimhelp_filename_suffix', ';', 'env')

    return {
        'version': 'builtin',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
