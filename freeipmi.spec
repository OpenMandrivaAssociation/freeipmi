%define freeipmi_major	        16
%define ipmiconsole_major	2
%define ipmidetect_major	0
%define ipmimonitoring_major	5
%define libfreeipmi	%mklibname freeipmi %{freeipmi_major}
%define libipmiconsole	%mklibname ipmiconsole %{ipmiconsole_major}
%define libipmidetect	%mklibname ipmidetect %{ipmidetect_major}
%define libipmimonitoring	%mklibname ipmimonitoring %{ipmimonitoring_major}
%define develname		%mklibname -d %{name}

Name: 		freeipmi
Version: 	1.4.7
Release: 	3
Summary: 	FreeIPMI
License: 	GPLv2+
Group: 		System/Kernel and hardware
URL:		http://www.gnu.org/software/freeipmi/index.html
Source0: 	http://ftp.gnu.org/gnu/freeipmi/%{name}-%{version}.tar.gz
Source1: 	ipmidetectd.service
Source2: 	bmc-watchdog.service
BuildRequires:  pkgconfig(guile-2.0)
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  transfig
BuildRequires:  ghostscript
BuildRequires:  texinfo
BuildRequires:  texlive-scheme-small

%description
The FreeIPMI project provides "Remote-Console" (out-of-band) and
"System Management Software" (in-band) based on Intelligent
Platform Management Interface (IPMI v1.5) specification.

%package -n	%{libfreeipmi}
Group:		System/Libraries
Summary:	Main library for %{name}

%description -n	%{libfreeipmi}
This package contains one of the libraries needed to run programs dynamically
linked with %{name}.

%package -n	%{libipmiconsole}
Group:		System/Libraries
Summary:	Main library for %{name}

%description -n	%{libipmiconsole}
This package contains one of the libraries needed to run programs dynamically
linked with %{name}.

%package -n	%{libipmidetect}
Group:		System/Libraries
Summary:	Main library for %{name}

%description -n	%{libipmidetect}
This package contains one of the libraries needed to run programs dynamically
linked with %{name}.

%package -n	%{libipmimonitoring}
Group:		System/Libraries
Summary:	Main library for %{name}

%description -n	%{libipmimonitoring}
This package contains one of the libraries needed to run programs dynamically
linked with %{name}.

%package -n	%{develname}
Group:		Development/C
Summary:	Headers for developing programs that will use %{name}
Requires:	%{libfreeipmi} = %{version}-%{release}
Requires:	%{libipmimonitoring} = %{version}-%{release}
Requires:	%{libipmiconsole} = %{version}-%{release}
Requires:	%{libipmidetect} = %{version}-%{release}
Conflicts:	%{libfreeipmi} < 1.0.8-2
Conflicts:	%{libipmimonitoring} < 1.0.8-2
Conflicts:	%{libipmiconsole} < 1.0.8-2
Conflicts:	%{libipmidetect} < 1.0.8-2
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{libfreeipmi}-devel

