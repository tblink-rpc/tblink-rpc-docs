# Build the pyvsc documentation
#
# Note: this Makefile is *not* used by Read The Docs, it exec()'s the conf.py
# file directly. Hence, all special build steps here are only relevant for
# local builds, not for RTD builds. Add all build steps which should be executed
# in RTD builds as Python code into the conf.py file.

DOC_DIR:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PACKAGES_DIR:=$(abspath $(DOC_DIR)/../packages)

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = .venv.bld/bin/sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help: .venv.bld
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: clean
clean: Makefile
	@$(PACKAGES_DIR)/python/bin/sphinx-build -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: distclean
distclean:
	-rm -rf .venv* build sphinxext/__pycache__

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
.DEFAULT:
# Dependencies for this special target are ignored by make, as discussed in
# http://stackoverflow.com/questions/26875072/dependencies-for-special-make-target-default-not-firing
# We hack around that by calling the target explicitly.
	$(PACKAGES_DIR)/python/bin/sphinx-build -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
