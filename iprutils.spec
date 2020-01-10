Summary: Utilities for the IBM Power Linux RAID adapters
Name:    iprutils
Version: 2.4.13.1
Release: 1%{?dist}
License: CPL
Group:   System Environment/Base
URL:     http://sourceforge.net/projects/iprdd/

Source0: https://sourceforge.net/projects/iprdd/files/iprutils%20for%202.6%20kernels/2.4.13/%{name}-%{version}.tar.gz

# missing man page
Source1: iprdbg.8.gz

Patch0: 0001-Service-start-is-controled-by-udev-rule.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: /sbin/pidof
# for iprsos
Requires: lsscsi

BuildRequires: ncurses-devel
BuildRequires: libcap-devel
BuildRequires: kernel-devel
BuildRequires: systemd
BuildRequires: python-devel
BuildRequires: zlib-devel

Obsoletes: ipr-utils

%description
Provides a suite of utilities to manage and configure SCSI devices
supported by the ipr SCSI storage device driver.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .udev

%build
export CFLAGS="%{optflags} -fPIE -Wl,-z,relro,-z,now"
export LDFLAGS="-pie"

%configure

%{__make}

%install

%make_install

mkdir -p $RPM_BUILD_ROOT/%{_udevrulesdir}
%{__install} -m 0644 udev/rules.d/90-iprutils.rules $RPM_BUILD_ROOT/%{_udevrulesdir}/90-iprutils.rules

# install all service units
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
%{__install} -m 0644 systemd/iprinit.service $RPM_BUILD_ROOT/%{_unitdir}/iprinit.service
%{__install} -m 0644 systemd/iprdump.service $RPM_BUILD_ROOT/%{_unitdir}/iprdump.service
%{__install} -m 0644 systemd/iprupdate.service $RPM_BUILD_ROOT/%{_unitdir}/iprupdate.service
%{__install} -m 0644 systemd/iprutils.target $RPM_BUILD_ROOT/%{_unitdir}/iprutils.target

# missing man page
%{__install} -m 0644 %SOURCE1 %{buildroot}%{_mandir}/man8/

%{__mv} %{buildroot}%{_sysconfdir}/bash_completion.d/iprconfig-bash-completion.sh %{buildroot}%{_sysconfdir}/bash_completion.d/iprutils
%{__chmod} 0644 %{buildroot}/etc/bash_completion.d/iprutils

# never been shipped in Fedora/RHEL
%{__rm} -rf %{buildroot}/etc/ha.d/resource.d/iprha
%{__rm} -rf %{buildroot}/etc/ha.d/resource.d/iprha.in

# fix permissions
%{__chmod} 0700 %{buildroot}/%{_sbindir}/iprdbg

%post
%systemd_post iprinit.service
%systemd_post iprdump.service
%systemd_post iprupdate.service
%systemd_post iprutils.target

%preun
%systemd_preun iprinit.service
%systemd_preun iprdump.service
%systemd_preun iprupdate.service
%systemd_preun iprutils.target

