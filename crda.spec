Summary:	udev helper: Central Regulatory Domain Agent
Name:		crda
Version:	1.0.1
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	http://wireless.kernel.org/download/crda/%{name}-%{version}.tar.bz2
# Source0-md5:	03554b71eef2626795befa17eb1d8b9e
Source1:	http://wireless.kernel.org/download/wireless-regdb/wireless-regdb-2009.03.09.tar.bz2
# Source1-md5:	09d423911584e6580efb8af366775d5f
URL:		http://wireless.kernel.org/en/developers/Regulatory/CRDA
BuildRequires:	python
BuildRequires:	python-M2Crypto
Requires:	udev-core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CRDA acts as the udev helper for communication between the kernel and
userspace for regulatory compliance. It relies on nl80211 for
communication. CRDA is intended to be run only through udev
communication from the kernel. The user should never have to run it
manually except if debugging udev issues.

%prep
%setup -q -a1

%build
%{__make} \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	REG_BIN=$(echo wireless-regdb-*/regulatory.bin)

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
