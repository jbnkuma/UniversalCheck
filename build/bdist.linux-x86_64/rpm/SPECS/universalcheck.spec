%define name universalcheck
%define version 1
%define unmangled_version 1
%define release 1

Summary: Aplicacion que genera las bitacoras para  el reporte de SLAS 
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: BSD
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Jesus Becerril Navarrete <jesusbn5@protonmail.com>
Url: 
Requires: python => 2.6

%description
Aplicación que genera las bitacoras para generar el reporte de SLAS.

%prep
%setup -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
ln -sf /usr/local/lib64/python2.6/site-packages/universalcheck/ /tmp/universalcheck
mv /tmp/universalcheck ${RPM_BUILD_ROOT}/usr/bin/universalcheck

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(755,root,root)
%attr(755,root,root) %{_bindir}/universalcheck
