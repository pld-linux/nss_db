# $Revision: 1.21 $Date: 2003-05-28 12:59:55 $
Summary:	Berkeley DB Name Service Switch Module
Summary(pl):	Modu³ NSS do baz db
Name:		nss_db
Version:	2.2
Release:	8
License:	LGPL
Group:		Base
Source0:	ftp://sources.redhat.com/pub/glibc/releases/%{name}-%{version}.tar.gz
# Source0-md5:	c2565cbd4a941ba70e41391693c3252d
Patch0:		%{name}-chmod_644.patch
Patch1:		%{name}-amfix.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	db-devel
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
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
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

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README NEWS THANKS
%attr(755,root,root) /lib/*.so
%attr(755,root,root) %{_bindir}/*
%config /var/db/Makefile
