package VSAP::Client::Config;

use 5.006;
use strict;
use warnings;

use POSIX;

require Exporter;

our @ISA = qw(Exporter);

our %EXPORT_TAGS = ( 'all' => [ qw(
	$VSAP_CLIENT_MODE
        $VSAP_CLIENT_TCP_HOST
	$VSAP_CLIENT_TCP_PORT 
	$VSAP_CLIENT_UNIX_SOCKET_PATH
	$VSAP_CLIENT_SSL
) ] );

our @EXPORT_OK = ( @{ $EXPORT_TAGS{'all'} } );

our @EXPORT = qw( );
our $VERSION = '1.00';

my $is_linux = ((POSIX::uname())[0] =~ /Linux/);
my $is_vps2 = -d '/skel' || $is_linux;
my $is_cloudn = -d '/var/vsap' && $is_linux;

our $VSAP_CLIENT_MODE = '';
our $VSAP_CLIENT_TCP_PORT = 551;
our $VSAP_CLIENT_TCP_HOST = 'localhost';
our $VSAP_CLIENT_UNIX_SOCKET_PATH = '/var/run/vsapd.sock';
our $VSAP_CLIENT_SSL;

if ($is_vps2 && !$is_cloudn) {
    ## use UNIX domain sockets (uses socket path above)
    $VSAP_CLIENT_MODE = 'unix';
}
else {
    ## use TCP (uses tcp host/port above)
    $VSAP_CLIENT_MODE = 'tcp';
    $VSAP_CLIENT_SSL = $is_cloudn;
}

# Preloaded methods go here.

1;
__END__
=head1 NAME

VSAP::Client::Config - VSAP Client Configuration module for VPS2.

=head1 SYNOPSIS

  use VSAP::Client::Config qw/ $VSAP_CLIENT_MODE $VSAP_CLIENT_TCP_PORT $VSAP_CLIENT_TCP_HOST $VSAP_CLIENT_UNIX_SOCKET_PATH $VSAP_CLIENT_SSL /

  #.. refer to the VSAP_CLIENT_* variables .. 

=head1 DESCRIPTION

Configuration parameters for the VSAP::Client module. Defines the default values which are used 
when the VSAP::Client is constructed. 

=head2 EXPORT

None by default, following are available: 

$VSAP_CLIENT_MODE - The mode the client is to operate in, either 'tcp' or 'unix'. 

$VSAP_CLIENT_TCP_PORT - The port which the vsap server is listening on. Used if mode is 'tcp'.

$VSAP_CLIENT_UNIX_SOCKET_PATH - The path of the unix domain socket, if client mode is 'unix'

$VSAP_CLIENT_SSL - Connect to a server in SSL mode

=head1 SEE ALSO

L<perl>. VSAP::Client module. 

=head1 AUTHOR

James Russo

=head1 COPYRIGHT AND LICENSE

Copyright (C) 2006 by MYNAMESERVER, LLC
 
No part of this module may be duplicated in any form without written
consent of the copyright holder.

=cut