%files
%doc README LICENSE
%{_sbindir}/*
%{_mandir}/man8/*
%{_unitdir}/iprinit.service
%{_unitdir}/iprdump.service
%{_unitdir}/iprupdate.service
%{_unitdir}/iprutils.target
%{_udevrulesdir}/90-iprutils.rules
%{_sysconfdir}/bash_completion.d

%changelog
* Tue Aug 23 2016 Sinny Kumari <skumari@redhat.com> - 2.4.13.1-1
- Rebase to upstream release 2.4.13.1
- Resolves: #1369259 - Fix known zeroed state tracking

* Mon Aug 08 2016 Sinny Kumari <skumari@redhat.com> - 2.4.12.1-1
- Resolves: #1364131 - Integrate various important bug fixes for iprutils in
  RHEL7.3 by updating iprutils to 2.4.12

* Mon Apr 25 2016 Sinny Kumari <skumari@redhat.com> - 2.4.11.1-1
- Resolves: #1274367 - [7.3 FEAT] iprutils package update
- Resolves: #1297921 - IPR: Raid migration fails to kick while executing through command line

* Tue Jun 23 2015 Jakub Čajka <jcajka@redhat.com> - 2.4.8-1
- Resolves: #1182038 - [7.2 FEAT] iprutils package update - ppc64/ppc64le
- Resolves: #1183460 - RHEL7.1 BE: iprutils: Set known zeroed after format

* Tue Jan 06 2015 Jakub Čajka <jcajka@redhat.com> - 2.4.3-3
- Related: #1174371 - Fixed changelog version-release

* Tue Jan 06 2015 Jakub Čajka <jcajka@redhat.com> - 2.4.3-2
- Resolves: #1174371 - [RHEL7.1 LE] migration between raid 0 to raid 10 fails for ZR1

* Thu Sep 04 2014 Jakub Čajka <jcajka@redhat.com> - 2.4.3-1
- Related: #1088562 - [7.1 FEAT] iprutils package update - ppc64

* Tue Sep 02 2014 Jakub Čajka <jcajka@redhat.com> - 2.4.2-2
- Related: #1088562 - removed unnecessary build requirements

* Mon Sep 01 2014 Jakub Čajka <jcajka@redhat.com> - 2.4.2-1
- Resolves: #1088562 - [7.1 FEAT] iprutils package update - ppc64
- Resolves: #1044679 - iprutils should use systemd
- Resolves: #1092519 - iprutils - PIE and RELRO check

* Fri Mar 07 2014 Karsten Hopp <karsten@redhat.com> 2.3.16-4
- add fix for T2 arrays
- Resolves: rhbz 1061166

* Mon Mar 03 2014 Karsten Hopp <karsten@redhat.com> 2.3.16-3
- fix permissions of man pages
- Resolves: rhbz 1061756

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.3.16-2
- Mass rebuild 2014-01-24

* Tue Jan 07 2014 Filip Kocina <fkocina@redhat.com> - 2.3.16-1
- Resolves: #1030303 - update to the latest upstream

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.3.15-2
- Mass rebuild 2013-12-27

* Thu Sep 12 2013 Filip Kocina <fkocina@redhat.com> - 2.3.15-1
- Resolves: #981666 - update to the latest upstream

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 29 2012 Peter Robinson <pbrobinson@fedoraproject.org> 2.3.13-1
- update to 2.3.13

* Tue Sep 11 2012 David Aquilina <dwa@redhat.com> 2.3.11-2
- Prevent the RPM from conflicting with itself (BZ #856330)

* Wed Sep 05 2012 Karsten Hopp <karsten@redhat.com> 2.3.11-1
- update to 2.3.11
- enable on all archs as it now supports some adapters on them, too.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 08 2012 Karsten Hopp <karsten@redhat.com> 2.3.10-1
- update to iprutils-2.3.10

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Jiri Skala <jskala@redhat.com> - 2.3.9-1
- Update to version 2.3.9

* Wed Aug 24 2011 Jiri Skala <jskala@redhat.com> - 2.3.7-1
- Update to version 2.3.7

* Fri Aug 05 2011 Jiri Skala <jskala@redhat.com> - 2.3.6-1
- Update to version 2.3.6

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 09 2011 Jiri Skala <jskala@redhat.com> - 2.3.2-1
- Update to version 2.3.2

* Mon Apr 12 2010 Roman Rakus <rrakus@redhat.com> - 2.2.20-1
- Update to version 2.2.20

* Thu Feb 11 2010 Roman Rakus <rrakus@redhat.com> 2.2.18-3
- added missing man page

* Tue Jan 26 2010 Roman Rakus <rrakus@redhat.com> 2.2.18-2
- moved files from /sbin to /usr/sbin and made symlinks

* Wed Nov 04 2009 Roman Rakus <rrakus@redhat.com> - 2.2.18-1
- Version 2.2.18

* Mon Oct 05 2009 Roman Rakus <rrakus@redhat.com> - 2.2.17-2
- Fixed initscripts (#522464, #522462, #522461)

* Thu Sep 17 2009 Roman Rakus <rrakus@redhat.com> - 2.2.17-1
- Version 2.2.17

* Mon Aug 17 2009 Roman Rakus <rrakus@redhat.com> - 2.2.16-1
- Bump to version 2.2.16

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 2 2009 Will Woods <wwoods@redhat.com> - 2.2.13-2
- Fix iprdump startup - #483340
- iprutils-swab-moved.patch - fix compilation with 2.6.29 kernels (#483643)

* Fri Nov 21 2008 Roman Rakus <rrakus@redhat.com> - 2.2.13-1
- New upstream version

* Wed Jul  2 2008 Roman Rakus <rrakus@redhat.com> - 2.2.8-6
- Fixed ExclusiveArch tag

* Wed Jul  2 2008 Roman Rakus <rrakus@redhat.com> - 2.2.8-5
- Fixed chkconfig issue - #453165

* Wed Apr  9 2008 Roman Rakus <rrakus@redhat.cz> - 2.2.8-4
- Rewrited initscripts for satisfying LSB spec

* Fri Feb 08 2008 David Cantrell <dcantrell@redhat.com> - 2.2.8-2
- Rebuild for gcc-4.3

* Fri Nov 16 2007 David Cantrell <dcantrell@redhat.com> - 2.2.8-1
- Upgrade to latest upstream release

* Mon Oct  1 2007 Jeremy Katz <katzj@redhat.com> - 2.2.6-3
- don't require redhat-lsb (#252343)

* Tue Aug 21 2007 David Cantrell <dcantrell@redhat.com> - 2.2.6-2
- Rebuild

* Thu May 17 2007 Paul Nasrat <pnasrat@redhat.com> - 2.2.6-1
- Update to latest upstream

* Thu Jul 13 2006 Paul Nasrat <pnasrat@redhat.com> - 2.1.5-1
- New upstream version

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.1.4-3.1
- rebuild

* Mon Jul 10 2006 Paul Nasrat <pnasrat@redhat.com> - 2.1.4-3
- Add redhat-lsb requires

* Mon Jul 10 2006 David Woodhouse <dwmw2@redhat.com> - 2.1.4-2
- Rebuild against new sysfsutils

* Mon Jun 26 2006 Paul Nasrat <pnasrat@redhat.com> - 2.1.4-1
- Update to 2.1.4

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.1.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.1.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 23 2005 Paul Nasrat <pnasrat@redhat.com> - 2.1.1-1
- Update to 2.1.1
- Use RPM_OPT_FLAGS

* Tue Aug 02 2005 Paul Nasrat <pnasrat@redhat.com> - 2.0.15.3-1
- update to 2.0.15.3-1

* Wed May 11 2005 Paul Nasrat <pnasrat@redhat.com> - 2.0.14.2-1
- update to 2.0.14.2 (#156934)

* Thu Feb 24 2005 Paul Nasrat <pnasrat@redhat.com> - 2.0.13.7-1
- Update to 2.0.13.7 (#144654)
- Project moved location to sourceforge

* Mon Jan 03 2005 Paul Nasrat <pnasrat@redhat.com> - 2.0.13.5-1
- Update to 2.0.13.5 (#143593)

* Wed Dec  8 2004 Jeremy Katz <katzj@redhat.com> - 2.0.13.4-2
- link dynamically to sysfsutils instead of statically (#142310)

* Wed Dec 08 2004 Paul Nasrat <pnasrat@redhat.com> 2.0.13.4-1
- update to 2.0.13.4 (#142164)

* Fri Dec  3 2004 Jeremy Katz <katzj@redhat.com> - 2.0.13.3-1
- update to 2.0.13.3 (#141707)

* Mon Nov 15 2004 Jeremy Katz <katzj@redhat.com> - 2.0.13.2-1
- update to 2.0.13.2 (#139083)
  - fix firmware upload for firmware in /lib instead of /usr/lib
  - fix sysfs race

* Wed Oct  6 2004 Jeremy Katz <katzj@redhat.com> - 2.0.13-1
- update to 2.0.13 (#128996)

* Tue Aug  3 2004 Jeremy Katz <katzj@redhat.com> - 2.0.12-1
- update to 2.0.12
- include a copy of libsysfs to build

* Tue Jun 15 2004 Jeremy Katz <katzj@redhat.com> - 1.0.7-1
- update to 1.0.7 (#125988)

* Tue May 11 2004 Jeremy Katz <katzj@redhat.com> - 1.0.5-3
- obsolete ipr-utils (old package name)

* Thu Mar 25 2004 Jeremy Katz <katzj@redhat.com> 1.0.5-2
- 1.0.5
- some spec file tweaks

* Tue Nov 25 2003 Brian King <brking@us.ibm.com> 1.0.3-2
- Fixed segmentation fault in iprupdate
