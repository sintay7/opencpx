###############################################################################
#
# opencpx SPEC file
#
###############################################################################

Name:		opencpx
Version:	0.12
Release:	1%{?dist}
Summary:	Open Control Panel X
Group:		Applications/Internet
License:	GPL
Source:         %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)

Requires:	perl
Requires:	httpd
Requires:	mod_perl
Requires:	perl-libapreq2
Requires:	perl-XML-LibXSLT
Requires:	pam-devel
Requires:	openssl
Requires:	libxml2
Requires:	libxslt
Requires:	perl-MIME-Types
Requires:	perl-Authen-PAM
Requires:	perl-Crypt-CBC
Requires:	perl-Crypt-Rijndael
Requires:	perl-Authen-SASL
Requires:	perl-Config-Crontab
Requires:	perl-Config-Savelogs
Requires:	perl-Email-Valid
Requires:	perl-Net-SMTP-TLS
Requires:	perl-Encode-EUCJPMS
Requires:	perl-Text-Iconv
Requires:	perl-Quota
Requires:	perl-Text-vCard
Requires:	perl-Encode-HanExtra
Requires:	perl-Encode-IMAPUTF7
Requires:	perl-Mail-Cclient
Requires:	perl-Data-UUID
Requires:	perl-XML-SimpleObject
Requires:	perl-HTML-Scrubber-StripScripts
Requires:	spamassassin

%description
The Open Control Panel X is this, that, the other, and then some.

%prep
%setup -q -c -n %{name}-%{version}
#%autosetup

%build

%install
mkdir -p $RPM_BUILD_ROOT/usr/local/cp/
cp -Rp $RPM_BUILD_DIR/%{name}-%{version}/cp $RPM_BUILD_ROOT/usr/local/
mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d/
cp -p $RPM_BUILD_ROOT/usr/local/cp/etc/conf.d/opencpx.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/perl_opencpx.conf
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig/iptables
cp -p $RPM_BUILD_ROOT/usr/local/cp/etc/fwlevels/DEFAULT $RPM_BUILD_ROOT/etc/sysconfig/iptables
mkdir -p $RPM_BUILD_ROOT/usr/local/share/cpx
cp -p $RPM_BUILD_ROOT/usr/local/cp/share/monitor_prefs.template $RPM_BUILD_ROOT/usr/local/share/cpx
cp -p $RPM_BUILD_ROOT/usr/local/cp/share/site_prefs.template $RPM_BUILD_ROOT/usr/local/share/cpx

mkdir -p $RPM_BUILD_ROOT/etc/init.d/
cp -p $RPM_BUILD_ROOT/usr/local/cp/etc/rc.d/init.d/vsapd $RPM_BUILD_ROOT/etc/init.d/vsapd


%post
if [ -x /sbin/chkconfig ]; then
  /sbin/chkconfig --add vsapd
else
   for i in 2 3 4 5; do
        ln -sf $RPM_BUILD_ROOT/etc/init.d/vsapd  $RPM_BUILD_ROOT/etc/rc.d/rc${i}.d/S46vsapd
   done
   for i in 1 6; do
        ln -sf  $RPM_BUILD_ROOT/etc/init.d/vsapd  $RPM_BUILD_ROOT/etc/rc.d/rc${i}.d/K64vsapd
   done
fi

## setup the convience dirs that opencpx expects.
mkdir /www
ln -s /var/www/cgi-bin /www/cgi-bin
ln -s /etc/httpd/conf /www/conf
ln -s /etc/httpd/conf.d /www/conf.d
ln -s /var/www/html /www/htdocs
ln -s /usr/lib64/httpd/modules /www/libexec
ln -s /var/log/httpd /www/logs
ln -s /usr/lib64/httpd/modules /www/modules

