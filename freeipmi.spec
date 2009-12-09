%define name freeipmi
%define version 0.8.1
%define release %mkrel 1
%define freeipmi_major	        10
%define ipmiconsole_major	    2
%define ipmidetect_major	    0
%define ipmimonitoring_major	4
%define libfreeipmi_name	    %mklibname freeipmi %{freeipmi_major}
%define libipmiconsole_name	    %mklibname ipmiconsole %{ipmiconsole_major}
%define libipmidetect_name	    %mklibname ipmidetect %{ipmidetect_major}
%define libipmimonitoring_name	%mklibname ipmimonitoring %{ipmimonitoring_major}
%define develname %mklibname -d %{name}

%define old_libname    %mklibname freeipmi 5
%define old_librelease 0.6.5-%mkrel 1

Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Summary: 	FreeIPMI
License: 	GPLv2+
Group: 		System/Kernel and hardware
URL:		http://www.gnu.org/software/freeipmi/index.html
Source: 	http://ftp.zresearch.com/pub/%name/%version/%{name}-%{version}.tar.gz
Patch0:		freeipmi-0.8.1-fix-str-fmt.patch
BuildRequires:	libguile-devel
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  transfig
BuildRequires:  ghostscript
BuildRequires:  texinfo
BuildRequires:  tetex-latex
# uses sys/io.h style I/O
ExcludeArch:	ppc %mips
BuildRoot:	    %{_tmppath}/%{name}-%{version}

%description
The FreeIPMI project provides "Remote-Console" (out-of-band) and
"System Management Software" (in-band) based on Intelligent
Platform Management Interface (IPMI v1.5) specification.

%package -n	%{libfreeipmi_name}
Group:		System/Libraries
License:	GPL
Summary:	Main library for %{name}
Obsoletes:	%old_libname < %old_librelease

%description -n	%{libfreeipmi_name}
This package contains one of the libraries needed to run programs dynamically
linked with %{name}.

%package -n	%{libipmiconsole_name}
Group:		System/Libraries
License:	GPL
Summary:	Main library for %{name}
Obsoletes:	%old_libname < %old_librelease

%description -n	%{libipmiconsole_name}
This package contains one of the libraries needed to run programs dynamically
linked with %{name}.

%package -n	%{libipmidetect_name}
Group:		System/Libraries
License:	GPL
Summary:	Main library for %{name}
Obsoletes:	%old_libname < %old_librelease

%description -n	%{libipmidetect_name}
This package contains one of the libraries needed to run programs dynamically
linked with %{name}.

%package -n	%{libipmimonitoring_name}
Group:		System/Libraries
License:	GPL
Summary:	Main library for %{name}
Obsoletes:	%old_libname < %old_librelease

%description -n	%{libipmimonitoring_name}
This package contains one of the libraries needed to run programs dynamically
linked with %{name}.

%package -n	%{develname}
Group:		Development/C
License:	GPL
Summary:	Headers for developing programs that will use %{name}
Requires:	%{libfreeipmi_name} = %{version}-%{release}
Requires:	%{libipmimonitoring_name} = %{version}-%{release}
Requires:	%{libipmiconsole_name} = %{version}-%{release}
Requires:	%{libipmidetect_name} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < %{version}-%{release}
Obsoletes:	%{libfreeipmi_name}-devel

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
Requires(pre,preun):	rpm-helper

%description utils
FreeIPMI utilities ipmipower, bmc-watchdog, ipmiping, and rmcpping.

%prep
%setup -q
%patch0 -p0

%build
%configure2_5x --localstatedir=/%{_var}
%make
cd doc
make pdf
cd -

%install
rm -rf %{buildroot}
%makeinstall_std 
install -d -m 755 %{buildroot}/%{_initrddir}
mv %{buildroot}/%{_sysconfdir}/init.d/bmc-watchdog %{buildroot}/%{_initrddir}/bmcwatchdog
mv %{buildroot}/%{_sysconfdir}/init.d/ipmidetectd %{buildroot}/%{_initrddir}
rm -rf %{buildroot}%{_docdir}/%{name}

%clean
rm -rf %{buildroot}

%post utils
%_post_service bmcwatchdog

%preun utils
%_preun_service bmcwatchdog

%preun
%_remove_install_info %{name}.info
%_remove_install_info %{name}-faq.info

%post
%_install_info %{name}.info
%_install_info %{name}-faq.info

