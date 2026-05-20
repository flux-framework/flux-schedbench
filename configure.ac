#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.63])
AC_INIT([flux-schedbench],
        m4_esyscmd_s([git describe --always 2>/dev/null | sed 's/^v//' | grep . || echo 0.1.0]))
AC_CONFIG_AUX_DIR([config])
AC_CONFIG_MACRO_DIR([config])
AC_CONFIG_SRCDIR([configure.ac])

AM_INIT_AUTOMAKE([subdir-objects tar-ustar filename-length-max=256 foreign])
AM_SILENT_RULES([yes])
AM_MAINTAINER_MODE([enable])

# flux-schedbench is Python-only: no C compiler needed.

AC_PREFIX_PROGRAM([flux])

PKG_PROG_PKG_CONFIG

AX_FLUX_CORE

# Use the same Python version as flux-core.
PYTHON_VERSION=${PYTHON_VERSION:-$FLUX_PYTHON_VERSION}
AM_PATH_PYTHON([$PYTHON_VERSION])
if test "X$PYTHON" = "X"; then
  AC_MSG_ERROR([could not find python])
fi

# Compute the installed site-packages directory so tests can add it
# to PYTHONPATH without hardcoding a path suffix.
PYTHON_SITE_PACKAGES=$($PYTHON -c \
  "import sysconfig; print(sysconfig.get_path('platlib'))")
AC_SUBST([PYTHON_SITE_PACKAGES])

#
# Install directories.
#
# fluxpydir:  where flux.* Python packages are installed.
#             Matches flux-core's choice: ${pyexecdir}/flux.
# fluxcmddir: where flux sub-commands (flux-schedbench) are installed.
#
AS_VAR_SET([fluxpydir], [$pyexecdir/flux])
AC_SUBST([fluxpydir])

AS_VAR_SET([fluxcmddir], [$libexecdir/flux/cmd])
AC_SUBST([fluxcmddir])

# Optional Sphinx documentation.
AS_IF([test "x$enable_docs" != "xno"], [
  AM_CHECK_PYMOD(sphinx,
    [Version(sphinx.__version__) >= Version('1.6.7')],
    [sphinx=true],
    [sphinx=false;
     AC_MSG_WARN([sphinx >= 1.6.7 not found; man pages will not be built])])
  AM_CHECK_PYMOD(docutils,
    [Version(docutils.__version__) >= Version('0.11.0')],
    [docutils=true],
    [docutils=false;
     AC_MSG_WARN([docutils not found; man pages will not be built])])
])
AS_IF([test "x$enable_docs" = "xyes" -a "x$sphinx" = "xfalse"],
  [AC_MSG_ERROR([--enable-docs requires sphinx >= 1.6.7])])
AS_IF([test "x$enable_docs" = "xyes" -a "x$docutils" = "xfalse"],
  [AC_MSG_ERROR([--enable-docs requires docutils])])
AM_CONDITIONAL([ENABLE_DOCS],
  [test "x$sphinx" = "xtrue" -a "x$docutils" = "xtrue"])
AC_CHECK_PROG([ASPELL], [aspell], [aspell])

AC_CONFIG_FILES([
  Makefile
  src/Makefile
  src/cmd/Makefile
  src/bindings/Makefile
  src/bindings/python/Makefile
  src/bindings/python/flux/Makefile
  t/Makefile
])
AC_OUTPUT

echo "
  $PACKAGE_NAME version $PACKAGE_VERSION
  Prefix............: $prefix
  FLUX..............: $FLUX
  FLUX_PREFIX.......: $FLUX_PREFIX
  FLUX_PYTHON.......: $FLUX_PYTHON_VERSION
  PYTHON............: $PYTHON ($PYTHON_VERSION)
  fluxpydir.........: $(eval echo $fluxpydir)
  fluxcmddir........: $(eval echo $fluxcmddir)
"
