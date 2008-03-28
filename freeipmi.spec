%define name freeipmi
%define version 0.5.6
%define release %mkrel 1
%define major	1
%define libname	%mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Summary: 	FreeIPMI
License: 	GPLv2+
Group: 		System/Kernel and hardware
URL:		http://www.gnu.org/software/freeipmi/index.html
Source: 	http://ftp.zresearch.com/pub/%name/%version/%{name}-%{version}.tar.bz2
BuildRequires:	libguile-devel
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  transfig
BuildRequires:  ghostscript
BuildRequires:  texinfo
BuildRequires:  tetex-latex
# uses sys/io.h style I/O
ExcludeArch:	ppc
BuildRoot:	    %{_tmppath}/%{name}-%{version}

%description
The FreeIPMI project provides "Remote-Console" (out-of-band) and
"System Management Software" (in-band) based on Intelligent
Platform Management Interface (IPMI v1.5) specification.

%package -n	%{libname}
Group:		System/Libraries
License:	GPL
Summary:	Main library for %{name}
Provides:	lib%{name} = %{version}-%{release}
Obsoletes:	lib%{name} < %{version}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{develname}
Group:		Development/C
License:	GPL
Summary:	Headers for developing programs that will use %{name}
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < %{version}-%{release}
Obsoletes:	%{libname}-devel

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

%build
%configure2_5x --localstatedir=%{_var}
%make
cd doc
make pdf
cd -

%install
rm -rf %{buildroot}
%makeinstall_std 
install -d -m 755 %{buildroot}/%{_initrddir}
mv %{buildroot}/%{_sysconfdir}/init.d/freeipmi-bmc-watchdog %{buildroot}/%{_initrddir}
mv %{buildroot}/%{_sysconfdir}/init.d/freeipmi-ipmidetectd %{buildroot}/%{_initrddir}
rm -rf %{buildroot}%{_docdir}/%{name}

%clean
rm -rf %{buildroot}

%post utils
%_post_service freeipmi-bmc-watchdog

%preun utils
%_preun_service freeimpi-bmc-watchdog

%preun
%_remove_install_info %{name}.info
%_remove_install_info %{name}-faq.info

%post
%_install_info %{name}.info
%_install_info %{name}-faq.info

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog* INSTALL NEWS README TODO
%doc doc/*.pdf
%{_infodir}/freeipmi-faq.info*
%dir %{_localstatedir}/%{name}
%dir %{_localstatedir}/%{name}/ipckey

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libfreeipmi.so.%{major}*
%{_libdir}/libipmi*.so.*
 
%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/*

%files fish
%defattr(-,root,root)
#%{_sbindir}/bmc-autoconfig
%{_sbindir}/bmc-config
%{_sbindir}/bmc-info
%{_sbindir}/ipmi-sel
%{_sbindir}/ipmi-sensors
%{_mandir}/man5/bmc-config.conf.5*
%{_mandir}/man8/bmc-config.*
%{_mandir}/man8/bmc-info.*
%{_mandir}/man8/ipmi-sel.*
%{_mandir}/man8/ipmi-sensors.*

%files utils
%defattr(-,root,root)
%doc COPYING.bmc-watchdog DISCLAIMER.bmc-watchdog
%doc COPYING.ipmiconsole DISCLAIMER.ipmiconsole 
%doc COPYING.ipmiping DISCLAIMER.ipmiping
%doc COPYING.ipmipower DISCLAIMER.ipmipower
%doc COPYING.rmcpping DISCLAIMER.rmcpping
%{_initrddir}/%{name}-bmc-watchdog
%{_initrddir}/%{name}-ipmidetectd
%config(noreplace) %{_sysconfdir}/ipmi_monitoring_sensors.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-bmc-watchdog
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}-bmc-watchdog
%{_sbindir}/bmc-watchdog
%{_sbindir}/ipmi-raw
%{_sbindir}/ipmiping
%{_sbindir}/ipmiconsole
%{_sbindir}/ipmi-locate
%{_sbindir}/ipmipower
%{_sbindir}/rmcpping
%{_sbindir}/ipmi-chassis
%{_sbindir}/ipmi-fru
%{_sbindir}/ipmidetect
%{_sbindir}/ipmidetectd
%{_sbindir}/ipmimonitoring
%{_sbindir}/pef-config
%{_mandir}/man3/libipmiconsole.3*
%{_mandir}/man3/libipmidetect.3*
%{_mandir}/man3/libipmimonitoring.3*
%{_mandir}/man5/ipmipower.conf.5*
%{_mandir}/man5/ipmiconsole.conf.5*
%{_mandir}/man5/ipmidetect.conf.5*
%{_mandir}/man5/ipmidetectd.conf.5*
%{_mandir}/man8/ipmi-raw.*
%{_mandir}/man8/bmc-watchdog.8*
%{_mandir}/man8/ipmiping.8*
%{_mandir}/man8/ipmiconsole.8*
%{_mandir}/man8/ipmi-locate.8*
%{_mandir}/man8/ipmipower.8*
%{_mandir}/man8/rmcpping.8*
%{_mandir}/man8/ipmi-chassis.8*
%{_mandir}/man8/ipmi-fru.8*
%{_mandir}/man8/ipmidetect.8*
%{_mandir}/man8/ipmidetectd.8*
%{_mandir}/man8/ipmimonitoring.8*
%{_mandir}/man8/pef-config.8*
