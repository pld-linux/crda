Summary:	udev helper: Central Regulatory Domain Agent
Name:		crda
Version:	1.1.2
Release:	1
License:	ISC
Group:		Networking/Daemons
Source0:	http://linuxwireless.org/download/crda/%{name}-%{version}.tar.bz2
# Source0-md5:	5226f65aebacf94baaf820f8b4e06df4
BuildRequires:	libgcrypt-devel
BuildRequires:	libnl-devel >= 1:3.0
BuildRequires:	python
BuildRequires:	python-M2Crypto
BuildRequires:	wireless-regdb
Requires:	udev-core
Requires:	wireless-regdb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CRDA acts as the udev helper for communication between the kernel and
userspace for regulatory compliance. It relies on nl80211 for
communication. CRDA is intended to be run only through udev
communication from the kernel. The user should never have to run it
manually except if debugging udev issues.

%prep
%setup -q

%build
%{__make} \
	V=1 \
	CC="%{__cc}" \
	REG_BIN=%{_datadir}/crda/regulatory.bin

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) /sbin/crda
%attr(755,root,root) /sbin/regdbdump
%{_mandir}/man8/*
/lib/udev/rules.d/85-regulatory.rules
