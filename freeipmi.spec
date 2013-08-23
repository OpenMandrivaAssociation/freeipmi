%define Werror_cflags %nil
%define freeipmi_major		13
%define ipmiconsole_major	2
%define ipmidetect_major	0
%define ipmimonitoring_major	5
%define libfreeipmi		%mklibname freeipmi %{freeipmi_major}
%define libipmiconsole		%mklibname ipmiconsole %{ipmiconsole_major}
%define libipmidetect		%mklibname ipmidetect %{ipmidetect_major}
%define libipmimonitoring	%mklibname ipmimonitoring %{ipmimonitoring_major}
%define devname %mklibname -d %{name}

Summary: 	FreeIPMI
Name: 		freeipmi
Version: 	1.3.1
Release: 	1
License: 	GPLv2
Group: 		System/Kernel and hardware
Url:		http://www.gnu.org/software/freeipmi/index.html
Source0: 	http://ftp.gnu.org/gnu/freeipmi/%{name}-%{version}.tar.gz
Source1: 	http://ftp.gnu.org/gnu/freeipmi/%{name}-%{version}.tar.gz.sig

BuildRequires:  ghostscript
BuildRequires:  texinfo
BuildRequires:  tetex-latex
BuildRequires:  transfig
BuildRequires:  readline-devel
BuildRequires:	pkgconfig(guile-2.0)
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(ncurses)

%description
The FreeIPMI project provides "Remote-Console" (out-of-band) and
"System Management Software" (in-band) based on Intelligent
Platform Management Interface (IPMI v1.5) specification.

%package -n	%{libfreeipmi}
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n	%{libfreeipmi}
This package contains one of the libraries needed to run programs dynamically
linked with %{name}.

%package -n	%{libipmiconsole}
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n	%{libipmiconsole}
This package contains one of the libraries needed to run programs dynamically
linked with %{name}.

%package -n	%{libipmidetect}
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n	%{libipmidetect}
This package contains one of the libraries needed to run programs dynamically
linked with %{name}.

%package -n	%{libipmimonitoring}
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n	%{libipmimonitoring}
This package contains one of the libraries needed to run programs dynamically
linked with %{name}.

%package -n	%{devname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libfreeipmi} = %{version}-%{release}
Requires:	%{libipmimonitoring} = %{version}-%{release}
Requires:	%{libipmiconsole} = %{version}-%{release}
Requires:	%{libipmidetect} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
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
Requires(pre,preun):	rpm-helper

%description utils
FreeIPMI utilities ipmipower, bmc-watchdog, ipmiping, and rmcpping.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
	--localstatedir=/%{_var} \
	--disable-dependency-tracking

%make 
cd doc
make pdf
cd -

%install
%makeinstall_std 

install -d -m 755 %{buildroot}/%{_initrddir}
mv %{buildroot}/%{_sysconfdir}/init.d/bmc-watchdog %{buildroot}/%{_initrddir}/bmcwatchdog
mv %{buildroot}/%{_sysconfdir}/init.d/ipmidetectd %{buildroot}/%{_initrddir}
mv %{buildroot}/%{_sysconfdir}/init.d/ipmiseld %{buildroot}/%{_initrddir}
rm -rf %{buildroot}%{_docdir}/%{name}

%post fish
%_post_service ipmiseld

%preun fish
%_preun_service ipmiseld

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
%dir %{_localstatedir}/lib/%{name}/ipckey

%files -n %{libfreeipmi}
%{_libdir}/libfreeipmi.so.%{freeipmi_major}*

%files -n %{libipmiconsole}
%{_libdir}/libipmiconsole.so.%{ipmiconsole_major}*

%files -n %{libipmidetect}
%{_libdir}/libipmidetect.so.%{ipmidetect_major}*

%files -n %{libipmimonitoring}
%{_libdir}/libipmimonitoring.so.%{ipmimonitoring_major}*

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/libfreeipmi.pc
%{_libdir}/pkgconfig/libipmiconsole.pc
%{_libdir}/pkgconfig/libipmidetect.pc
%{_libdir}/pkgconfig/libipmimonitoring.pc

%files fish
%{_initrddir}/ipmiseld
%{_sbindir}/bmc-config
%{_sbindir}/bmc-info
%{_sbindir}/ipmi-sel
%{_sbindir}/ipmiseld
%{_sbindir}/ipmi-sensors
%{_sbindir}/ipmi-sensors-config
%{_mandir}/man5/bmc-config.conf.5*
%{_mandir}/man5/ipmiseld.conf.5*
%{_mandir}/man8/bmc-config.8*
%{_mandir}/man8/bmc-info.8*
%{_mandir}/man8/ipmi-sel.8*
%{_mandir}/man8/ipmiseld.8*
%{_mandir}/man8/ipmi-sensors.8*
%{_mandir}/man8/ipmi-sensors-config.8*

%files utils
%doc COPYING.bmc-watchdog DISCLAIMER.bmc-watchdog
%doc COPYING.ipmiconsole DISCLAIMER.ipmiconsole 
%doc COPYING.ipmiping DISCLAIMER.ipmiping
%doc COPYING.ipmipower DISCLAIMER.ipmipower
%{_initrddir}/bmcwatchdog
%{_initrddir}/ipmidetectd
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
%{_sbindir}/ipmi-pet
%{_sbindir}/ipmi-pef-config
%{_sbindir}/ipmi-ping
%{_sbindir}/ipmi-power
%{_sbindir}/ipmi-raw
%{_sbindir}/ipmiconsole
%{_sbindir}/ipmidetect
%{_sbindir}/ipmidetectd
%{_sbindir}/ipmimonitoring
%{_sbindir}/ipmiping
%{_sbindir}/ipmipower
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
%{_mandir}/man8/ipmi-pet.8.*
%{_mandir}/man8/ipmi-pef-config.8.*
%{_mandir}/man8/ipmi-ping.8.*
%{_mandir}/man8/ipmi-power.8.*
%{_mandir}/man8/ipmi-raw.8.*
%{_mandir}/man8/ipmiconsole.8.*
%{_mandir}/man8/ipmidetect.8.*
%{_mandir}/man8/ipmidetectd.8.*
%{_mandir}/man8/ipmimonitoring.8.*
%{_mandir}/man8/ipmiping.8.*
%{_mandir}/man8/ipmipower.8.*
%{_mandir}/man8/pef-config.8.*
%{_mandir}/man8/rmcp-ping.8.*
%{_mandir}/man8/rmcpping.8.*

