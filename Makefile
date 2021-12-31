
TBLINK_RPC_DOCS_DIR:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ifeq (,$(PACKAGES_DIR))
  PACKAGES_DIR := $(TBLINK_RPC_DOCS_DIR)/packages
endif

export PACKAGES_DIR

html :
	doxygen $(TBLINK_RPC_DOCS_DIR)/doc/TbLinkRPC.conf
	DOXYDOCS_DIR=`pwd`/doxydocs \
		$(PACKAGES_DIR)/python/bin/sphinx-build -M html \
			$(TBLINK_RPC_DOCS_DIR)/doc/source \
			build
