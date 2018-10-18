#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.
#
# Use the following command to create Makefile for mingw32
# and to build for windows platform
#
# $ mkdir ../build ; cd ../build
# $ ../src/configure --host=i686-pc-mingw32 \
#                    --with-libintl-prefix=/usr/local/mingw
# $ make SPECIESE_NAME=human
#

AC_PREREQ([2.60])
AC_INIT([parser], [1.0.1], [jondy.zhao@gmail.com])
AC_CONFIG_SRCDIR([config.h.in])
AC_CONFIG_AUX_DIR([build-aux])
AC_CONFIG_MACRO_DIR([build-aux/m4])
AC_CONFIG_HEADERS([config.h])

dnl Set some variables
AC_SUBST([PYTHON_VERSION], [2.6])

dnl Cross Compiler
AC_CANONICAL_SYSTEM

case $host in
       *-*-mingw32)
           CC="gcc-3"
	   CFLAGS="-mno-cygwin -g -O2"
	   YFLAGS="-d"
           ;;       
       *-*-cygwin)
           CFLAGS="-g -O2"
	   YFLAGS="-d"
           ;;
       i?86-pc-linux*)
           CFLAGS="-g -O2"
	   YFLAGS="-d"
           ;;
esac

dnl Init automake
AM_INIT_AUTOMAKE

AM_GNU_GETTEXT([external])
BISON_I18N

# Checks for programs.
AC_PROG_CC
AC_C_INLINE

AC_PROG_YACC
AC_PROG_LEX

# Checks for header files.

# Checks for typedefs, structures, and compiler characteristics.

# Checks for library functions.
AC_CHECK_FUNCS([asprintf])
AM_CONDITIONAL([NEEDLIBIBERTY], [test x$ac_cv_func_asprintf = xno])

AC_CONFIG_FILES([Makefile po/Makefile.in])
AC_OUTPUT
