%global user %{name}
%global group %{name}
%global __python %{__python2}

Name:           tautulli
Version:        2.1.21
Release:        1%{?dist}
Summary:        A Python based monitoring and tracking tool for Plex Media Server
License:        GPLv3
URL:            http://tautulli.com
BuildArch:      noarch

Source0:        https://github.com/Tautulli/Tautulli/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source10:       %{name}.service
Source11:       %{name}.xml

BuildRequires:  firewalld-filesystem
BuildRequires:  systemd
BuildRequires:  tar

Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem
Requires:       python2
Requires:       python2-pycryptodomex
Requires(pre):  shadow-utils

%description
A python based web application for monitoring, analytics and notifications for
Plex Media Server.

%prep
%autosetup -n Tautulli-%{version}

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_prefix}/lib/firewalld/services/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}

cp -fr * %{buildroot}%{_datadir}/%{name}

install -m 0644 -p %{SOURCE10} %{buildroot}%{_unitdir}/%{name}.service
install -m 0644 -p %{SOURCE11} %{buildroot}%{_prefix}/lib/firewalld/services/%{name}.xml

# Always invoke Python 2
find %{buildroot} -name "*.py" -exec sed -i \
    -e 's|/usr/bin/env python|/usr/bin/env python2|g' \
    -e 's|/usr/bin/python|/usr/bin/env python2|g' {} \;

find %{buildroot} \( -name "*.js" -o -name "*.css" \) -exec chmod 644 {} \;

rm -fr %{buildroot}%{_datadir}/%{name}/{README.md,API.md,LICENSE,.gitignore,init-scripts,contrib}

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
%doc README.md CHANGELOG.md API.md
%attr(750,%{user},%{group}) %{_sharedstatedir}/%{name}
%attr(750,%{user},%{group}) %{_sysconfdir}/%{name}
%ghost %config %{_sysconfdir}/%{name}/config.ini
%{_datadir}/%{name}
%{_prefix}/lib/firewalld/services/%{name}.xml
%{_unitdir}/%{name}.service

%changelog
* Thu Sep 27 2018 Simone Caronni <negativo17@gmail.com> - 2.1.21-1
- Update to 2.1.21.

* Tue Aug 21 2018 Simone Caronni <negativo17@gmail.com> - 2.1.19-1
- Update to 2.1.19.

* Sat Jul 21 2018 Simone Caronni <negativo17@gmail.com> - 2.1.16-1
- First build.
