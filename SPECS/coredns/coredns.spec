%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        CoreDNS
Name:           coredns
Version:        1.7.0
Release:        1%{?dist}
License:        Apache License 2.0
URL:            https://github.com/coredns/coredns/releases/v%{version}.tar.gz
Source0:        coredns-%{version}.tar.gz
%define sha1 coredns=61bf65cfcc29abf941d486bc669a283a71666ee5
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  git
%define debug_package %{nil}

%description
CoreDNS is a DNS server that chains plugins

%prep -p exit
%setup -qn coredns-%{version}

%build
export ARCH=%{gohostarch}
export VERSION=%{version}
export PKG=github.com/%{name}/%{name}
export GOARCH=${ARCH}
export GOHOSTARCH=${ARCH}
export GOOS=linux
export GOHOSTOS=linux
export GOROOT=/usr/lib/golang
export GOPATH=/usr/share/gocode
export GOBIN=/usr/share/gocode/bin
export PATH=$PATH:$GOBIN
mkdir -p ${GOPATH}/src/${PKG}
cp -rf . ${GOPATH}/src/${PKG}
pushd ${GOPATH}/src/${PKG}
# Just download (do not compile), since it's not compilable with go-1.9.
# TODO: use prefetched tarball instead.
sed -i 's#go get -u github.com/mholt/caddy#go get -u -d github.com/mholt/caddy#' Makefile
sed -i 's#go get -u github.com/miekg/dns#go get -u -d github.com/miekg/dns#' Makefile
make

%install
install -m 755 -d %{buildroot}%{_bindir}
install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/%{name}/%{name}/coredns

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/coredns

%changelog
*   Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-1
-   Automatic Version Bump
*   Sun Sep 22 2019 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-3
-   Fix compilation issue (do not compile mholt/caddy).
*   Sun Sep 23 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-2
-   Fix compilation issue.
-   aarch64 support.
*   Fri Aug 03 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.2.0-1
-   Initial version of coredns 1.2.0.
