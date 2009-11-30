#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use lib qw(/home/kur/local/lib/perl5 /home/kur/local/lib/perl5/site_perl /home/kur/local/lib/perl5/site_perl/5.8.9 /home/kur/local/lib/perl5/site_perl/5.8.9/mach);
use Encode;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use Config::Pit;
use MIME::Lite;
use DateTime;
use DateTime::Format::HTTP;
use DateTime::Format::W3CDTF;

    my $cgi = CGI->new();
    my $config = pit_get("personal.server");
    my $last;

    if($cgi->param('AREACODE') or $cgi->param('POSINFO')) {

        my $tab = $cgi->param('AREACODE')."\t".$cgi->param('LAT')."\t".$cgi->param('LON')."\t".$cgi->param('GEO')."\t".$cgi->param('XACC')."\t".$cgi->param('POSINFO');
        my $msg =
            'Area: '.$cgi->param('AREACODE')."\n".
            ' Lat: '.$cgi->param('LAT')."\n".
            ' Lon: '.$cgi->param('LON')."\n".
            ' Geo: '.$cgi->param('GEO')."\n".
            ' Acc: '.$cgi->param('XACC')."\n".
            'info: '.$cgi->param('POSINFO')."\n\n".
            $cgi->param('view')."\n\n";
        my $sub = $cgi->param('AREACODE').'|'.$cgi->param('LAT').'|'.$cgi->param('LON');

        $last = $tab; # $sub."\n".$msg
        $sub = Encode::encode("MIME-Header-ISO_2022_JP", $sub);
        $msg = Encode::encode("iso-2022-jp", $msg.$tab);

        my $mail = MIME::Lite->new(
            From    => $config->{twsendmail},
            To      => $config->{docomomail},
            Subject => $sub,
            Data    => $msg,
        );
        $mail->send("sendmail", "/usr/sbin/sendmail -t -oi -oem");


        {
            my $dt = DateTime->now(time_zone => 'Asia/Tokyo');
            open my $fp, '>>', $config->{log}.'iarea.log';
            print $fp DateTime::Format::W3CDTF->format_datetime($dt)."\t".$tab."\t".$cgi->param('view')."\n";
            close $fp;
        }

    }

    unless($last) { $last = 'none'; }
    my $dt = DateTime->now(time_zone => 'Asia/Tokyo');
    $dt = DateTime::Format::W3CDTF->format_datetime($dt);

    print $cgi->header(-type => 'text/html', -charset => 'utf-8');
    print <<EOD;
<html><body>$dt
<div align="center"><form method="post" action="http://w1m.docomo.ne.jp/cp/iarea">
<input type="hidden" name="ecode" value="OPENAREACODE">
<input type="hidden" name="msn" value="OPENAREAKEY">
<input type="hidden" name="nl" value="$config->{testhost}/geo/iarea/iarea.cgi">
<input type="hidden" name="arg1" value="view=$dt">
<input type="hidden" name="posinfo" value="1">
<input type="submit" name="ok" value="iArea Check">
</form></div><hr>
$last
</body></html>
EOD

