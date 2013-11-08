Summary:	The PGPLOT Graphics Subroutine Library
Summary(pl.UTF-8):	Biblioteka PGPLOT
Name:		pgplot
Version:	5.2.2
Release:	11
%define	foover	%(echo %{version} | tr -d .)
License:	free for non-commercial purposes
Group:		Libraries
Source0:	ftp://ftp.astro.caltech.edu/pub/pgplot/%{name}%{foover}.tar.gz
# Source0-md5:	e8a6e8d0d5ef9d1709dfb567724525ae
Patch0:		%{name}-misc.patch
Patch1:		%{name}-man.patch
Patch2:		%{name}-drv.patch
Patch3:		%{name}-config.patch
Patch4:		%{name}-png.patch
Patch5:		%{name}-compile.patch
Patch6:		%{name}-libpng15.patch
URL:		http://astro.caltech.edu/~tjp/pgplot/
BuildRequires:	libxcb-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXau-devel
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXdmcp-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-proto-xproto-devel
BuildRequires:	gcc-fortran
BuildRequires:	motif-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Device-independent graphics package for making simple scientific
graphs.

%description -l pl.UTF-8
Niezależny sprzętowo pakiet graficzny do tworzenia naukowych wykresów.

%package devel
Summary:	PGPLOT application development files
Summary(pl.UTF-8):	Pliki do tworzenia aplikacji dla PGPLOT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Libraries and headers for developing applications that use PGPLOT.

%description devel -l pl.UTF-8
Biblioteki i pliki nagłówkowe niezbędne do tworzenia aplikacji dla
PGPLOT.

%package demos
Summary:	PGPLOT demo applications
Summary(pl.UTF-8):	Aplikacje demonstracyjne PGPLOT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description demos
Demonstration applications for PGPLOT.

%description demos -l pl.UTF-8
Aplikacje demonstrujące wykorzystanie biblioteki PGPLOT.

%package static
Summary:	PGPLOT static libraries
Summary(pl.UTF-8):	Biblioteki statyczne dla PGPLOT
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libraries for PGPLOT.

%description static -l pl.UTF-8
Biblioteki statyczne dla PGPLOT.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
./makemake . linux g77_gcc
%{__make} -j1 \
	FCOMPL=gfortran \
	SHARED_LD="gfortran -shared -o libpgplot.so.5.2.2 -Wl,-soname,libpgplot.so.5" \
	FFLAGC="-u -Wall -fPIC %{rpmcflags}" \
	CFLAGC="-Wall -fPIC -DPG_PPU %{rpmcflags}" \
	CFLAGD="-Wall %{rpmcflags}" \
	SHARED_LIB_LIBS="-L/usr/X11R6/%{_lib} -lX11 -lpng" \
	LIBS="-L/usr/X11R6/%{_lib} -lX11" \
	MOTIF_LIBS="-L/usr/X11R6/%{_lib} -lXm -lXt -lX11"

%{__make} cpg \
	FCOMPL=gfortran \
	CFLAGD="-Wall %{rpmcflags}" \
	LIBS="-L/usr/X11R6/%{_lib} -lX11"

%{__make} pgplot.html
%{__make} pgplot-routines.tex
%{__make} clean

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_bindir},%{_mandir}/man3} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}/{cpg,pgm,demos} \
	$RPM_BUILD_ROOT%{_libdir}/pgplot

install grfont.dat grexec.f rgb.txt *.inc	$RPM_BUILD_ROOT%{_libdir}/pgplot
install pgdisp pgxwin_server			$RPM_BUILD_ROOT%{_bindir}
install cpgplot.h XmPgplot.h			$RPM_BUILD_ROOT%{_includedir}
install pgplot.3x				$RPM_BUILD_ROOT%{_mandir}/man3
install lib*.a					$RPM_BUILD_ROOT%{_libdir}
install libpgplot.so.*				$RPM_BUILD_ROOT%{_libdir}

(cd $RPM_BUILD_ROOT%{_libdir}; ln -sf libpgplot.so.*.*.* libpgplot.so)

install cpgdemo $RPM_BUILD_ROOT%{_examplesdir}/%{name}/cpg
install pgdemo* $RPM_BUILD_ROOT%{_examplesdir}/%{name}/demos
install pgmdemo $RPM_BUILD_ROOT%{_examplesdir}/%{name}/pgm
cp -a cpg/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}/cpg
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}/demos
cp -a drivers/xmotif/pgmdemo.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}/pgm

mv -f pgdispd/aaaread.me pgdispd/pgdisp.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc drivers.list aaaread.me ver5*.txt pgplot.doc pgdispd/pgdisp.txt copyright.notice
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libpgplot.so.*.*

%dir %{_libdir}/pgplot
%{_libdir}/pgplot/grexec.f
%{_libdir}/pgplot/grfont.dat
%{_libdir}/pgplot/rgb.txt

%files devel
%defattr(644,root,root,755)
%doc pgplot-routines.tex pgplot.html
%attr(755,root,root) %{_libdir}/libpgplot.so
%{_libdir}/libcpgplot.a
%{_libdir}/libXmPgplot.a
%{_libdir}/pgplot/*.inc
%{_includedir}/*
%{_mandir}/man3/*

%files demos
%defattr(644,root,root,755)
%{_examplesdir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/libpgplot.a
