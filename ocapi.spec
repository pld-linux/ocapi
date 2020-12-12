#
# Conditional build:
%bcond_with	tests		# perform tests (requires network)
#
Summary:	The OPeNDAP C DAP2 library (client-side only)
Summary(pl.UTF-8):	Biblioteka OPeNDAP DAP2 dla C (tylko strona kliencka)
Name:		ocapi
Version:	1.4.3
Release:	3
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.opendap.org/pub/OCAPI/source/%{name}-%{version}.tar.gz
# Source0-md5:	c1a4f9391d7f88b0f9e93bfcb9c5181f
Patch0:		%{name}-libdir.patch
Patch1:		%{name}-curl.patch
Patch2:		%{name}-opt.patch
Patch3:		%{name}-format.patch
URL:		http://opendap.org/ocapi/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	curl-devel >= 7.10.6
BuildRequires:	libtirpc-devel
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
Requires:	curl >= 7.10.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OPeNDAP C API (OCAPI) provides a set of C-language type
definitions and functions that can be used to retrieve data over the
Internet from servers that implement the OPeNDAP Data Access Protocol
(DAP). The OCAPI implementation provides a low-overhead way to
retrieve this data, making it practical to include OPeNDAP capability
in relatively simple software. Use the OCAPI to build clients such as
command extensions for IDL and Matlab which are implemented as shared
object libraries.

%description -l pl.UTF-8
OPeNDAP C API (OCAPI) zawiera zbiór definicji typów i funkcji języka C
przeznaczonych do pobierania danych poprzez Internet z serwerów
implementujących protokół OPeNDAP Data Access Protocol (DAP).
Implementacja OCAPI daje możliwość pobierania tych danych z małym
narzutem, czyniąc praktycznym wbudowanie obsługi OPeNDAP w stosunkowo
proste oprogramowanie. Przy użyciu OCAPI można stworzyć klientów,
takich jak rozszerzenia poleceń IDL lub Matlaba zaimplementowane jako
biblioteki współdzielone.

%package devel
Summary:	Header files for OCAPI library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OCAPI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	curl-devel >= 7.10.6
Requires:	libtirpc-devel
Requires:	ncurses-devel
Requires:	readline-devel

%description devel
Header files for OCAPI library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OCAPI.

%package static
Summary:	Static OCAPI library
Summary(pl.UTF-8):	Statyczna biblioteka OCAPI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OCAPI library.

%description static -l pl.UTF-8
Statyczna biblioteka OCAPI.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal} -I conf
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CPPFLAGS="%{rpmcppflags} -I/usr/include/tirpc" \
	LIBS="-ltirpc"
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/getocapi
%attr(755,root,root) %{_libdir}/libocapi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libocapi.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ocapi-config
%attr(755,root,root) %{_libdir}/libocapi.so
%{_libdir}/libocapi.la
%{_includedir}/ocapi

%files static
%defattr(644,root,root,755)
%{_libdir}/libocapi.a
