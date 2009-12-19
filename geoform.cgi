#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use lib qw(/home/kur/local/lib/perl5 /home/kur/local/lib/perl5/site_perl /home/kur/local/lib/perl5/site_perl/5.8.9 /home/kur/local/lib/perl5/site_perl/5.8.9/mach);
use Encode;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use Config::Pit;
use LWP::UserAgent;

    my $svcfg = pit_get("personal.server");
    my $geocfg = pit_get("cirius.co.jp");

    my $cgi = CGI->new();

    print $cgi->header(-type => 'text/html', -charset => 'utf-8');
    print '<html><body>';

    if($ENV{'HTTP_USER_AGENT'}) {
        my $returl = $svcfg->{testhost}.'/geo/iarea/geoform.cgi';
        my $uri = 'http://api.cirius.co.jp/v1/geoform/xhtml'.
            '?ua='.$ENV{'HTTP_USER_AGENT'}.
            '&return_uri='.$returl.
            '&api_key='.$geocfg->{apikey};
        my $ua = LWP::UserAgent->new();
        my $req = HTTP::Request->new(GET => $uri);
        my $res = $ua->request($req);
        if($res->is_success) {
            print '<div style="text-align:center">';
            print $res->content;
            print '</div>';
        }
    }

    if($cgi->param('accuracy')) {
        my @color = ('blue', 'green', 'yellow', 'red');
        print 'l:'.$cgi->param('lat').'*'.$cgi->param('lon').'<br>';
        print 'L:'.$cgi->param('address').'<br>';
        print '<img src="http://maps.google.com/staticmap?maptype=mobile&size=240x240'.
            '&markers='.$cgi->param('lat').','.$cgi->param('lon').','.
            @color[$cgi->param('accuracy')].'c&format=gif&zoom=16">';
    }

    print '</body></html>';