%description -n	%{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package fish
Summary:    FreeIPMI Shell
Group:      System/Kernel and hardware
Requires:   %{name} = %{version}

%description fish
Fish provides Shell, Extension/Plug-in and scripting interface. As a
shell, User has access to both in-band and out-of-band access to the
host BMC through a rich set of IPMI commands.

%package utils
Summary:    FreeIPMI Utilities
Group:      System/Kernel and hardware
Requires:   %{name} = %{version}
Requires(post):  rpm-helper >= 0.24.8-1
Requires(preun): rpm-helper >= 0.24.8-1

%description utils
FreeIPMI utilities ipmipower, bmc-watchdog, ipmiping, and rmcpping.

%prep
%setup -q

%build
%define Werror_cflags %{nil}
%serverbuild
export CC=gcc
%configure2_5x --localstatedir=/%{_var} --disable-dependency-tracking --disable-static
%make
cd doc
make pdf
cd -

%install
%makeinstall_std 

rm -rf %{buildroot}%{_docdir}/%{name}
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_initrddir}/*  %{buildroot}%{_sysconfdir}/init.d/*

# Install systemd units
install -m 755 -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_unitdir}

# (cg) Make sure we mask the sysvinit script name
ln -s bmc-watchdog.service %{buildroot}%{_unitdir}/bmcwatchdog.service

%post utils
%_post_service bmcwatchdog

%preun utils
%_preun_service bmcwatchdog

%files
%doc AUTHORS COPYING ChangeLog* INSTALL NEWS README TODO
%doc doc/*.pdf
%{_sysconfdir}/freeipmi/*.conf
%{_mandir}/man5/freeipmi_interpret_sel.conf.5.*
%{_mandir}/man5/freeipmi_interpret_sensor.conf.5.*
%{_mandir}/man5/libipmiconsole.conf.5.*
%{_infodir}/freeipmi-faq.info*
%dir %{_localstatedir}/lib/%{name}
%{_localstatedir}/lib/%{name}/ipckey

%files -n %{libfreeipmi}
%{_libdir}/libfreeipmi.so.%{freeipmi_major}*

%files -n %{libipmiconsole}
%{_libdir}/libipmiconsole.so.%{ipmiconsole_major}*

%files -n %{libipmidetect}
%{_libdir}/libipmidetect.so.%{ipmidetect_major}*

%files -n %{libipmimonitoring}
%{_libdir}/libipmimonitoring.so.%{ipmimonitoring_major}*

%files -n %{develname}
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

%files fish
%{_sbindir}/bmc-config
%{_sbindir}/bmc-info
%{_sbindir}/ipmi-config
%{_sbindir}/ipmi-sel
%{_sbindir}/ipmi-sensors
%{_sbindir}/ipmi-sensors-config
%{_mandir}/man5/bmc-config.conf.5*
%{_mandir}/man5/ipmi-config.conf.5*
%{_mandir}/man8/bmc-config.8*
%{_mandir}/man8/bmc-info.8*
%{_mandir}/man8/ipmi-config.8*
%{_mandir}/man8/ipmi-sel.8*
%{_mandir}/man8/ipmi-sensors.8*
%{_mandir}/man8/ipmi-sensors-config.8*

%files utils
%doc COPYING.bmc-watchdog DISCLAIMER.bmc-watchdog
%doc COPYING.ipmiconsole DISCLAIMER.ipmiconsole 
%doc COPYING.ipmiping DISCLAIMER.ipmiping
%doc COPYING.ipmipower DISCLAIMER.ipmipower
%{_unitdir}/bmc-watchdog.service
%{_unitdir}/bmcwatchdog.service
%{_unitdir}/ipmidetectd.service
%config(noreplace) %{_sysconfdir}/sysconfig/bmc-watchdog
%{_sbindir}/bmc-device
%{_sbindir}/bmc-watchdog
%{_sbindir}/ipmi-chassis
%{_sbindir}/ipmi-chassis-config
%{_sbindir}/ipmi-console
%{_sbindir}/ipmi-dcmi
%{_sbindir}/ipmi-detect
%{_sbindir}/ipmi-fru
%{_sbindir}/ipmi-locate
%{_sbindir}/ipmi-oem
%{_sbindir}/ipmi-pef-config
%{_sbindir}/ipmi-pet
%{_sbindir}/ipmi-ping
%{_sbindir}/ipmi-power
%{_sbindir}/ipmi-raw
%{_sbindir}/ipmiconsole
%{_sbindir}/ipmidetect
%{_sbindir}/ipmidetectd
%{_sbindir}/ipmimonitoring
%{_sbindir}/ipmiping
%{_sbindir}/ipmipower
%{_sbindir}/ipmiseld
%{_sbindir}/pef-config
%{_sbindir}/rmcp-ping
%{_sbindir}/rmcpping
%{_mandir}/man3/libfreeipmi.3.*
%{_mandir}/man3/libipmiconsole.3.*
%{_mandir}/man3/libipmidetect.3.*
%{_mandir}/man3/libipmimonitoring.3.*
%{_mandir}/man5/freeipmi.conf.5.*
%{_mandir}/man5/ipmi_monitoring_sensors.conf.5.*
%{_mandir}/man5/ipmiconsole.conf.5.*
%{_mandir}/man5/ipmidetect.conf.5.*
%{_mandir}/man5/ipmidetectd.conf.5.*
%{_mandir}/man5/ipmimonitoring.conf.5.*
%{_mandir}/man5/ipmimonitoring_sensors.conf.5.*
%{_mandir}/man5/ipmipower.conf.5.*
%{_mandir}/man5/libipmimonitoring.conf.5.*
%{_mandir}/man5/ipmiseld.conf.5.*
%{_mandir}/man7/freeipmi.7.*
%{_mandir}/man8/bmc-device.8.*
%{_mandir}/man8/bmc-watchdog.8.*
%{_mandir}/man8/ipmi-chassis-config.8.*
%{_mandir}/man8/ipmi-chassis.8.*
%{_mandir}/man8/ipmi-console.8.*
%{_mandir}/man8/ipmi-dcmi.8.*
%{_mandir}/man8/ipmi-detect.8.*
%{_mandir}/man8/ipmi-fru.8.*
%{_mandir}/man8/ipmi-locate.8.*
%{_mandir}/man8/ipmi-oem.8.*
%{_mandir}/man8/ipmi-pef-config.8.*
%{_mandir}/man8/ipmi-pet.8.*
%{_mandir}/man8/ipmi-ping.8.*
%{_mandir}/man8/ipmi-power.8.*
%{_mandir}/man8/ipmi-raw.8.*
%{_mandir}/man8/ipmiconsole.8.*
%{_mandir}/man8/ipmidetect.8.*
%{_mandir}/man8/ipmidetectd.8.*
%{_mandir}/man8/ipmimonitoring.8.*
%{_mandir}/man8/ipmiping.8.*
%{_mandir}/man8/ipmiseld.8.*
%{_mandir}/man8/ipmipower.8.*
%{_mandir}/man8/pef-config.8.*
%{_mandir}/man8/rmcp-ping.8.*
%{_mandir}/man8/rmcpping.8.*
