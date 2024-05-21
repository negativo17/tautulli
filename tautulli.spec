%global user %{name}
%global group %{name}
#global beta 1

Name:           tautulli
Version:        2.14.2
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
* Tue May 21 2024 Simone Caronni <negativo17@gmail.com> - 2.14.2-1
- Update to 2.14.2.

* Tue Dec 12 2023 Simone Caronni <negativo17@gmail.com> - 2.13.4-1
- Update to 2.13.4.

* Tue Oct 31 2023 Simone Caronni <negativo17@gmail.com> - 2.13.2-1
- Update to 2.13.2.

* Sun Aug 27 2023 Simone Caronni <negativo17@gmail.com> - 2.13.1-1
- Update to 2.13.1.
- Trim changelog.

* Tue Jul 18 2023 Simone Caronni <negativo17@gmail.com> - 2.12.5-1
- Update to 2.12.5.

* Sat May 27 2023 Simone Caronni <negativo17@gmail.com> - 2.12.4-1
- Update to 2.12.4.

* Thu Apr 27 2023 Simone Caronni <negativo17@gmail.com> - 2.12.3-1
- Update to 2.12.3.

* Sun Mar 26 2023 Simone Caronni <negativo17@gmail.com> - 2.12.2-1
- Update to 2.12.2.

* Fri Dec 23 2022 Simone Caronni <negativo17@gmail.com> - 2.11.1-1
- Update to 2.11.1.

* Thu Nov 10 2022 Simone Caronni <negativo17@gmail.com> - 2.10.5-1
- Update to 2.10.5.

* Wed Sep 21 2022 Simone Caronni <negativo17@gmail.com> - 2.10.4-1
- Update to 2.10.4.

* Wed Aug 10 2022 Simone Caronni <negativo17@gmail.com> - 2.10.3-1
- Update to 2.10.3.

* Tue Jul 05 2022 Simone Caronni <negativo17@gmail.com> - 2.10.2-1
- Update to 2.10.2.

* Wed Jun 01 2022 Simone Caronni <negativo17@gmail.com> - 2.10.1-1
- Update to 2.10.1.

* Tue May 24 2022 Simone Caronni <negativo17@gmail.com> - 2.10.0-1
- Update to 2.10.0.

* Sun Apr 17 2022 Simone Caronni <negativo17@gmail.com> - 2.9.7-1
- Update to 2.9.7.

* Wed Feb 16 2022 Simone Caronni <negativo17@gmail.com> - 2.9.4-1
- Update to 2.9.4.

* Sat Feb 12 2022 Simone Caronni <negativo17@gmail.com> - 2.9.3-1
- Update to 2.9.3.

* Thu Jan 13 2022 Simone Caronni <negativo17@gmail.com> - 2.8.1-1
- Update to 2.8.1.
