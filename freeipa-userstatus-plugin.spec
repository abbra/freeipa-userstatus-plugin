# This spec file provides facilities to build FreeIPA external plugins for both
# Fedora and RHEL (EPEL). Support for external plugins was added to FreeIPA in
# 4.4.1 (and backported to RHEL in IdM version 4.4.0) For Fedora 27 or later we
# package both Python 2 and Python 3 versions in parallel. Fedora 27 defaults
# to Python 3 but one can force FreeIPA server to run under Python 2 with
# removal of python3-mod_wsgi (and install of mod_wsgi instead).
#
# Since this is an example how to package FreeIPA plugins, we include both
# client and server side components, thus creating five different packages:
# - main package (freeipa-<plugin_name>) that holds LDAP schema and JS code
# - server and client packages for Python 2
# - server and client packages for Python 3

%global debug_package %{nil}
%global plugin_name userstatus

%global ipa_python2_sitelib %{python2_sitelib}
%if 0%{?fedora} > 26 || 0%{?rhel} > 7
%global ipa_python3_sitelib %{python3_sitelib}
%endif

Name:           freeipa-%{plugin_name}-plugin
Version:        0.0.2
Release:        1%{?dist}
Summary:        A module for FreeIPA to add 'user status' field to user properties

BuildArch:      noarch

License:        GPL
URL:            https://github.com/abbra/freeipa-%{plugin_name}-plugin
Source0:        freeipa-%{plugin_name}-plugin-%{version}.tar.gz

# Python3 support was added in Fedora 27 with FreeIPA 4.6
%if 0%{?fedora} > 26 || 0%{?rhel} > 7
BuildRequires: python3-devel
BuildRequires: python3-ipaserver >= 4.6.0
%endif


# In RHEL 7 a version of IPA which supports external plugins was introduced
# with a rebase to 4.4.0 and backports to it, so set expectations properly --
# in upstream it was added in 4.4.1.
%if 0%{?rhel}
BuildRequires: python2-devel
BuildRequires: python2-ipaserver >= 4.4.0
Requires:      ipa-server-common >= 4.4.0
%else
BuildRequires:  python2-devel
BuildRequires:  python2-ipaserver >= 4.4.1
Requires:       ipa-server-common >= 4.4.1
%endif

# In Fedora 27 we have FreeIPA using Python 3, enforce that
%if 0%{?fedora} > 26 || 0%{?rhel} > 7
Requires(post): python3-ipa-%{plugin_name}-server
Requires: python3-ipa-%{plugin_name}-server
Requires: python3-ipa-%{plugin_name}-client
%else
Requires(post): python2-ipa-%{plugin_name}-server
Requires: python2-ipa-%{plugin_name}-server
Requires: python2-ipa-%{plugin_name}-client
%endif

%description
A module for FreeIPA to add 'user status' field to user properties

%package -n python2-ipa-%{plugin_name}-server
Summary: Server side of a module for FreeIPA to add 'user status' field to user properties
License:        GPL
Requires: python2-ipaserver
Requires: python3-ipa-%{plugin_name}-client

%description  -n python2-ipa-%{plugin_name}-server
A module for FreeIPA to add 'user status' field to user properties
This package adds server-side support for Python 2 version of FreeIPA

%package -n python2-ipa-%{plugin_name}-client
Summary: Server side of a module for FreeIPA to add 'user status' field to user properties
License:        GPL
Requires: python2-ipaclient

%description  -n python2-ipa-%{plugin_name}-client
A module for FreeIPA to add 'user status' field to user properties
This package adds client-side support for Python 2 version of FreeIPA

%if 0%{?fedora} > 26 || 0%{?rhel} > 7
%package -n python3-ipa-%{plugin_name}-server
Summary: Server side of a module for FreeIPA to add 'user status' field to user properties
License:        GPL
Requires: python3-ipaserver
Requires: python3-ipa-%{plugin_name}-client

%description  -n python3-ipa-%{plugin_name}-server
A module for FreeIPA to add 'user status' field to user properties
This package adds server-side support for Python 3 version of FreeIPA

%package -n python3-ipa-%{plugin_name}-client
Summary: Server side of a module for FreeIPA to add 'user status' field to user properties
License:        GPL
Requires: python3-ipaclient

%description  -n python3-ipa-%{plugin_name}-client
A module for FreeIPA to add 'user status' field to user properties
This package adds client-side support for Python 3 version of FreeIPA

%endif

%prep
%autosetup

%build
touch debugfiles.list

%install
rm -rf $RPM_BUILD_ROOT
%__mkdir_p %buildroot/%_datadir/ipa/schema.d
%__mkdir_p %buildroot/%_datadir/ipa/updates
%__mkdir_p %buildroot/%_datadir/ipa/ui/js/plugins/%{plugin_name}

sitelibs=%{ipa_python2_sitelib}
%if 0%{?fedora} > 26 || 0%{?rhel} > 7
sitelibs="$sitelibs %{ipa_python3_sitelib}"
%endif

for s in $sitelibs ; do
    %__mkdir_p %buildroot/$s/ipaclient/plugins
    %__mkdir_p %buildroot/$s/ipaserver/plugins

    for i in ipaclient ipaserver ; do
        for j in $(find plugin/$i/plugins -name '*.py') ; do
            %__cp $j %buildroot/$s/$i/plugins
        done
    done
done

for j in $(find plugin/schema.d -name '*.ldif') ; do
    %__cp $j %buildroot/%_datadir/ipa/schema.d
done

for j in $(find plugin/updates -name '*.update') ; do
    %__cp $j %buildroot/%_datadir/ipa/updates
done

for j in $(find plugin/ui/ -name '*.js') ; do
    %__cp $j %buildroot/%_datadir/ipa/ui/js/plugins/%{plugin_name}
done

%posttrans
%if 0%{?fedora} > 26 || 0%{?rhel} > 7
ipa_interp=python3
%else
ipa_interp=python2
%endif
$ipa_interp -c "import sys; from ipaserver.install import installutils; sys.exit(0 if installutils.is_ipa_configured() else 1);" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    # This must be run in posttrans so that updates from previous
    # execution that may no longer be shipped are not applied.
    /usr/sbin/ipa-server-upgrade --quiet >/dev/null || :

    # Restart IPA processes. This must be also run in postrans so that plugins
    # and software is in consistent state
    # NOTE: systemd specific section

    /bin/systemctl is-enabled ipa.service >/dev/null 2>&1
    if [  $? -eq 0 ]; then
        /bin/systemctl restart ipa.service >/dev/null 2>&1 || :
    fi
fi

%files
%license COPYING
%doc plugin/Feature.mediawiki
%_datadir/ipa/schema.d/*
%_datadir/ipa/updates/*
%_datadir/ipa/ui/js/plugins/%{plugin_name}/*

%files -n python2-ipa-%{plugin_name}-client
%ipa_python2_sitelib/ipaclient/plugins/*

%files -n python2-ipa-%{plugin_name}-server
%ipa_python2_sitelib/ipaserver/plugins/*

%if 0%{?fedora} > 26 || 0%{?rhel} > 7
%files -n python3-ipa-%{plugin_name}-client
%ipa_python3_sitelib/ipaclient/plugins/*

%files -n python3-ipa-%{plugin_name}-server
%ipa_python3_sitelib/ipaserver/plugins/*
%endif


%changelog
* Tue Dec 05 2017 Alexander Bokovoy <abokovoy@redhat.com> 0.0.2-1
- Support both py2 and py3 versions of FreeIPA server

* Thu Nov  9 2017 Alexander Bokovoy <abokovoy@redhat.com> 0.0.1-1
- Initial release

