# $Revision: 1.4 $Date: 2000-11-12 03:38:18 $
Summary:	Berkeley DB Name Service Switch Module
Name:		nss_db
Version:	2.2
Release:	1
License:	LGPL
Group:		Base
Group(de):	Gründsätzlich
Group(pl):	Podstawowe
Source0:	ftp://sources.redhat.com/pub/glibc/releases/%{name}-%{version}.tar.gz
BuildRequires:	db3-devel 
BuildRequires:	glibc-devel >= 2.2
Requires:	glibc >= 2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description 
This is nss_db, a name service switch module that can be used with
glibc-2.2.xx.

%prep
%setup -q

%build
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

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) /lib/*.so
%attr(755,root,root) %{_bindir}/*
%config /var/db/Makefile
