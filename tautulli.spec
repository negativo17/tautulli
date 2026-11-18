%global user %{name}
%global group %{name}
#global beta 1

Name:           tautulli
Version:        2.19.1
Release:        1%{?dist}
Summary:        A Python based monitoring and tracking tool for Plex Media Server
License:        GPLv3
URL:            http://tautulli.com
BuildArch:      noarch

Source0:        https://github.com/Tautulli/Tautulli/archive/v%{version}%{?beta:-beta}.tar.gz#/%{name}-%{version}%{?beta:-beta}.tar.gz
Source10:       %{name}.service
Source11:       %{name}.xml
Source12:       %{name}.sysusers.conf

BuildRequires:  firewalld-filesystem
BuildRequires:  systemd-rpm-macros

Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem
Requires:       python3 >= 3.8
Requires:       python3-pycryptodomex

%description
A python based web application for monitoring, analytics and notifications for
Plex Media Server.

%prep
%autosetup -n Tautulli-%{version}%{?beta:-beta} -p1

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}

# Changelog is displayed in the GUI:
cp -fr data lib plexpy PlexPy.py pylintrc Tautulli.py CHANGELOG.md %{buildroot}%{_datadir}/%{name}

install -D -m 0644 -p %{SOURCE10} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 0644 -p %{SOURCE11} %{buildroot}%{_prefix}/lib/firewalld/services/%{name}.xml
install -D -m 0644 -p %{SOURCE12} %{buildroot}%{_sysusersdir}/%{name}.conf

find %{buildroot} -name "*.py" -exec sed -i \
    -e 's|/usr/bin/env python.*|/usr/bin/python3|g' \
    -e 's|/usr/bin/python.*|/usr/bin/python3|g' {} \;

find %{buildroot} \( -name "*.js" -o -name "*.css" \) -exec chmod 644 {} \;

%post
%systemd_post %{name}.service
%firewalld_reload

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%doc API.md README.md
%attr(750,%{user},%{group}) %{_sharedstatedir}/%{name}
%attr(750,%{user},%{group}) %{_sysconfdir}/%{name}
%ghost %config %{_sysconfdir}/%{name}/config.ini
%{_datadir}/%{name}
%{_prefix}/lib/firewalld/services/%{name}.xml
%{_sysusersdir}/%{name}.conf
%{_unitdir}/%{name}.service

%changelog
* Wed Nov 18 2026 Simone Caronni <negativo17@gmail.com> - 2.19.1-1
- Update to 2.19.1.

* Tue Sep 29 2026 Simone Caronni <negativo17@gmail.com> - 2.18.2-1
- Update to 2.18.2.

* Thu Sep 17 2026 Simone Caronni <negativo17@gmail.com> - 2.18.1-1
- Update to 2.18.1.

* Wed Jun 17 2026 Simone Caronni <negativo17@gmail.com> - 2.17.1-2
- Update to 2.17.2.

* Wed May 06 2026 Simone Caronni <negativo17@gmail.com> - 2.17.1-1
- Update to 2.17.1.

* Thu Apr 09 2026 Simone Caronni <negativo17@gmail.com> - 2.17.0-1
- Update to 2.17.0.

* Mon Feb 16 2026 Simone Caronni <negativo17@gmail.com> - 2.16.1-1
- Update to 2.16.1.
