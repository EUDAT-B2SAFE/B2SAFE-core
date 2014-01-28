ifndef buildDir
buildDir = /lat/irods
endif

include $(buildDir)/config/config.mk
include $(buildDir)/config/platform.mk
include $(buildDir)/config/directories.mk
include $(buildDir)/config/common.mk

#
# Directories
#
MSBaseDir =		$(modulesDir)/BE2SAFE
MSObjDir =		$(MSBaseDir)/microservices/obj
MSSrcDir =		$(MSBaseDir)/microservices/src
MSIncDir =		$(MSBaseDir)/microservices/include
MSLibDir =		$(MSBaseDir)/microservices/lib

#
# Objects to compile
#
EUDAT_OBJECTS = $(MSObjDir)/eudat.o

#bundle objects
OBJECTS =  $(EUDAT_OBJECTS)

#compile and linker flags
INCLUDE_FLAGS =	-I$(MSIncDir)

INCLUDES +=	$(INCLUDE_FLAGS) $(LIB_INCLUDES) $(SVR_INCLUDES)
CFLAGS_OPTIONS := -DRODS_SERVER $(CFLAGS) $(MY_CFLAG)
CFLAGS =	$(CFLAGS_OPTIONS) $(INCLUDES) $(MODULE_CFLAGS)

.PHONY: all rules microservices server client clean
.PHONY: server_ldflags client_ldflags server_cflags client_cflags
.PHONY: print_cflags

.PHONY: all rules microservices server client clean
.PHONY: server_ldflags client_ldflags server_cflags client_cflags
.PHONY: print_cflags

# Build everything
all:	microservices
	@true

# List module's objects for inclusion in the clients
client_ldflags:
	@true

# List module's includes for inclusion in the clients
client_cflags:
	@true

# List module's objects for inclusion in the server
server_ldflags:
	@echo $(OBJECTS) $(LIBS)

# List module's includes for inclusion in the server
server_cflags:
	@echo $(INCLUDE_FLAGS)

# Build microservices
microservices:	print_cflags $(OBJECTS)
	@true

# Build client additions
client:
	@true

# Build server additions
server:
	@true

# Build rules
rules:
	@true

# Clean
clean:
	@echo "Clean MPI web services module..."
	@rm -f $(OBJECTS)

# Show compile flags
print_cflags:
	@echo "Compile flags:"
	@echo "    CC: $(CC)"
	@echo "    CFLAGS: $(CFLAGS)"
	@echo "    CFLAGS_OPTIONS: $(CFLAGS_OPTIONS)"
	@echo ""
	@echo "Linker flag:"
	@echo "	    $(OBJECTS) $(LIBS)"
	@echo ""

#
# Compilation targets
#
$(EUDAT_OBJECTS): $(MSObjDir)/%.o: $(MSSrcDir)/%.c $(DEPEND)
	@echo "Compile webservices-common module `basename $@`..."
	@$(CC) -c $(CFLAGS) -o $@ $<
