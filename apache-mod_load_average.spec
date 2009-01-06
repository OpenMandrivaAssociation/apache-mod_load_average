#Module-Specific definitions
%define mod_name mod_load_average
%define mod_conf A52_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	0.1.0
Release:	%mkrel 10
Group:		System/Servers
License:	Apache License
URL:		http://svn.force-elite.com/mod_load_average/trunk/src/
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%{_sbindir}/apxs -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


