#
# Conditional build:
%bcond_with	verify	# database verification
%bcond_without	verbose	# verbose build (V=1)

Summary:	udev helper: Central Regulatory Domain Agent
Summary(pl.UTF-8):	Program pomocniczy udev: Central Regulatory Domain Agent
Name:		crda
Version:	3.18
Release:	3
License:	ISC
Group:		Networking/Daemons
Source0:	https://www.kernel.org/pub/software/network/crda/%{name}-%{version}.tar.xz
# Source0-md5:	0431fef3067bf503dfb464069f06163a
Source1:	https://git.kernel.org/pub/scm/linux/kernel/git/wens/wireless-regdb.git/plain/wens.key.pub.pem
# Source1-md5:	11522c524aa619d6031b73edd02e8071
Patch0:		%{name}-regdb.patch
Patch1:		%{name}-destdir.patch
Patch2:		%{name}-link.patch
Patch3:		build.patch
URL:		http://wireless.kernel.org/en/developers/Regulatory/CRDA
BuildRequires:	libgcrypt-devel
BuildRequires:	libnl-devel >= 1:3.2
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	python-M2Crypto
BuildRequires:	python-modules
%{?with_verify:BuildRequires:	wireless-regdb}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
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

%package libs
Summary:	CRDA libreg shared library
Summary(pl.UTF-8):	Biblioteka współdzielona CRDA libreg
Group:		Libraries

%description libs
CRDA libreg shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona CRDA libreg.

%package devel
Summary:	Header files for CRDA libreg library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CRDA libreg
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for CRDA libreg library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki CRDA libreg.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

cp -p %{SOURCE1} pubkeys

%build
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
%{__make} \
	CC="%{__cc}" \
	%{?with_verbose:V=1} \
%if %{with verify}
	REG_BIN=%{_datadir}/crda/regulatory.bin \
%else
	all_noverify \
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	%{?with_verbose:V=1} \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=/%{_lib}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) /sbin/crda
%attr(755,root,root) /sbin/regdbdump
%{_mandir}/man8/crda.8*
%{_mandir}/man8/regdbdump.8*
/lib/udev/rules.d/85-regulatory.rules

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libreg.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/reglib
