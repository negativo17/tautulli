%global user %{name}
%global group %{name}
#global beta 1

Name:           tautulli
Version:        2.15.3
Release:        1%{?dist}
Summary:        A Python based monitoring and tracking tool for Plex Media Server
License:        GPLv3
URL:            http://tautulli.com
BuildArch:      noarch

Source0:        https://github.com/Tautulli/Tautulli/archive/v%{version}%{?beta:-beta}.tar.gz#/%{name}-%{version}%{?beta:-beta}.tar.gz
Source10:       %{name}.service
Source11:       %{name}.xml

BuildRequires:  firewalld-filesystem
BuildRequires:  systemd
BuildRequires:  tar

Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem
Requires:       python3 >= 3.8
Requires:       python3-pycryptodomex
Requires(pre):  shadow-utils

%description
A python based web application for monitoring, analytics and notifications for
Plex Media Server.

%prep
%autosetup -n Tautulli-%{version}%{?beta:-beta} -p1

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_prefix}/lib/firewalld/services/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}

# Changelog is displayed in the GUI:
cp -fr data lib plexpy PlexPy.py pylintrc Tautulli.py CHANGELOG.md %{buildroot}%{_datadir}/%{name}

install -m 0644 -p %{SOURCE10} %{buildroot}%{_unitdir}/%{name}.service
install -m 0644 -p %{SOURCE11} %{buildroot}%{_prefix}/lib/firewalld/services/%{name}.xml

find %{buildroot} -name "*.py" -exec sed -i \
    -e 's|/usr/bin/env python.*|/usr/bin/python3|g' \
    -e 's|/usr/bin/python.*|/usr/bin/python3|g' {} \;

find %{buildroot} \( -name "*.js" -o -name "*.css" \) -exec chmod 644 {} \;

%pre
getent group %{group} >/dev/null || groupadd -r %{group}
getent passwd %{user} >/dev/null || \
    useradd -r -g %{group} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "%{name}" %{user}
exit 0

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
%{_unitdir}/%{name}.service

%changelog
* Fri Aug 08 2025 Simone Caronni <negativo17@gmail.com> - 2.15.3-1
- Update to 2.15.3.

* Sun Apr 13 2025 Simone Caronni <negativo17@gmail.com> - 2.15.2-1
- Update to 2.15.2.
- Trim changelog.

* Fri Mar 14 2025 Simone Caronni <negativo17@gmail.com> - 2.15.1-1
- Update to 2.15.1.

* Mon Nov 25 2024 Simone Caronni <negativo17@gmail.com> - 2.15.0-1
- Update to 2.15.0.

* Sun Oct 20 2024 Simone Caronni <negativo17@gmail.com> - 2.14.6-1
- Update to 2.14.6.

* Tue Sep 24 2024 Simone Caronni <negativo17@gmail.com> - 2.14.5-1
- Update to 2.14.5.

* Sun Aug 18 2024 Simone Caronni <negativo17@gmail.com> - 2.14.4-1
- Update to 2.14.4.

* Mon Jun 24 2024 Simone Caronni <negativo17@gmail.com> - 2.14.3-1
- Update to 2.14.3.

* Tue May 21 2024 Simone Caronni <negativo17@gmail.com> - 2.14.2-1
- Update to 2.14.2.
