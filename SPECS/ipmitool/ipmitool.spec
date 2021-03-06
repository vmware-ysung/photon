%global debug_package %{nil}
Summary:        ipmitool - Utility for IPMI control
Name:           ipmitool
Version:        1.8.18
Release:        3%{?dist}
License:        BSD

Group:          System Environment/Utilities
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.bz2
%define sha1    ipmitool=ff4781bb78f264d44fa4bf1767f268d4079d87ba
Patch0:         CVE-2020-5208.patch

%description
This package contains a utility for interfacing with devices that support
the Intelligent Platform Management Interface specification.  IPMI is
an open standard for machine health, inventory, and remote power control.

This utility can communicate with IPMI-enabled devices through either a
kernel driver such as OpenIPMI or over the RMCP LAN protocol defined in
the IPMI specification.  IPMIv2 adds support for encrypted LAN
communications and remote Serial-over-LAN functionality.

It provides commands for reading the Sensor Data Repository (SDR) and
displaying sensor values, displaying the contents of the System Event
Log (SEL), printing Field Replaceable Unit (FRU) information, reading and
setting LAN configuration, and chassis power control.

%prep
%setup -q
%patch0 -p1

%build
%configure --with-kerneldir \
    --with-rpm-distro=
make

%install
make DESTDIR=$RPM_BUILD_ROOT install-strip
mkdir -p %{buildroot}/lib/systemd/system

%check
make %{?_smp_mflags} check

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(755,root,root)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_datadir}/ipmitool/*
%{_mandir}/man*/*
%doc %{_datadir}/doc/ipmitool

%changelog
*   Thu Mar 05 2020 Keerthana K <keerthanak@vmware.com> 1.8.18-3
-   Fix %configure.
*   Thu Feb 13 2020 Keerthana K <keerthanak@vmware.com> 1.8.18-2
-   Fix CVE-2020-5208.
*   Fri Aug 25 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.18-1
-   Initial build.  First version
