# $Revision: 1.2 $Date: 2000-10-03 22:10:00 $
Summary:	Berkeley DB Name Service Switch Module
Name:		nss_db
Version:	2.1.92
Release:	1
License:	LGPL
Group:		Base
Group(de):	Gründsätzlich
Group(pl):	Podstawowe
Source0:	ftp://sourceware.cygnus.com/pub/glibc/releases/%{name}-%{version}.tar.gz
BuildRequires:	db3-devel 
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

strip --strip-unneeded $RPM_BUILD_ROOT/lib/*
strip --strip-unneeded $RPM_BUILD_ROOT%{_bindir}/makedb

gzip -9nf AUTHORS ChangeLog README NEWS THANKS

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {AUTHORS,ChangeLog,README,NEWS,THANKS}.gz
%attr(755,root,root) /lib/*.so
%attr(755,root,root) %{_bindir}/*
%config /var/db/Makefile
