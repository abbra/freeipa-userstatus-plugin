# A user status plugin example for freeIPA

![](userstatus.png)

User status plugin demonstrates how to extend both freeIPA Python framework and
freeIPA Web UI. It provides enough components and RPM spec file to maintain the
changes separate from freeIPA core.

The 'user status' is an imaginary field stored in the user object in freeIPA
that allows other users to see whether this user is active in executing some
tasks or is not available for a task execution.

[See plugin/Feature.mediawiki](plugin/Feature.mediawiki) for detailed explanation.

Steps to build sample

$ sudo dnf -y install rpm-build rpmdevtools
$ rpmdev-setuptree
$ git archive --prefix freeipa-userstatus-plugin-0.0.2/ -o freeipa-userstatus-plugin-0.0.2.tar.gz HEAD
$ cp freeipa-userstatus-plugin-0.0.2.tar.gz ~/rpmbuild/SOURCES/
$ rpmbuild -ba freeipa-userstatus-plugin.spec

The packages will be in ~/rpmbuild/RPMS/noarch/
