%global debug_package   %{nil}

Name:		etcd
Version:	3.2.9
Release:	1%{?dist}
Summary:	A highly-available key value store for shared configuration
License:	ASL 2.0
URL:		https://github.com/coreos/%{name}
Source1:	%{name}.service
Source2:	%{name}.conf

%description
A highly-available key value store for shared configuration.


%prep
export GOPATH=/usr/share/gocode
export PATH=$GOPATH/bin:$PATH


%build


%install
cd $GOPATH/src/github.com/coreos/etcd
install -D -p -m 0755 bin/%{name} %{buildroot}%{_bindir}/%{name}
install -D -p -m 0755 bin/%{name}ctl %{buildroot}%{_bindir}/%{name}ctl
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 -t %{buildroot}%{_sysconfdir}/%{name} %{SOURCE2}
# And create /var/lib/etcd
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}


%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin -c "etcd user" %{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service


%files
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_bindir}/%{name}ctl
%dir %attr(-,%{name},%{name}) %{_sharedstatedir}/%{name}
%{_unitdir}/%{name}.service


%changelog
* Tue Nov 07 2017 Allan Hung <hung.allan@gmail.com> - 3.2.9-1
- Update to 3.2.9
