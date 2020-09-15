MAKE             = /usr/bin/make
RST2HTML         = ./bootstrap.py
STYLESHEET       =
RST2HTML_OPTIONS = --strip-comments             \
                   --report=3                   \
                   --no-doc-title               \
                   --traceback                  \
                   --compact-lists              \
                   --no-toc-backlinks           \
                   --syntax-highlight=short     \
                   --template=page.tmpl         \
                   --cloak-email-addresses      \
                   --stylesheet=$(STYLESHEET)   \
                   --link-stylesheet

SOURCES = $(wildcard doc/*.rst)
TMP = $(subst .rst,.html, $(SOURCES))
OBJECTS = $(subst doc/,, $(TMP))

all:$(OBJECTS)

%.html: doc/%.rst
	@echo "  - $@"
	@$(RST2HTML) $(RST2HTML_OPTIONS) $< $@

clean:
	@-rm -f $(OBJECTS)

distclean: clean
	@-rm -f `find . -name "*~"`

.PHONY: all clean distclean
