
TBLINK_RPC_DOCS_DIR:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ifeq (,$(PACKAGES_DIR))
  PACKAGES_DIR := $(TBLINK_RPC_DOCS_DIR)/packages
endif

export PACKAGES_DIR

pdf : doxydocs_cpp doxydocs_sv
	DOXYDOCS_DIR_CPP=`pwd`/doxydocs_cpp \
	DOXYDOCS_DIR_SV=`pwd`/doxydocs_sv \
		$(PACKAGES_DIR)/python/bin/sphinx-build -M latexpdf \
			$(TBLINK_RPC_DOCS_DIR)/doc/source \
			build

html : doxydocs_cpp doxydocs_sv
	DOXYDOCS_DIR_CPP=`pwd`/doxydocs_cpp \
	DOXYDOCS_DIR_SV=`pwd`/doxydocs_sv \
		$(PACKAGES_DIR)/python/bin/sphinx-build -M html \
			$(TBLINK_RPC_DOCS_DIR)/doc/source \
			build

doxydocs_cpp : 
	doxygen $(TBLINK_RPC_DOCS_DIR)/doc/TbLinkRpcCpp.conf

doxydocs_sv : 
	rm -rf tblink_rpc_sv_tmp
	mkdir tblink_rpc_sv_tmp
	verilator -E -pp-comments +incdir+$(PACKAGES_DIR)/tblink-rpc-hdl/src/sv \
		$(PACKAGES_DIR)/tblink-rpc-hdl/src/sv/tblink_rpc.sv \
		> tblink_rpc_sv_tmp/tblink_rpc_pkg_1.sv
	perl $(PACKAGES_DIR)/sv-doxygen-filter/filter/idv_doxyfilter_sv.pl --package_mode \
		< tblink_rpc_sv_tmp/tblink_rpc_pkg_1.sv \
		> tblink_rpc_sv_tmp/tblink_rpc_pkg.cpp
	doxygen $(TBLINK_RPC_DOCS_DIR)/doc/TbLinkRpcSv.conf
	rm -rf tblink_rpc_sv_tmp

clean :
	rm -rf build

