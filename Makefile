
TOPDIR=$(CURDIR)
SRCDIR=$(TOPDIR)/congressclient

all: docs

clean: rm -Rf $(TOPDIR)/doc/html/*

docs: $(TOPDIR)/doc/source/*.rst
	sphinx-build -b html $(TOPDIR)/doc/source $(TOPDIR)/doc/html


