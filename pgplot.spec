Summary:	The PGPLOT Graphics Subroutine Library
Summary(pl):	Biblioteka PGPLOT
Name:		pgplot
Version:	5.2.0
Release:	2
License:	California Institute of Technology
Group:		Libraries
Source0:	ftp://ftp.astro.caltech.edu/pub/%{name}/%{name}5.2.tar.gz
Patch0:		%{name}-misc.patch
Patch1:		%{name}-man.patch
Patch2:		%{name}-drv.patch
Patch3:		%{name}-config.patch
URL:		http://astro.caltech.edu/~tjp/pgplot/
BuildRequires:	XFree86-devel
BuildRequires:	motif-devel
BuildRequires:	gcc-g77
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Device-independent graphics package for making simple scientific
graphs.

%description -l pl
Niezale¿ny sprzêtowo pakiet graficzny do tworzenia naukowych wykresów.

%package devel
Summary:	PGPLOT application development files
Summary(pl):	Pliki do tworzenia aplikacji dla PGPLOT
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Libraries and headers for developing applications that use PGPLOT.

%description devel -l pl
Biblioteki i pliki nag³ówkowe niezbêdne do tworzenia aplikacji dla
PGPLOT.

%package demos
Summary:	PGPLOT demo applications
Summary(pl):	Aplikacje demonstracyjne PGPLOT
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description demos
Demonstration applications for PGPLOT.

%description demos -l pl
Aplikacje demonstruj±ce wykorzystanie biblioteki PGPLOT.

%package static
Summary:	PGPLOT static libraries
Summary(pl):	Biblioteki statyczne dla PGPLOT
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static libraries for PGPLOT.

%description static -l pl
Biblioteki statyczne dla PGPLOT.

%prep
%setup -q -n pgplot
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p0

%build
./makemake . linux g77_elf
%{__make} \
	FFLAGC="-u -Wall -fPIC %{rpmcflags}" \
	CFLAGC="-Wall -fPIC -DPG_PPU %{rpmcflags}"

%{__make} cpg \
        CFLAGC="-Wall -fPIC -DPG_PPU %{rpmcflags}"

%{__make} pgplot.html
%{__make} pgplot-routines.tex
%{__make} clean

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_bindir},%{_mandir}/man3} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}/{cpg,pgm,demos} \
	$RPM_BUILD_ROOT%{_libdir}/pgplot

install grfont.dat grexec.f rgb.txt *.inc $RPM_BUILD_ROOT%{_libdir}/pgplot
install pgdisp pgxwin_server $RPM_BUILD_ROOT%{_bindir}
install cpgplot.h XmPgplot.h $RPM_BUILD_ROOT%{_includedir}
install pgplot.3x	     $RPM_BUILD_ROOT%{_mandir}/man3
install lib*.a		     $RPM_BUILD_ROOT%{_libdir}
install libpgplot.so.*	     $RPM_BUILD_ROOT%{_libdir}

(cd $RPM_BUILD_ROOT%{_libdir}; ln -sf libpgplot.so.5.2.0 libpgplot.so)

install cpgdemo $RPM_BUILD_ROOT%{_examplesdir}/%{name}/cpg
install pgdemo* $RPM_BUILD_ROOT%{_examplesdir}/%{name}/demos
install pgmdemo $RPM_BUILD_ROOT%{_examplesdir}/%{name}/pgm
cp -a cpg/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}/cpg
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}/demos
cp -a drivers/xmotif/pgmdemo.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}/pgm

mv -f pgdispd/aaaread.me pgdispd/pgdisp.txt

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_libdir}/pgplot/*.inc
%{_includedir}/*
%{_mandir}/man3/*

%files demos
%defattr(644,root,root,755)
%{_examplesdir}/%{name}

%files static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/lib*.a
