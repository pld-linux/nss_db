# $Revision: 1.11 $Date: 2002-01-18 02:14:03 $
Summary:	Berkeley DB Name Service Switch Module
Summary(pl):	Modu³ NSS do baz db
Name:		nss_db
Version:	2.2
Release:	8
License:	LGPL
Group:		Base
Group(de):	Gründsätzlich
Group(es):	Base
Group(pl):	Podstawowe
Group(pt_BR):	Base
Source0:	ftp://sources.redhat.com/pub/glibc/releases/%{name}-%{version}.tar.gz
Patch0:		%{name}-chmod_644.patch
Patch1:		%{name}-amfix.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	db3-devel 
BuildRequires:	glibc-devel >= 2.2
BuildRequires:	libtool
Requires:	glibc >= 2.2
Requires:	make
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description 
This is nss_db, a name service switch module that can be used with
glibc-2.2.x.

%description -l pl
To jest nss_db, modu³ do serwisu nazw, który mo¿e byæ u¿ywany z
glibc-2.2.x.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing
libtoolize --copy --force
aclocal
autoconf
automake -a -c
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{lib,var/db}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install db-Makefile $RPM_BUILD_ROOT/var/db/Makefile

cat << EOF > $RPM_BUILD_ROOT%{_bindir}/create-db
#!/bin/sh
/usr/bin/make -sC /var/db/
EOF

ln -sf create-db $RPM_BUILD_ROOT%{_bindir}/update-db

gzip -9nf AUTHORS ChangeLog README NEWS THANKS

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) /lib/*.so
%attr(755,root,root) %{_bindir}/*
%config /var/db/Makefile