%if %mdkversion < 200900
%post -n %{libfreeipmi_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libfreeipmi_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libipmidetect_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libipmidetect_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libipmiconsole_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libipmiconsole_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libipmimonitoring_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libipmimonitoring_name} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog* INSTALL NEWS README TODO
%doc doc/*.pdf
%{_sysconfdir}/*.conf
%{_infodir}/freeipmi-faq.info*
%dir %{_localstatedir}/lib/%{name}
%dir %{_localstatedir}/lib/%{name}/ipckey

%files -n %{libfreeipmi_name}
%defattr(-,root,root)
%{_libdir}/libfreeipmi.so.%{freeipmi_major}*

%files -n %{libipmiconsole_name}
%defattr(-,root,root)
%{_libdir}/libipmiconsole.so.%{ipmiconsole_major}*

%files -n %{libipmidetect_name}
%defattr(-,root,root)
%{_libdir}/libipmidetect.so.%{ipmidetect_major}*

%files -n %{libipmimonitoring_name}
%defattr(-,root,root)
%{_libdir}/libipmimonitoring.so.%{ipmimonitoring_major}*
 
%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/*

%files fish
%defattr(-,root,root)
%{_sbindir}/bmc-config
%{_sbindir}/bmc-info
%{_sbindir}/ipmi-sel
%{_sbindir}/ipmi-sensors
%{_sbindir}/ipmi-sensors-config
%{_mandir}/man5/bmc-config.conf.5*
%{_mandir}/man8/bmc-config.8*
%{_mandir}/man8/bmc-info.8*
%{_mandir}/man8/ipmi-sel.8*
%{_mandir}/man8/ipmi-sensors.8*
%{_mandir}/man8/ipmi-sensors-config.8*

%files utils
%defattr(-,root,root)
%doc COPYING.bmc-watchdog DISCLAIMER.bmc-watchdog
%doc COPYING.ipmiconsole DISCLAIMER.ipmiconsole 
%doc COPYING.ipmiping DISCLAIMER.ipmiping
%doc COPYING.ipmipower DISCLAIMER.ipmipower
%doc COPYING.rmcpping DISCLAIMER.rmcpping
%{_initrddir}/bmcwatchdog
%{_initrddir}/ipmidetectd
%config(noreplace) %{_sysconfdir}/ipmi_monitoring_sensors.conf
%config(noreplace) %{_sysconfdir}/sysconfig/bmc-watchdog
%config(noreplace) %{_sysconfdir}/logrotate.d/bmc-watchdog
%{_sbindir}/bmc-watchdog
%{_sbindir}/bmc-device
%{_sbindir}/ipmi-raw
%{_sbindir}/ipmi-oem
%{_sbindir}/ipmiping
%{_sbindir}/ipmiconsole
%{_sbindir}/ipmi-locate
%{_sbindir}/ipmipower
%{_sbindir}/rmcpping
%{_sbindir}/ipmi-chassis
%{_sbindir}/ipmi-chassis-config
%{_sbindir}/ipmi-fru
%{_sbindir}/ipmidetect
%{_sbindir}/ipmidetectd
%{_sbindir}/ipmimonitoring
%{_sbindir}/ipmi-dcmi
%{_sbindir}/pef-config
%{_sbindir}/ipmi-pef-config
%{_mandir}/man3/libipmiconsole.3*
%{_mandir}/man3/libipmidetect.3*
%{_mandir}/man3/libipmimonitoring.3*
%{_mandir}/man3/libfreeipmi.3*
%{_mandir}/man5/freeipmi.conf.5*
%{_mandir}/man5/ipmipower.conf.5*
%{_mandir}/man5/ipmiconsole.conf.5*
%{_mandir}/man5/ipmidetect.conf.5*
%{_mandir}/man5/ipmidetectd.conf.5*
%{_mandir}/man5/ipmi_monitoring_sensors.conf.5*
%{_mandir}/man5/ipmimonitoring.conf.5*
%{_mandir}/man5/ipmimonitoring_sensors.conf.5*
%{_mandir}/man5/libipmimonitoring.conf.5*
%{_mandir}/man7/freeipmi.7*
%{_mandir}/man8/ipmi-raw.*
%{_mandir}/man8/bmc-watchdog.8*
%{_mandir}/man8/bmc-device.8*
%{_mandir}/man8/ipmiping.8*
%{_mandir}/man8/ipmiconsole.8*
%{_mandir}/man8/ipmi-locate.8*
%{_mandir}/man8/ipmi-oem.8*
%{_mandir}/man8/ipmipower.8*
%{_mandir}/man8/rmcpping.8*
%{_mandir}/man8/ipmi-chassis.8*
%{_mandir}/man8/ipmi-chassis-config.8*
%{_mandir}/man8/ipmi-fru.8*
%{_mandir}/man8/ipmidetect.8*
%{_mandir}/man8/ipmidetectd.8*
%{_mandir}/man8/ipmimonitoring.8*
%{_mandir}/man8/pef-config.8*
%{_mandir}/man8/ipmi-dcmi.8.*
%{_mandir}/man8/ipmi-pef-config.8.*
