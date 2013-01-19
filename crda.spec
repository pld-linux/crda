#
# Conditional build:
%bcond_without	verify	# don't verify database
#
Summary:	udev helper: Central Regulatory Domain Agent
Summary(pl.UTF-8):	Program pomocniczy udev: Central Regulatory Domain Agent
Name:		crda
Version:	1.1.3
Release:	1
License:	ISC
Group:		Networking/Daemons
Source0:	http://linuxwireless.org/download/crda/%{name}-%{version}.tar.bz2
# Source0-md5:	29579185e06a75675507527243d28e5c
Patch0:		%{name}-regdb.patch
URL:		http://wireless.kernel.org/en/developers/Regulatory
BuildRequires:	libgcrypt-devel
BuildRequires:	libnl-devel >= 1:3.2
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	python-M2Crypto
%{?with_verify:BuildRequires:	wireless-regdb}
Requires:	udev-core
Requires:	wireless-regdb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CRDA acts as the udev helper for communication between the kernel and
userspace for wireless regulatory compliance. It relies on nl80211 for
communication. CRDA is intended to be run only through udev
communication from the kernel. The user should never have to run it
manually except if debugging udev issues.

%description -l pl.UTF-8
CRDA działa jako program pomocniczy udev do komunikacji między jądrem
a przestrzenią użytkownika w celu zgodności łączności bezprzewodowej z
przepisami. Na potrzeby komunikacji polega na nl80211. CRDA jest
przeznaczone do uruchamiania wyłącznie poprzez udev. Użytkownik nigdy
nie powinien wywoływać go ręcznie, chyba że w celach diagnostyki udev.

%prep
%setup -q
%patch0 -p1

%build
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
%{__make} %{!?with_verify:all_noverify} \
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
%doc LICENSE README
%attr(755,root,root) /sbin/crda
%attr(755,root,root) /sbin/regdbdump
%{_mandir}/man8/crda.8*
%{_mandir}/man8/regdbdump.8*
/lib/udev/rules.d/85-regulatory.rules
