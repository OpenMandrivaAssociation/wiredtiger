%define major %(echo %{version}|cut -d. -f1)
%define libname %mklibname wiredtiger %{major}
%define devname %mklibname -d wiredtiger

Name: wiredtiger
Version: 10.0.0
Release: 1
Source0: https://github.com/wiredtiger/wiredtiger/archive/refs/tags/%{version}.tar.gz
# Add cmake support (from develop branch)
Patch0: https://github.com/wiredtiger/wiredtiger/commit/31aeb15fc5cde6fa0722d009b46af91191ba70d8.patch
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
	-DWT_ARCH=arm64 \
%else
%ifarch %{ppc}
	-DWT_ARCH=ppc64 \
%endif
%endif
%endif
	-G Ninja \

%build
%ninja_build -C build

%install
%ninja_install -C build

%files -n %{libname}
%{_libdir}/libwiredtiger.so.%{major}*
# Those are plugins, not -devel files
%{_libdir}/libwiredtiger_lz4.so
%{_libdir}/libwiredtiger_snappy.so
%{_libdir}/libwiredtiger_zlib.so
%{_libdir}/libwiredtiger_zstd.so
%{_libdir}/pkgconfig/wiredtiger.pc

%files -n %{devname}
%{_includedir}/wiredtiger.h
%{_includedir}/wiredtiger_ext.h
%{_libdir}/libwiredtiger.so
