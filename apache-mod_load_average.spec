#Module-Specific definitions
%define mod_name mod_load_average
%define mod_conf A52_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	0.1.0
Release:	16
Group:		System/Servers
License:	Apache License
URL:		https://svn.force-elite.com/mod_load_average/trunk/src/
# http://issues.apache.org/bugzilla/show_bug.cgi?id=29122
Source0: 	http://svn.force-elite.com/svn/mod_load_average/trunk/src/mod_load_average.c.bz2
Source1:	%{mod_conf}.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0

%description
mod_load_average uses the getloadavg function to determine if the
request should be serviced. The module has two operating Modes.

First, it has an absolute max load average, if this is reached,
all requests will be rejected with a 503.

The 2nd mode uses the handler type to determine the maximum load
under which they will be served. This enables you for example to
disable PHP or CGI under high loads, but still serve images and
plain html.

%prep

%setup -q -c -T -n %{mod_name}-%{version}
bzcat %{SOURCE0} > %{mod_name}.c

%build

%{_bindir}/apxs -c %{mod_name}.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-15mdv2012.0
+ Revision: 772675
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-14
+ Revision: 678334
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-13mdv2011.0
+ Revision: 588018
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-12mdv2010.1
+ Revision: 516136
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-11mdv2010.0
+ Revision: 406606
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-10mdv2009.1
+ Revision: 325809
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-9mdv2009.0
+ Revision: 234983
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-8mdv2009.0
+ Revision: 215597
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-7mdv2008.1
+ Revision: 181795
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 0.1.0-6mdv2008.1
+ Revision: 170733
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-5mdv2008.0
+ Revision: 82604
- rebuild

* Fri Aug 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-4mdv2008.0
+ Revision: 61211
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-3mdv2007.1
+ Revision: 140710
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-2mdv2007.0
+ Revision: 79451
- Import apache-mod_load_average

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-2mdv2007.0
- rebuild

* Wed Mar 01 2006 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdk
- initial Mandriva package

