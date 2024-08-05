# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SPHINXMULTIVERSION ?= sphinx-multiversion
SOURCEDIR     = .
BUILDDIR      = _build
WEB_DOCS_BUILDER_URL ?= https://ai.b-bug.org/~huangziyi/web-docs-builder
WEB_DOCS_BUILDER_USER ?= gitlab+deploy-token-8
WEB_DOCS_BUILDER_TOKEN ?= _qsc99tPFsbcBhSbXH4S

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile _templates/versions.html  _static/topbar.css _static/custom.css
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

mhtml: Makefile _templates/versions.html  _static/topbar.css _static/custom.css
	@$(SPHINXMULTIVERSION) "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

_templates:
	mkdir $@

_templates/versions.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_static/topbar.css:
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_static/custom.css:
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@