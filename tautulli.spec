%global gittag0 %{version}-beta
%global user %{name}
%global group %{name}
%global __python %{__python2}

Name:           tautulli
Version:        2.1.16
Release:        1%{?dist}
Summary:        A Python based monitoring and tracking tool for Plex Media Server
License:        GPLv3
URL:            http://tautulli.com
BuildArch:      noarch

Source0:        https://github.com/Tautulli/Tautulli/archive/v%{gittag0}.tar.gz#/%{name}-%{gittag0}.tar.gz
Source10:       %{name}.service
Source11:       %{name}.xml

BuildRequires:  firewalld-filesystem
BuildRequires:  systemd
BuildRequires:  tar

Requires:       python2
Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem

%description
A python based web application for monitoring, analytics and notifications for
Plex Media Server.

%prep
%autosetup -n Tautulli-%{gittag0}

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

rm -fr %{buildroot}%{_datadir}/%{name}/{*.md,LICENSE,.gitignore,init-scripts,contrib}

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
%ghost %{_sysconfdir}/%{name}/config.ini
%{_datadir}/%{name}
%{_prefix}/lib/firewalld/services/%{name}.xml
%{_unitdir}/%{name}.service

%changelog
* Sat Jul 21 2018 Simone Caronni <negativo17@gmail.com> - 2.1.16-1
- First build.
