# 4.8 makes libpthread a hard requirement
# 4.7 has a heavier footprint
%define		db_version	4.6.21

%define		subver		pre1
%define		rel			11
Summary:	Berkeley DB Name Service Switch Module
Summary(pl.UTF-8):	Moduł NSS do baz db
Name:		nss_db
Version:	2.2.3
Release:	0.%{subver}.%{rel}
# DB is under the Sleepycat (Oracle) license.
# nss_db is under the LGPLv2+ license.
License:	Sleepycat and LGPL v2+
Group:		Base
Source0:	ftp://sources.redhat.com/pub/glibc/old-releases/%{name}-%{version}%{subver}.tar.gz
# Source0-md5:	b4440ba2865d28e9068e465426c19ede
Source1:	http://download.oracle.com/berkeley-db/db-%{db_version}.tar.gz
# Source1-md5:	718082e7e35fc48478a2334b0bc4cd11
Patch0:		%{name}-chmod_644.patch
Patch1:		%{name}-amfix.patch
Patch2:		%{name}-glibc23.patch
Patch3:		%{name}-db41.patch
Patch4:		%{name}-errno.patch
Patch5:		%{name}-link.patch
Patch6:		%{name}-enoent.patch
Patch7:		%{name}-uniqdb.patch
Patch8:		%{name}-initialize.patch
Patch9:		%{name}-selinux.patch
Patch10:	%{name}-makedb-atomic.patch
Patch101:	http://www.oracle.com/technology/products/berkeley-db/db/update/4.6.21/patch.4.6.21.1
Patch102:	http://www.oracle.com/technology/products/berkeley-db/db/update/4.6.21/patch.4.6.21.2
Patch103:	http://www.oracle.com/technology/products/berkeley-db/db/update/4.6.21/patch.4.6.21.3
Patch104:	http://www.oracle.com/technology/products/berkeley-db/db/update/4.6.21/patch.4.6.21.4
BuildRequires:	autoconf
BuildRequires:	automake >= 1.4
BuildRequires:	db-devel
# because of broken configure
BuildRequires:	gcc-c++
BuildRequires:	gettext-devel
BuildRequires:	glibc-devel >= 2.3
BuildRequires:	libselinux-devel
BuildRequires:	libtool
Requires:	glibc >= 6:2.3
Requires:	make
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# private symbols
%define		_noautoprov		.*\(GLIBC_PRIVATE\)
%define		_noautoreq		.*\(GLIBC_PRIVATE\)

%description
This is nss_db, a name service switch module that can be used with
glibc-2.2.x.

%description -l pl.UTF-8
To jest nss_db, moduł do serwisu nazw, który może być używany z
glibc-2.2.x.

%prep
%setup -q -n %{name}-%{version}%{subver} -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

mkdir db-build
cd db-%{db_version}
%patch101 -p0
%patch102 -p0
%patch103 -p0
%patch104 -p0

%build
dbdir=$(pwd)/db-instroot
cd db-build

CC="%{__cc}"
CXX="%{__cxx}"
CFLAGS="%{rpmcflags}"
CXXFLAGS="%{rpmcflags} -fno-implicit-templates"
LDFLAGS="%{rpmcflags} %{rpmldflags}"
export CC CXX CFLAGS CXXFLAGS LDFLAGS

echo db_cv_mutex=UNIX/fcntl > config.cache
../db-%{db_version}/dist/configure -C \
	--disable-compat185 \
	--disable-cxx \
	--disable-diagnostic \
	--disable-dump185 \
	--disable-java \
	--disable-rpc \
	--disable-tcl \
	--disable-shared \
	--disable-cryptography \
	--disable-hash \
	--disable-queue \
	--disable-replication \
	--disable-statistics \
	--disable-verify \
	--with-pic \
	--with-uniquename=_nssdb \
	--prefix=$dbdir \
	--libdir=$dbdir/lib
%{__make}
%{__make} install
cd ..

%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-db=${dbdir} \
	--with-selinux

%{__make} \
	slibdir=/%{_lib}

# Check for any problems, since we filter GLIBC_PRIVATE provs
# in glibc package and deps here
cat >> test-dlopen.c << _EOF
#include <dlfcn.h>
/* Simple program to see if dlopen() would succeed. */
int main(int argc, char **argv)
{
	if (dlopen(argv[1], RTLD_NOW))
		return 0;
	return 1;
}
_EOF

%{__cc} %{rpmcflags} -o test-dlopen test-dlopen.c -ldl

./test-dlopen src/.libs/libnss_db.so.2.0.0

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/%{_lib},/var/db}

%{__make} install \
	slibdir=/%{_lib} \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/libnss_db.so
cp -a db-Makefile $RPM_BUILD_ROOT/var/db/Makefile

cat << EOF -> $RPM_BUILD_ROOT%{_bindir}/create-db
#!/bin/sh
%{__make} -sC /var/db
EOF

ln -sf create-db $RPM_BUILD_ROOT%{_bindir}/update-db

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS
%attr(755,root,root) /%{_lib}/libnss_db-*.so
%attr(755,root,root) %ghost /%{_lib}/libnss_db.so.2
%attr(755,root,root) %{_bindir}/create-db
%attr(755,root,root) %{_bindir}/makedb
%attr(755,root,root) %{_bindir}/update-db

%config(noreplace) %verify(not md5 mtime size) /var/db/Makefile
