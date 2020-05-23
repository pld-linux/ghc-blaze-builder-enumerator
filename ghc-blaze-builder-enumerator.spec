#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	blaze-builder-enumerator
Summary:	Enumeratees for the incremental conversion of builders to bytestrings
Summary(pl.UTF-8):	Funkcje enumeratee do przyrostowej konwersji builderów do łańcuchów bajtów
Name:		ghc-%{pkgname}
Version:	0.2.0.5
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/blaze-builder-enumerator
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	735b6422d93043554db61297e047a5f5
URL:		http://hackage.haskell.org/package/blaze-builder-enumerator
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-blaze-builder >= 0.2.1.4
BuildRequires:	ghc-blaze-builder < 0.4
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-bytestring < 0.11
BuildRequires:	ghc-enumerator >= 0.4.3.1
BuildRequires:	ghc-enumerator < 0.5
BuildRequires:	ghc-transformers >= 0.2
BuildRequires:	ghc-transformers < 0.4
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-blaze-builder-prof >= 0.2.1.4
BuildRequires:	ghc-blaze-builder-prof < 0.4
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-bytestring-prof < 0.11
BuildRequires:	ghc-enumerator-prof >= 0.4.3.1
BuildRequires:	ghc-enumerator-prof < 0.5
BuildRequires:	ghc-transformers-prof >= 0.2
BuildRequires:	ghc-transformers-prof < 0.4
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4
Requires:	ghc-base < 5
Requires:	ghc-blaze-builder >= 0.2.1.4
Requires:	ghc-blaze-builder < 0.4
Requires:	ghc-bytestring >= 0.9
Requires:	ghc-bytestring < 0.11
Requires:	ghc-enumerator >= 0.4.3.1
Requires:	ghc-enumerator < 0.5
Requires:	ghc-transformers >= 0.2
Requires:	ghc-transformers < 0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This package integrates the builders from the blaze-builder package
with the enumerator package. It provides infrastructure and
enumeratees for incrementally executing builders and pass the filled
chunks to a bytestring iteratee.

%description -l pl.UTF-8
Ten pakiet integruje buildery z pakietu blaze-builder z pakietem
enumerator. Dostarcza infrastrukturę i funkcje enumeratee do
przyrostowego wywoływania builderów i przekazywania wypełnionych
porcji do funkcji iteratee łańcucha bajtów.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4
Requires:	ghc-base-prof < 5
Requires:	ghc-blaze-builder-prof >= 0.2.1.4
Requires:	ghc-blaze-builder-prof < 0.4
Requires:	ghc-bytestring-prof >= 0.9
Requires:	ghc-bytestring-prof < 0.11
Requires:	ghc-enumerator-prof >= 0.4.3.1
Requires:	ghc-enumerator-prof < 0.5
Requires:	ghc-transformers-prof >= 0.2
Requires:	ghc-transformers-prof < 0.4

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGES %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSblaze-builder-enumerator-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSblaze-builder-enumerator-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/*.hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSblaze-builder-enumerator-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Blaze/ByteString/Builder/*.p_hi
