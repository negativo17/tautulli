%global user %{name}
%global group %{name}
#global beta 1

Name:           tautulli
Version:        2.7.4
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
Requires:       python3
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
* Sun Jun 20 2021 Simone Caronni <negativo17@gmail.com> - 2.7.4-1
- Update to 2.7.4.

* Sun May 23 2021 Simone Caronni <negativo17@gmail.com> - 2.7.3-1
- Update to 2.7.3.

* Wed May 05 2021 Simone Caronni <negativo17@gmail.com> - 2.7.2-1
- Update to 2.7.2.

* Wed Apr 21 2021 Simone Caronni <negativo17@gmail.com> - 2.7.0-1
- Update to 2.7.0.

* Thu Feb 11 2021 Simone Caronni <negativo17@gmail.com> - 2.6.6-1
- Update to 2.6.6.

* Thu Jan 21 2021 Simone Caronni <negativo17@gmail.com> - 2.6.5-1
- Update to 2.6.5.

* Sat Dec 26 2020 Simone Caronni <negativo17@gmail.com> - 2.6.4-1
- Update to 2.6.4.

* Tue Dec 08 2020 Simone Caronni <negativo17@gmail.com> - 2.6.2-1
- Update to 2.6.2.

* Thu Nov 05 2020 Simone Caronni <negativo17@gmail.com> - 2.6.1-1
- Update to 2.6.1.

* Thu Oct 29 2020 Simone Caronni <negativo17@gmail.com> - 2.6.0-1
- Update to 2.6.0-beta.

* Tue Oct 06 2020 Simone Caronni <negativo17@gmail.com> - 2.5.6-1
- Update to 2.5.6.

* Sun Aug 16 2020 Simone Caronni <negativo17@gmail.com> - 2.5.4-1
- Update to 2.5.4.

* Tue Jul 14 2020 Simone Caronni <negativo17@gmail.com> - 2.5.3-1
- Update to 2.5.3.

* Fri May 22 2020 Simone Caronni <negativo17@gmail.com> - 2.2.4-1
- Update to 2.2.4.

* Wed Apr 01 2020 Simone Caronni <negativo17@gmail.com> - 2.2.1-1
- Update to 2.2.1.

* Fri Feb 21 2020 Simone Caronni <negativo17@gmail.com> - 2.1.44-2
- Enforce Python 2 in main script.

* Thu Feb 06 2020 Simone Caronni <negativo17@gmail.com> - 2.1.44-1
- Update to 2.1.44.

* Sat Dec 21 2019 Simone Caronni <negativo17@gmail.com> - 2.1.39-1
- Update to 2.1.39.

* Sun Dec 01 2019 Simone Caronni <negativo17@gmail.com> - 2.1.38-1
- Update to 2.1.38.

* Wed Oct 02 2019 Simone Caronni <negativo17@gmail.com> - 2.1.35-1
- Update to 2.1.35-beta.

* Sun Sep 08 2019 Simone Caronni <negativo17@gmail.com> - 2.1.34-1
- Update to 2.1.34.

* Tue Jul 09 2019 Simone Caronni <negativo17@gmail.com> - 2.1.32-1
- Update to 2.1.32.

* Sun Jun 16 2019 Simone Caronni <negativo17@gmail.com> - 2.1.31-1
- Update to 2.1.31-beta.

* Mon May 27 2019 Simone Caronni <negativo17@gmail.com> - 2.1.30-1
- Update to 2.1.30-beta.

* Tue Apr 30 2019 Simone Caronni <negativo17@gmail.com> - 2.1.29-1
- Update to 2.1.29-beta.

* Mon Apr 01 2019 Simone Caronni <negativo17@gmail.com> - 2.1.28-1
- Update to 2.1.28.

* Sun Mar 10 2019 Simone Caronni <negativo17@gmail.com> - 2.1.27-1
- Update to 2.1.27-beta.

* Sun Dec 09 2018 Simone Caronni <negativo17@gmail.com> - 2.1.26-1
- Update to 2.1.26.

* Sun Nov 25 2018 Simone Caronni <negativo17@gmail.com> - 2.1.25-1
- Update to 2.1.25.

* Sun Oct 28 2018 Simone Caronni <negativo17@gmail.com> - 2.1.23-1
- Update to 2.1.23.

* Wed Oct 10 2018 Simone Caronni <negativo17@gmail.com> - 2.1.22-1
- Update to 2.1.22.

* Thu Sep 27 2018 Simone Caronni <negativo17@gmail.com> - 2.1.21-1
- Update to 2.1.21.

* Tue Aug 21 2018 Simone Caronni <negativo17@gmail.com> - 2.1.19-1
- Update to 2.1.19.

* Sat Jul 21 2018 Simone Caronni <negativo17@gmail.com> - 2.1.16-1
- First build.
