%define major %(echo %{version}|cut -d. -f1)
%define libname %mklibname wiredtiger
%define devname %mklibname -d wiredtiger

Name: wiredtiger
Version: 11.0.0
Release: 2
Source0: https://github.com/wiredtiger/wiredtiger/archive/refs/tags/%{version}.tar.gz
Summary: NoSQL platform for data management
URL: https://github.com/wiredtiger/wiredtiger
License: GPLv2/GPLv3
Group: Servers
BuildRequires: cmake ninja
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(libzstd)
BuildRequires: pkgconfig(liblz4)
BuildRequires: pkgconfig(snappy)
BuildRequires: pkgconfig(python3)
BuildRequires: pkgconfig(libsodium)
BuildRequires: swig
Requires: %{libname} = %{EVRD}

%description
WiredTiger is a NoSQL, Open Source extensible platform for data management. It
is released under version 2 or 3 of the GNU General Public License.
WiredTiger uses MultiVersion Concurrency Control (MVCC) architecture.

%package -n %{libname}
Summary: Libraries for the WiredTiger NoSQL data management platform
Group: System/Libraries

%description -n %{libname}
Libraries for the WiredTiger NoSQL data management platform

%package -n %{devname}
Summary: Development files for the WiredTiger NoSQL data management platform
Group: Development/Libraries
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files for the WiredTiger NoSQL data management platform

%prep
%autosetup -p1
%cmake \
	-DENABLE_STRICT:BOOL=OFF \
	-DENABLE_LZ4:BOOL=ON \
	-DENABLE_PYTHON:BOOL=ON \
	-DENABLE_SNAPPY:BOOL=ON \
	-DENABLE_ZLIB:BOOL=ON \
	-DENABLE_ZSTD:BOOL=ON \
%ifarch %{x86_64}
	-DWT_ARCH=x86 \
%else
%ifarch %{aarch64}
	-DWT_ARCH=aarch64 \
%else
%ifarch %{ppc}
	-DWT_ARCH=ppc64 \
%else
%ifarch %{riscv}
	-DWT_ARCH=riscv64 \
%endif
%endif
%endif
%endif
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

# -L/standard-directories is EVIL
sed -i 's,-L${libdir} ,,g' %{buildroot}%{_libdir}/pkgconfig/*.pc
# And so is -I/usr/include
sed -i -e '/^Cflags:/d' %{buildroot}%{_libdir}/pkgconfig/*.pc

%files
%{_bindir}/wt

%files -n %{libname}
%{_libdir}/libwiredtiger.so.%{major}*
# Those are plugins, not -devel files
%{_libdir}/libwiredtiger_lz4.so
%{_libdir}/libwiredtiger_snappy.so
%{_libdir}/libwiredtiger_zlib.so
%{_libdir}/libwiredtiger_zstd.so

%files -n %{devname}
%{_includedir}/wiredtiger.h
%{_includedir}/wiredtiger_ext.h
%{_libdir}/libwiredtiger.so
%{_libdir}/pkgconfig/wiredtiger.pc
