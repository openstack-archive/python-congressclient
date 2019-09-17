# -*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

sys.path.insert(0, os.path.abspath('../..'))
# -- General configuration ----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'openstackdocstheme',
    'sphinxcontrib.apidoc'
]

# openstackdocstheme options
repository_name = 'openstack/python-congressclient'
bug_project = 'python-congressclient'
bug_tag = ''

# sphinxcontrib.apidoc options
apidoc_module_dir = '../../congressclient'
apidoc_output_dir = 'reference/api'
apidoc_excluded_paths = ['tests/*']

apidoc_separate_modules = True

# Must set this variable to include year, month, day, hours, and minutes.
html_last_updated_fmt = '%Y-%m-%d %H:%M'

# autodoc generation is a bit aggressive and a nuisance when doing heavy
# text edit cycles.
# execute "export SPHINX_DEBUG=1" in your terminal to disable

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'python-congressclient'
copyright = u'2013, OpenStack Foundation'

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of glob-style patterns that should be excluded when looking for
# source files. They are matched against the source file names relative to the
# source directory, using slashes as directory separators on all platforms.
exclude_patterns = ['reference/api/congressclient.tests.*']

# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
# html_theme_path = ["."]
html_theme = 'openstackdocs'
# html_static_path = ['static']

# Output file base name for HTML help builder.
htmlhelp_basename = '%sdoc' % project

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = ['congressclient.']

# Disable usage of xindy https://bugzilla.redhat.com/show_bug.cgi?id=1643664
latex_use_xindy = False

latex_domain_indices = False

latex_elements = {
    'makeindex': '',
    'printindex': '',
    'preamble': r'\setcounter{tocdepth}{3}',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto/manual]).
# NOTE: Specify toctree_only=True for a better document structure of
# the generated PDF file.
latex_documents = [
    ('index',
     'doc-%s.tex' % project,
     u'Congress Client Documentation',
     u'OpenStack Foundation', 'manual', True),
]

# Example configuration for intersphinx: refer to the Python standard library.
#intersphinx_mapping = {'http://docs.python.org/': None}
