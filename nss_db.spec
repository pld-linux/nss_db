Summary:	Berkeley DB Name Service Switch Module
Summary(pl):	Modu³ NSS do baz db
Name:		nss_db
Version:	2.2.3
%define	bver	pre1
Release:	0.%{bver}.1
License:	LGPL
Group:		Base
Source0:	ftp://sources.redhat.com/pub/glibc/releases/%{name}-%{version}%{bver}.tar.gz
# Source0-md5:	b4440ba2865d28e9068e465426c19ede
Patch0:		%{name}-chmod_644.patch
Patch1:		%{name}-amfix.patch
Patch2:		%{name}-glibc23.patch
Patch3:		%{name}-db41.patch
BuildRequires:	autoconf
BuildRequires:	automake >= 1.4
BuildRequires:	db-devel >= 3.0
BuildRequires:	gettext-devel
BuildRequires:	glibc-devel >= 2.3
BuildRequires:	libtool
Requires:	glibc >= 2.3
Requires:	make
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is nss_db, a name service switch module that can be used with
glibc-2.2.x.

%description -l pl
To jest nss_db, modu³ do serwisu nazw, który mo¿e byæ u¿ywany z
glibc-2.2.x.

%prep
%setup -q -n %{name}-%{version}%{bver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make} \
	slibdir=/%{_lib}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/%{_lib},/var/db}

%{__make} install \
	slibdir=/%{_lib} \
	DESTDIR=$RPM_BUILD_ROOT

install db-Makefile $RPM_BUILD_ROOT/var/db/Makefile

cat << EOF > $RPM_BUILD_ROOT%{_bindir}/create-db
#!/bin/sh
/usr/bin/make -sC /var/db
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
%attr(755,root,root) /%{_lib}/*.so
%attr(755,root,root) %{_bindir}/*
%config /var/db/Makefile