## configure some system settings. 
setsebool -P httpd_can_network_connect 1
groupadd --gid 104 mailgrp
groupadd --gid 500 admin
useradd -m -d /home/admin -g admin -G wheel -c "Server Admin" -s /sbin/nologin --uid 500 admin
passwd admin
service iptables restart
service httpd restart
service vsapd start

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/etc/httpd/conf.d/perl_opencpx.conf
/etc/init.d/vsapd
/etc/sysconfig/iptables/DEFAULT
/usr/local/share/cpx/monitor_prefs.template
/usr/local/share/cpx/site_prefs.template
/usr/local/cp/images
/usr/local/cp/strings/en
/usr/local/cp/strings/ja
/usr/local/cp/RELEASE
/usr/local/cp/bin/site_prefs
/usr/local/cp/cpimages/brandx/file_sound.gif
/usr/local/cp/cpimages/brandx/file_html.gif
/usr/local/cp/cpimages/brandx/MailFilters.png
/usr/local/cp/cpimages/brandx/file_link_hidden.gif
/usr/local/cp/cpimages/brandx/icon-mailboxoptions.gif
/usr/local/cp/cpimages/brandx/contract.gif
/usr/local/cp/cpimages/brandx/logo_placeholder_cp.jpg
/usr/local/cp/cpimages/brandx/folder_sys_link_hidden.gif
/usr/local/cp/cpimages/brandx/EmailAddresses.png
/usr/local/cp/cpimages/brandx/logo_placeholder_login.jpg
/usr/local/cp/cpimages/brandx/icon-mailboxoptionsSml.png
/usr/local/cp/cpimages/brandx/read.gif
/usr/local/cp/cpimages/brandx/icon-webmailoptions.png
/usr/local/cp/cpimages/brandx/AddressBook.png
/usr/local/cp/cpimages/brandx/DomainManagement.png
/usr/local/cp/cpimages/brandx/helpAdditionalSml.png
/usr/local/cp/cpimages/brandx/1header.jpg
/usr/local/cp/cpimages/brandx/logo_placeholder_help.jpg
/usr/local/cp/cpimages/brandx/UserManagement.png
/usr/local/cp/cpimages/brandx/mailManagement.png
/usr/local/cp/cpimages/brandx/Profile.png
/usr/local/cp/cpimages/brandx/icon-foldermgmt.gif
/usr/local/cp/cpimages/brandx/important.gif
/usr/local/cp/cpimages/brandx/icon-mailmgt.gif
/usr/local/cp/cpimages/brandx/folder_sys_hidden.gif
/usr/local/cp/cpimages/brandx/attachment.gif
/usr/local/cp/cpimages/brandx/icon-usermgt.gif
/usr/local/cp/cpimages/brandx/FileManagement.png
/usr/local/cp/cpimages/brandx/myPreferences.png
/usr/local/cp/cpimages/brandx/spamassassin_logo.png
/usr/local/cp/cpimages/brandx/guagemarker.gif
/usr/local/cp/cpimages/brandx/file_hidden.gif
/usr/local/cp/cpimages/brandx/clam.gif
/usr/local/cp/cpimages/brandx/icon-addressbook.png
/usr/local/cp/cpimages/brandx/unread-status.gif
/usr/local/cp/cpimages/brandx/minusIcon.gif
/usr/local/cp/cpimages/brandx/helpCategorySml.png
/usr/local/cp/cpimages/brandx/folder_sys_link.gif
/usr/local/cp/cpimages/brandx/green_success.png
/usr/local/cp/cpimages/brandx/logo_placeholder_mail.jpg
/usr/local/cp/cpimages/brandx/file_image.gif
/usr/local/cp/cpimages/brandx/folder_compressed.gif
/usr/local/cp/cpimages/brandx/folder_parent.gif
/usr/local/cp/cpimages/brandx/AdvancedHelp.png
/usr/local/cp/cpimages/brandx/1userMgmntIcon.jpg
/usr/local/cp/cpimages/brandx/icon-addressbook.gif
/usr/local/cp/cpimages/brandx/icon-mailfilters.gif
/usr/local/cp/cpimages/brandx/sort_arrow_up.gif
/usr/local/cp/cpimages/brandx/check_enabled.gif
/usr/local/cp/cpimages/brandx/icon-addressbookSml.png
/usr/local/cp/cpimages/brandx/MyProfileexpanded_en_US.png
/usr/local/cp/cpimages/brandx/guagemarkerleft.gif
/usr/local/cp/cpimages/brandx/expand.gif
/usr/local/cp/cpimages/brandx/info.gif
/usr/local/cp/cpimages/brandx/systemAdmin.png
/usr/local/cp/cpimages/brandx/logo_placeholder_webmail.jpg
/usr/local/cp/cpimages/brandx/MyProfileexpanded_ja_JP.png
/usr/local/cp/cpimages/brandx/icon-mailfiltersSml.png
/usr/local/cp/cpimages/brandx/FolderManagement.png
/usr/local/cp/cpimages/brandx/arrow_up.gif
/usr/local/cp/cpimages/brandx/icon-foldermgmt.png
/usr/local/cp/cpimages/brandx/arrow_down2.gif
/usr/local/cp/cpimages/brandx/icon-temp.gif
/usr/local/cp/cpimages/brandx/guagemarkerright.gif
/usr/local/cp/cpimages/brandx/file_media.gif
/usr/local/cp/cpimages/brandx/61logo.gif
/usr/local/cp/cpimages/brandx/success.gif
/usr/local/cp/cpimages/brandx/file_mail.gif
/usr/local/cp/cpimages/brandx/individual.gif
/usr/local/cp/cpimages/brandx/help_1616.gif
/usr/local/cp/cpimages/brandx/icon-webmailoptionsSml.png
/usr/local/cp/cpimages/brandx/check_disabled.gif
/usr/local/cp/cpimages/brandx/domainManagement.png
/usr/local/cp/cpimages/brandx/icon-mailfilters.png
/usr/local/cp/cpimages/brandx/group.gif
/usr/local/cp/cpimages/brandx/custommenu_bg.jpg
/usr/local/cp/cpimages/brandx/help.png
/usr/local/cp/cpimages/brandx/hypertext_link.gif
/usr/local/cp/cpimages/brandx/icon-help-search.png
/usr/local/cp/cpimages/brandx/folder_sys.gif
/usr/local/cp/cpimages/brandx/rss_20.gif
/usr/local/cp/cpimages/brandx/MyProfilecollapsed_en_US.png
/usr/local/cp/cpimages/brandx/sort_arrow_down.gif
/usr/local/cp/cpimages/brandx/SystemAdministration.png
/usr/local/cp/cpimages/brandx/icon-help-search.gif
/usr/local/cp/cpimages/brandx/logo_placeholder.jpg
/usr/local/cp/cpimages/brandx/MyProfilecollapsed_ja_JP.png
/usr/local/cp/cpimages/brandx/folder.gif
/usr/local/cp/cpimages/brandx/1gaugeEmptyBack.jpg
/usr/local/cp/cpimages/brandx/fileManagement.png
/usr/local/cp/cpimages/brandx/icon-domainmgt.gif
/usr/local/cp/cpimages/brandx/MailboxOptions.png
/usr/local/cp/cpimages/brandx/arrow_down.gif
/usr/local/cp/cpimages/brandx/plusIcon.gif
/usr/local/cp/cpimages/brandx/folder_hidden.gif
/usr/local/cp/cpimages/brandx/icon-foldermgmtSml.png
/usr/local/cp/cpimages/brandx/icon-foldermgmtSml.gif
/usr/local/cp/cpimages/brandx/red_error.png
/usr/local/cp/cpimages/brandx/WebmailOptions.png
/usr/local/cp/cpimages/brandx/userManagement.png
/usr/local/cp/cpimages/brandx/icon-mailfolders.gif
/usr/local/cp/cpimages/brandx/icon-webmailoptions.gif
/usr/local/cp/cpimages/brandx/arrowSide.gif
/usr/local/cp/cpimages/brandx/logo_placeholder_error.jpg
/usr/local/cp/cpimages/brandx/blue_message.png
/usr/local/cp/cpimages/brandx/icon-mailfolders.png
/usr/local/cp/cpimages/brandx/file_link.gif
/usr/local/cp/cpimages/brandx/yellow_alert.png
/usr/local/cp/cpimages/brandx/folder_link.gif
/usr/local/cp/cpimages/brandx/file_dirspace.gif
/usr/local/cp/cpimages/brandx/new.gif
/usr/local/cp/cpimages/brandx/folder_link_hidden.gif
/usr/local/cp/cpimages/brandx/icon-sysadmin.gif
/usr/local/cp/cpimages/brandx/onlinehelp.css
/usr/local/cp/cpimages/brandx/icon-mailboxoptions.png
/usr/local/cp/cpimages/brandx/gray_circle.gif
/usr/local/cp/cpimages/brandx/MailMessages.png
/usr/local/cp/cpimages/brandx/red_x.gif
/usr/local/cp/cpimages/brandx/icon-prefs.gif
/usr/local/cp/cpimages/brandx/globalTools.png
/usr/local/cp/cpimages/brandx/1gaugeBack.jpg
/usr/local/cp/cpimages/brandx/icon-filemgmt.gif
/usr/local/cp/cpimages/brandx/arrowDown.gif
/usr/local/cp/cpimages/brandx/error.gif
/usr/local/cp/cpimages/brandx/myProfile.png
/usr/local/cp/cpimages/brandx/style156.css
/usr/local/cp/cpimages/brandx/GlobalTools.png
/usr/local/cp/cpimages/brandx/icon-profile.gif
/usr/local/cp/cpimages/brandx/unread.gif
/usr/local/cp/cpimages/brandx/Preferences.png
/usr/local/cp/cpimages/brandx/file.gif
/usr/local/cp/cpimages/brandx/file_txt.gif
/usr/local/cp/cpimages/brandx/green_check.gif
/usr/local/cp/cpimages/brandx/icon-mailfoldersSml.png
/usr/local/cp/cpimages/brandx/folder_system.gif
/usr/local/cp/cpimages/brandx/file_compressed.gif
/usr/local/cp/cpimages/default/file_sound.gif
/usr/local/cp/cpimages/default/file_html.gif
/usr/local/cp/cpimages/default/file_link_hidden.gif
/usr/local/cp/cpimages/default/icon-mailboxoptions.gif
/usr/local/cp/cpimages/default/logo_placeholder_cp.jpg
/usr/local/cp/cpimages/default/folder_sys_link_hidden.gif
/usr/local/cp/cpimages/default/logo_placeholder_login.jpg
/usr/local/cp/cpimages/default/read.gif
/usr/local/cp/cpimages/default/icon-foldermgmt.gif
/usr/local/cp/cpimages/default/important.gif
/usr/local/cp/cpimages/default/icon-mailmgt.gif
/usr/local/cp/cpimages/default/folder_sys_hidden.gif
/usr/local/cp/cpimages/default/attachment.gif
/usr/local/cp/cpimages/default/style.css
/usr/local/cp/cpimages/default/icon-usermgt.gif
/usr/local/cp/cpimages/default/spamassassin_logo.png
/usr/local/cp/cpimages/default/guagemarker.gif
/usr/local/cp/cpimages/default/file_hidden.gif
/usr/local/cp/cpimages/default/clam.gif
/usr/local/cp/cpimages/default/unread-status.gif
/usr/local/cp/cpimages/default/folder_sys_link.gif
/usr/local/cp/cpimages/default/logo_placeholder_mail.jpg
/usr/local/cp/cpimages/default/file_image.gif
/usr/local/cp/cpimages/default/folder_compressed.gif
/usr/local/cp/cpimages/default/folder_parent.gif
/usr/local/cp/cpimages/default/icon-addressbook.gif
/usr/local/cp/cpimages/default/icon-mailfilters.gif
/usr/local/cp/cpimages/default/sort_arrow_up.gif
/usr/local/cp/cpimages/default/check_enabled.gif
/usr/local/cp/cpimages/default/guagemarkerleft.gif
/usr/local/cp/cpimages/default/info.gif
/usr/local/cp/cpimages/default/logo_placeholder_webmail.jpg
/usr/local/cp/cpimages/default/arrow_up.gif
/usr/local/cp/cpimages/default/icon-temp.gif
/usr/local/cp/cpimages/default/guagemarkerright.gif
/usr/local/cp/cpimages/default/file_media.gif
/usr/local/cp/cpimages/default/success.gif
/usr/local/cp/cpimages/default/file_mail.gif
/usr/local/cp/cpimages/default/individual.gif
/usr/local/cp/cpimages/default/help_1616.gif
/usr/local/cp/cpimages/default/check_disabled.gif
/usr/local/cp/cpimages/default/group.gif
/usr/local/cp/cpimages/default/folder_sys.gif
/usr/local/cp/cpimages/default/sort_arrow_down.gif
/usr/local/cp/cpimages/default/logo_placeholder.jpg
/usr/local/cp/cpimages/default/folder.gif
/usr/local/cp/cpimages/default/icon-domainmgt.gif
/usr/local/cp/cpimages/default/arrow_down.gif
/usr/local/cp/cpimages/default/folder_hidden.gif
/usr/local/cp/cpimages/default/icon-mailfolders.gif
/usr/local/cp/cpimages/default/icon-webmailoptions.gif
/usr/local/cp/cpimages/default/arrowSide.gif
/usr/local/cp/cpimages/default/file_link.gif
/usr/local/cp/cpimages/default/folder_link.gif
/usr/local/cp/cpimages/default/file_dirspace.gif
/usr/local/cp/cpimages/default/folder_link_hidden.gif
/usr/local/cp/cpimages/default/icon-sysadmin.gif
/usr/local/cp/cpimages/default/red_x.gif
/usr/local/cp/cpimages/default/icon-prefs.gif
/usr/local/cp/cpimages/default/icon-filemgmt.gif
/usr/local/cp/cpimages/default/arrowDown.gif
/usr/local/cp/cpimages/default/error.gif
/usr/local/cp/cpimages/default/icon-profile.gif
/usr/local/cp/cpimages/default/unread.gif
/usr/local/cp/cpimages/default/file.gif
/usr/local/cp/cpimages/default/file_txt.gif
/usr/local/cp/cpimages/default/green_check.gif
/usr/local/cp/cpimages/default/folder_system.gif
/usr/local/cp/cpimages/default/file_compressed.gif
/usr/local/cp/etc/vsapd.conf
/usr/local/cp/etc/server.key
/usr/local/cp/etc/conf.d/opencpx.conf
/usr/local/cp/etc/fwlevels/iptables.1
/usr/local/cp/etc/fwlevels/DEFAULT
/usr/local/cp/etc/fwlevels/iptables.3.c
/usr/local/cp/etc/fwlevels/iptables.1.h
/usr/local/cp/etc/fwlevels/iptables.2.m
/usr/local/cp/etc/fwlevels/iptables.3.m
/usr/local/cp/etc/fwlevels/iptables.0
/usr/local/cp/etc/fwlevels/iptables.3.w
/usr/local/cp/etc/fwlevels/iptables.2.h
/usr/local/cp/etc/fwlevels/iptables.2.c
/usr/local/cp/etc/fwlevels/iptables.f
/usr/local/cp/etc/fwlevels/iptables.2.w
/usr/local/cp/etc/server.crt
/usr/local/cp/etc/rc.d/init.d/vsapd
/usr/local/cp/lib/ControlPanel2.pm
/usr/local/cp/lib/VSAP/XMLObj.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/Base.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/Linux/Vsapd.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/Linux/RC.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/Linux/Inetd.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/Linux/Xinetd.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/Linux/Postgresql.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/Linux/Mailman.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/Linux/Dovecot.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/Linux/Mysql.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/Linux/sshd.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/Linux/Postfix.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/Linux/Sendmail.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/Linux/Apache.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/FreeBSD/Vsapd.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/FreeBSD/RC.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/FreeBSD/Inetd.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/FreeBSD/Postgresql.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/FreeBSD/Mailman.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/FreeBSD/Dovecot.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/FreeBSD/Mysql.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/FreeBSD/sshd.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/FreeBSD/Sendmail.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control/FreeBSD/Apache.pm
/usr/local/cp/lib/VSAP/Server/Sys/Service/Control.pm
/usr/local/cp/lib/VSAP/Server/Sys/Config/Inetd/Impl/Linux/Inetd.pm
/usr/local/cp/lib/VSAP/Server/Sys/Config/Inetd/Impl/FreeBSD/Inetd.pm
/usr/local/cp/lib/VSAP/Server/Sys/Config/Inetd.pm
/usr/local/cp/lib/VSAP/Server/Util.pm
/usr/local/cp/lib/VSAP/Server/G11N/Mail.pm
/usr/local/cp/lib/VSAP/Server/Base.pm
/usr/local/cp/lib/VSAP/Server/Modules.pm
/usr/local/cp/lib/VSAP/Server/G11N.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/apache.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/user/messages.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/user/mail.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/user/password.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/user/shell.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/user/prefs.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/mysql.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/auth.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/backup.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files/list.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files/chmod.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files/rename.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files/copy.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files/chown.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files/mkdir.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files/link.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files/properties.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files/upload.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files/delete.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files/move.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files/uncompress.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files/create.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files/download.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/files/compress.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/web/rss.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/domain.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/mail.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/config.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/sys/service.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/sys/reboot.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/sys/ssl.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/sys/timezone.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/sys/inetd.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/sys/shutdown.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/sys/hostname.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/sys/monitor.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/sys/ssh.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/sys/account.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/sys/firewall.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/sys/info.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/sys/security.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/sys/logs.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/sys/crontab.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/extensions.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/user.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/webmail/messages.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/webmail/send.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/webmail/options.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/webmail/distlist.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/webmail/addressbook.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/webmail/folders.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/logout.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/mail/addresses.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/mail/clamav.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/mail/spamassassin.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/mail/autoreply.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/mail/helper.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/mail/forward.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/postgresql.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/webmail.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/diskspace.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/string/encoding.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/help.pm
/usr/local/cp/lib/VSAP/Server/Modules/vsap/logger.pm
/usr/local/cp/lib/VSAP/Client/Config.pm
/usr/local/cp/lib/VSAP/Client/UNIX.pm
/usr/local/cp/lib/VSAP/Client/INET.pm
/usr/local/cp/lib/VSAP/Server.pm
/usr/local/cp/lib/VSAP/Client.pm
/usr/local/cp/lib/x86_64-linux-thread-multi/perllocal.pod
/usr/local/cp/lib/x86_64-linux-thread-multi/VSAP/Server/G11N/Date.pm
/usr/local/cp/lib/ControlPanel/MetaProc.pm
/usr/local/cp/lib/ControlPanel/Transform.pm
/usr/local/cp/lib/VWH/Platform/Info.pm
/usr/local/cp/lib/ControlPanel2/FileTransfer.pm
/usr/local/cp/sbin/monitor
/usr/local/cp/sbin/vsapd
/usr/local/cp/share/monitor_prefs.template
/usr/local/cp/share/site_prefs.template
/usr/local/cp/strings/en_US/cp_prefs.xml
/usr/local/cp/strings/en_US/global.xml
/usr/local/cp/strings/en_US/mail_options.xml
/usr/local/cp/strings/en_US/cp.xml
/usr/local/cp/strings/en_US/cp_email.xml
/usr/local/cp/strings/en_US/cp_files.xml
/usr/local/cp/strings/en_US/cp_profile.xml
/usr/local/cp/strings/en_US/error.xml
/usr/local/cp/strings/en_US/cp_users.xml
/usr/local/cp/strings/en_US/mail_address_book.xml
/usr/local/cp/strings/en_US/mail.xml
/usr/local/cp/strings/en_US/cp_admin.xml
/usr/local/cp/strings/en_US/help.xml
/usr/local/cp/strings/en_US/cp_help.xml
/usr/local/cp/strings/en_US/cp_domains.xml
/usr/local/cp/strings/ja_JP/cp_prefs.xml
/usr/local/cp/strings/ja_JP/global.xml
/usr/local/cp/strings/ja_JP/mail_options.xml
/usr/local/cp/strings/ja_JP/cp.xml
/usr/local/cp/strings/ja_JP/cp_email.xml
/usr/local/cp/strings/ja_JP/cp_files.xml
/usr/local/cp/strings/ja_JP/cp_profile.xml
/usr/local/cp/strings/ja_JP/error.xml
/usr/local/cp/strings/ja_JP/cp_users.xml
/usr/local/cp/strings/ja_JP/mail_address_book.xml
/usr/local/cp/strings/ja_JP/mail.xml
/usr/local/cp/strings/ja_JP/cp_admin.xml
/usr/local/cp/strings/ja_JP/help.xml
/usr/local/cp/strings/ja_JP/cp_help.xml
/usr/local/cp/strings/ja_JP/cp_domains.xml
/usr/local/cp/templates/default/jquery-1.2.1.min.js
/usr/local/cp/templates/default/error.xsl
/usr/local/cp/templates/default/help/help.js
/usr/local/cp/templates/default/help/help_global.xsl
/usr/local/cp/templates/default/help/index.meta.xsl
/usr/local/cp/templates/default/help/index.xsl
/usr/local/cp/templates/default/restart_apache.meta.xsl
/usr/local/cp/templates/default/error/error_global.xsl
/usr/local/cp/templates/default/error/413.xsl
/usr/local/cp/templates/default/error/404.xsl
/usr/local/cp/templates/default/error/413.meta.xsl
/usr/local/cp/templates/default/error/503.xsl
/usr/local/cp/templates/default/error/403.xsl
/usr/local/cp/templates/default/error/503.meta.xsl
/usr/local/cp/templates/default/error/403.meta.xsl
/usr/local/cp/templates/default/error/404.meta.xsl
/usr/local/cp/templates/default/restart_apache.xsl
/usr/local/cp/templates/default/login.xsl
/usr/local/cp/templates/default/data_table_obj.js
/usr/local/cp/templates/default/auth.xsl
/usr/local/cp/templates/default/global.xsl
/usr/local/cp/templates/default/cp/cp.js
/usr/local/cp/templates/default/cp/email/add-edit.xsl
/usr/local/cp/templates/default/cp/email/add-edit.meta.xsl
/usr/local/cp/templates/default/cp/email/index.meta.xsl
/usr/local/cp/templates/default/cp/email/index.xsl
/usr/local/cp/templates/default/cp/help/index.meta.xsl
/usr/local/cp/templates/default/cp/help/index.xsl
/usr/local/cp/templates/default/cp/prefs/dm.xsl
/usr/local/cp/templates/default/cp/prefs/autologout.meta.xsl
/usr/local/cp/templates/default/cp/prefs/autologout.xsl
/usr/local/cp/templates/default/cp/prefs/um.meta.xsl
/usr/local/cp/templates/default/cp/prefs/um.xsl
/usr/local/cp/templates/default/cp/prefs/fm.meta.xsl
/usr/local/cp/templates/default/cp/prefs/datetime.xsl
/usr/local/cp/templates/default/cp/prefs/fm.xsl
/usr/local/cp/templates/default/cp/prefs/datetime.meta.xsl
/usr/local/cp/templates/default/cp/prefs/dm.meta.xsl
/usr/local/cp/templates/default/cp/files/add_file.xsl
/usr/local/cp/templates/default/cp/files/add_dir.xsl
/usr/local/cp/templates/default/cp/files/dirspace.xsl
/usr/local/cp/templates/default/cp/files/compress.xsl
/usr/local/cp/templates/default/cp/files/compress.meta.xsl
/usr/local/cp/templates/default/cp/files/permissions.xsl
/usr/local/cp/templates/default/cp/files/properties.xsl
/usr/local/cp/templates/default/cp/files/add_file.meta.xsl
/usr/local/cp/templates/default/cp/files/files.js
/usr/local/cp/templates/default/cp/files/add_dir.meta.xsl
/usr/local/cp/templates/default/cp/files/dirdialog.meta.xsl
/usr/local/cp/templates/default/cp/files/dirspace.meta.xsl
/usr/local/cp/templates/default/cp/files/dirdialog.xsl
/usr/local/cp/templates/default/cp/files/upload_progress.xsl
/usr/local/cp/templates/default/cp/files/file_global.xsl
/usr/local/cp/templates/default/cp/files/link.meta.xsl
/usr/local/cp/templates/default/cp/files/properties.meta.xsl
/usr/local/cp/templates/default/cp/files/link.xsl
/usr/local/cp/templates/default/cp/files/uncompress.meta.xsl
/usr/local/cp/templates/default/cp/files/upload.xsl
/usr/local/cp/templates/default/cp/files/move.xsl
/usr/local/cp/templates/default/cp/files/owners.xsl
/usr/local/cp/templates/default/cp/files/rename.meta.xsl
/usr/local/cp/templates/default/cp/files/owners.meta.xsl
/usr/local/cp/templates/default/cp/files/upload.meta.xsl
/usr/local/cp/templates/default/cp/files/delete.xsl
/usr/local/cp/templates/default/cp/files/upload_progress.meta.xsl
/usr/local/cp/templates/default/cp/files/rename.xsl
/usr/local/cp/templates/default/cp/files/copy.meta.xsl
/usr/local/cp/templates/default/cp/files/delete.meta.xsl
/usr/local/cp/templates/default/cp/files/uncompress.xsl
/usr/local/cp/templates/default/cp/files/copy.xsl
/usr/local/cp/templates/default/cp/files/move.meta.xsl
/usr/local/cp/templates/default/cp/files/permissions.meta.xsl
/usr/local/cp/templates/default/cp/files/index.meta.xsl
/usr/local/cp/templates/default/cp/files/index.xsl
/usr/local/cp/templates/default/cp/ewm_prompt.meta.xsl
/usr/local/cp/templates/default/cp/users/user_properties.meta.xsl
/usr/local/cp/templates/default/cp/users/user_add_profile.xsl
/usr/local/cp/templates/default/cp/users/user_add_eu_profile.meta.xsl
/usr/local/cp/templates/default/cp/users/user_add_mail.xsl
/usr/local/cp/templates/default/cp/users/user_add_eu_profile.xsl
/usr/local/cp/templates/default/cp/users/user_edit_profile.xsl
/usr/local/cp/templates/default/cp/users/user_edit_mail.meta.xsl
/usr/local/cp/templates/default/cp/users/user_add_mail.meta.xsl
/usr/local/cp/templates/default/cp/users/user_edit_profile.meta.xsl
/usr/local/cp/templates/default/cp/users/user_add_da_profile.xsl
/usr/local/cp/templates/default/cp/users/user_add_domain.xsl
/usr/local/cp/templates/default/cp/users/user_add_domain.meta.xsl
/usr/local/cp/templates/default/cp/users/user_add_preview.meta.xsl
/usr/local/cp/templates/default/cp/users/user_properties.xsl
/usr/local/cp/templates/default/cp/users/user_add_da_profile.meta.xsl
/usr/local/cp/templates/default/cp/users/user_add_profile.meta.xsl
/usr/local/cp/templates/default/cp/users/user_edit_mail.xsl
/usr/local/cp/templates/default/cp/users/index.meta.xsl
/usr/local/cp/templates/default/cp/users/index.xsl
/usr/local/cp/templates/default/cp/users/user_add_preview.xsl
/usr/local/cp/templates/default/cp/custom_frame.meta.xsl
/usr/local/cp/templates/default/cp/profile/password.xsl
/usr/local/cp/templates/default/cp/profile/password.meta.xsl
/usr/local/cp/templates/default/cp/profile/shell.meta.xsl
/usr/local/cp/templates/default/cp/profile/shell.xsl
/usr/local/cp/templates/default/cp/profile/index.meta.xsl
/usr/local/cp/templates/default/cp/profile/index.xsl
/usr/local/cp/templates/default/cp/admin/podcast_item_select.meta.xsl
/usr/local/cp/templates/default/cp/admin/packageview.meta.xsl
/usr/local/cp/templates/default/cp/admin/schedule.js
/usr/local/cp/templates/default/cp/admin/packageview.xsl
/usr/local/cp/templates/default/cp/admin/config_phpmyadmin.meta.xsl
/usr/local/cp/templates/default/cp/admin/config_file_restore.meta.xsl
/usr/local/cp/templates/default/cp/admin/selfmanaged.js
/usr/local/cp/templates/default/cp/admin/logarc.xsl
/usr/local/cp/templates/default/cp/admin/applications.meta.xsl
/usr/local/cp/templates/default/cp/admin/packages.xsl
/usr/local/cp/templates/default/cp/admin/config_mysql.meta.xsl
/usr/local/cp/templates/default/cp/admin/config_backup_view.meta.xsl
/usr/local/cp/templates/default/cp/admin/config_phppgadmin.meta.xsl
/usr/local/cp/templates/default/cp/admin/config_webdav.xsl
/usr/local/cp/templates/default/cp/admin/acctinfo.xsl
/usr/local/cp/templates/default/cp/admin/config_file_restore.xsl
/usr/local/cp/templates/default/cp/admin/config_backup_view.xsl
/usr/local/cp/templates/default/cp/admin/selfmanaged.meta.xsl
/usr/local/cp/templates/default/cp/admin/config_file.js
/usr/local/cp/templates/default/cp/admin/services.js
/usr/local/cp/templates/default/cp/admin/services.meta.xsl
/usr/local/cp/templates/default/cp/admin/config_postgresql.xsl
/usr/local/cp/templates/default/cp/admin/schedule.xsl
/usr/local/cp/templates/default/cp/admin/services.xsl
/usr/local/cp/templates/default/cp/admin/config_phpadmin.js
/usr/local/cp/templates/default/cp/admin/jta25.jar
/usr/local/cp/templates/default/cp/admin/selfmanaged.xsl
/usr/local/cp/templates/default/cp/admin/applications.xsl
/usr/local/cp/templates/default/cp/admin/timezone.xsl
/usr/local/cp/templates/default/cp/admin/config_phpmyadmin.xsl
/usr/local/cp/templates/default/cp/admin/timezone.meta.xsl
/usr/local/cp/templates/default/cp/admin/shell.meta.xsl
/usr/local/cp/templates/default/cp/admin/config_webdav.meta.xsl
/usr/local/cp/templates/default/cp/admin/logarc.meta.xsl
/usr/local/cp/templates/default/cp/admin/config_postgresql.meta.xsl
/usr/local/cp/templates/default/cp/admin/loglist.meta.xsl
/usr/local/cp/templates/default/cp/admin/event_handlers.js
/usr/local/cp/templates/default/cp/admin/logarc.js
/usr/local/cp/templates/default/cp/admin/podcast_item_add.xsl
/usr/local/cp/templates/default/cp/admin/config_webalizer.xsl
/usr/local/cp/templates/default/cp/admin/monitor.meta.xsl
/usr/local/cp/templates/default/cp/admin/config_mysql.xsl
/usr/local/cp/templates/default/cp/admin/schedule.meta.xsl
/usr/local/cp/templates/default/cp/admin/config_mailman.meta.xsl
/usr/local/cp/templates/default/cp/admin/podcast_item_add.meta.xsl
/usr/local/cp/templates/default/cp/admin/podcast_list.meta.xsl
/usr/local/cp/templates/default/cp/admin/podcast_item_select.xsl
/usr/local/cp/templates/default/cp/admin/logview.xsl
/usr/local/cp/templates/default/cp/admin/podcast_feed_add.xsl
/usr/local/cp/templates/default/cp/admin/firewall.xsl
/usr/local/cp/templates/default/cp/admin/firewall.meta.xsl
/usr/local/cp/templates/default/cp/admin/acctinfo.meta.xsl
/usr/local/cp/templates/default/cp/admin/schededit.meta.xsl
/usr/local/cp/templates/default/cp/admin/config_file.meta.xsl
/usr/local/cp/templates/default/cp/admin/security.xsl
/usr/local/cp/templates/default/cp/admin/podcast_list.xsl
/usr/local/cp/templates/default/cp/admin/packages.meta.xsl
/usr/local/cp/templates/default/cp/admin/applet.conf
/usr/local/cp/templates/default/cp/admin/logview.meta.xsl
/usr/local/cp/templates/default/cp/admin/shell.xsl
/usr/local/cp/templates/default/cp/admin/packages.js
/usr/local/cp/templates/default/cp/admin/config_phppgadmin.xsl
/usr/local/cp/templates/default/cp/admin/loglist.xsl
/usr/local/cp/templates/default/cp/admin/podcast.js
/usr/local/cp/templates/default/cp/admin/security.meta.xsl
/usr/local/cp/templates/default/cp/admin/config_file.xsl
/usr/local/cp/templates/default/cp/admin/config_webalizer.meta.xsl
/usr/local/cp/templates/default/cp/admin/schededit.xsl
/usr/local/cp/templates/default/cp/admin/monitor.xsl
/usr/local/cp/templates/default/cp/admin/podcast_feed_add.meta.xsl
/usr/local/cp/templates/default/cp/admin/config_webdav.js
/usr/local/cp/templates/default/cp/admin/config_mailman.xsl
/usr/local/cp/templates/default/cp/admin/monitor.js
/usr/local/cp/templates/default/cp/ewm_prompt.xsl
/usr/local/cp/templates/default/cp/cp_global.xsl
/usr/local/cp/templates/default/cp/cp_global.meta.xsl
/usr/local/cp/templates/default/cp/domains/domain_self_signed_cert.meta.xsl
/usr/local/cp/templates/default/cp/domains/domain_cert.xsl
/usr/local/cp/templates/default/cp/domains/domain_create_csr.xsl
/usr/local/cp/templates/default/cp/domains/domain_edit.xsl
/usr/local/cp/templates/default/cp/domains/domain_create_csr.meta.xsl
/usr/local/cp/templates/default/cp/domains/domain_properties.xsl
/usr/local/cp/templates/default/cp/domains/domain_add.xsl
/usr/local/cp/templates/default/cp/domains/domain_cert.meta.xsl
/usr/local/cp/templates/default/cp/domains/domain_self_signed_cert.xsl
/usr/local/cp/templates/default/cp/domains/domain_properties.meta.xsl
/usr/local/cp/templates/default/cp/domains/domain_add_setup.meta.xsl
/usr/local/cp/templates/default/cp/domains/domain_add.meta.xsl
/usr/local/cp/templates/default/cp/domains/domain_edit.meta.xsl
/usr/local/cp/templates/default/cp/domains/domain_add_setup.xsl
/usr/local/cp/templates/default/cp/domains/index.meta.xsl
/usr/local/cp/templates/default/cp/domains/index.xsl
/usr/local/cp/templates/default/cp/custom_frame.js
/usr/local/cp/templates/default/cp/custom_frame.xsl
/usr/local/cp/templates/default/cp/index.meta.xsl
/usr/local/cp/templates/default/cp/index.xsl
/usr/local/cp/templates/default/auth.meta.xsl
/usr/local/cp/templates/default/allfunctions.js
/usr/local/cp/templates/default/login.meta.xsl
/usr/local/cp/templates/default/mail/wm_folders.xsl
/usr/local/cp/templates/default/mail/wm_addfolder.meta.xsl
/usr/local/cp/templates/default/mail/wm_folders.meta.xsl
/usr/local/cp/templates/default/mail/wm_subscribefolder.xsl
/usr/local/cp/templates/default/mail/wm_printmessage.xsl
/usr/local/cp/templates/default/mail/wm_subscribefolder.meta.xsl
/usr/local/cp/templates/default/mail/wm_addfolder.xsl
/usr/local/cp/templates/default/mail/address_book/wm_distlist.meta.xsl
/usr/local/cp/templates/default/mail/address_book/wm_import_export.meta.xsl
/usr/local/cp/templates/default/mail/address_book/wm_addresses.meta.xsl
/usr/local/cp/templates/default/mail/address_book/wm_addcontact.xsl
/usr/local/cp/templates/default/mail/address_book/address_book.js
/usr/local/cp/templates/default/mail/address_book/wm_import_export.xsl
/usr/local/cp/templates/default/mail/address_book/wm_addcontact.meta.xsl
/usr/local/cp/templates/default/mail/address_book/mail_addressbook_feedback.xsl
/usr/local/cp/templates/default/mail/address_book/wm_addresses.xsl
/usr/local/cp/templates/default/mail/address_book/wm_distlist.xsl
/usr/local/cp/templates/default/mail/wm_renamefolder.xsl
/usr/local/cp/templates/default/mail/wm_add-edit-attachment.meta.xsl
/usr/local/cp/templates/default/mail/wm_compose.xsl
/usr/local/cp/templates/default/mail/options/outgoing_mail.meta.xsl
/usr/local/cp/templates/default/mail/options/mail_options.js
/usr/local/cp/templates/default/mail/options/mail_options_feedback.xsl
/usr/local/cp/templates/default/mail/options/message_display.meta.xsl
/usr/local/cp/templates/default/mail/options/wm_spamfilter_list.meta.xsl
/usr/local/cp/templates/default/mail/options/folder_display.meta.xsl
/usr/local/cp/templates/default/mail/options/outgoing_mail.xsl
/usr/local/cp/templates/default/mail/options/message_display.xsl
/usr/local/cp/templates/default/mail/options/wm_spamfilter.meta.xsl
/usr/local/cp/templates/default/mail/options/wm_spamfilter.xsl
/usr/local/cp/templates/default/mail/options/wm_spamfilter_list.xsl
/usr/local/cp/templates/default/mail/options/folder_display.xsl
/usr/local/cp/templates/default/mail/options/wm_mailfwd.xsl
/usr/local/cp/templates/default/mail/options/wm_autoreply.meta.xsl
/usr/local/cp/templates/default/mail/options/wm_autoreply.xsl
/usr/local/cp/templates/default/mail/options/wm_virusscan.meta.xsl
/usr/local/cp/templates/default/mail/options/wm_mailfwd.meta.xsl
/usr/local/cp/templates/default/mail/options/wm_virusscan.xsl
/usr/local/cp/templates/default/mail/mail_compose_feedback.xsl
/usr/local/cp/templates/default/mail/wm_rawmessage.xsl
/usr/local/cp/templates/default/mail/wm_rawmessage.meta.xsl
/usr/local/cp/templates/default/mail/mail.js
/usr/local/cp/templates/default/mail/wm_add-edit-attachment.xsl
/usr/local/cp/templates/default/mail/wm_viewmessage.xsl
/usr/local/cp/templates/default/mail/wm_select-addressee.xsl
/usr/local/cp/templates/default/mail/mail_global.xsl
/usr/local/cp/templates/default/mail/wm_viewmessage.meta.xsl
/usr/local/cp/templates/default/mail/wm_renamefolder.meta.xsl
/usr/local/cp/templates/default/mail/wm_select-addressee.meta.xsl
/usr/local/cp/templates/default/mail/mail_folders_feedback.xsl
/usr/local/cp/templates/default/mail/wm_messages.meta.xsl
/usr/local/cp/templates/default/mail/wm_messages.xsl
/usr/local/cp/templates/default/mail/wm_printmessage.meta.xsl
/usr/local/cp/templates/default/mail/wm_compose.meta.xsl
/usr/local/cp/templates/default/mail/index.meta.xsl
/usr/local/cp/templates/default/mail/index.xsl
/usr/local/cp/templates/default/jquery-1.9.1.min.js
/usr/local/cp/templates/default/index.meta.xsl
/usr/local/cp/templates/default/global.meta.xsl
/usr/local/cp/templates/default/index.xsl
