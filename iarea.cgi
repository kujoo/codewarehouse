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
    my $gps = 1;

    if($cgi->param('POSINFO')) {

        $gps = 0;

        my $sub = $cgi->param('AREACODE').'|'.$cgi->param('LAT').'|'.$cgi->param('LON');
        my $msg =
            ' Lat: '.$cgi->param('LAT')."\n".
            ' Lon: '.$cgi->param('LON')."\n".
            ' Geo: '.$cgi->param('GEO')."\n".
            ' Acc: '.$cgi->param('XACC')."\n".
            'Area: '.$cgi->param('AREACODE')."\n".
            'info: '.$cgi->param('POSINFO');

        # mail-send
        $sub = Encode::encode("MIME-Header-ISO_2022_JP", $sub);
        $msg = Encode::encode("iso-2022-jp", $msg."\n\n".$cgi->param('view'));
        my $mail = MIME::Lite->new(
            From    => $config->{twsendmail},
            To      => $config->{docomomail},
            Subject => $sub,
            Data    => $msg,
        );
#       $mail->send("sendmail", "/usr/sbin/sendmail -t -oi -oem");

        # logging
        my $dt = DateTime->now(time_zone => 'Asia/Tokyo');
        open my $fp, '>>', $config->{log}.'iarea.log';
        print $fp $cgi->param('view')."\t".
            DateTime::Format::W3CDTF->format_datetime($dt)."\t".
            $cgi->param('LAT')."\t".
            $cgi->param('LON')."\t".
            $cgi->param('GEO')."\t".
            $cgi->param('XACC')."\t".
            $cgi->param('AREACODE')."\t".
            $cgi->param('POSINFO')."\n";
        close $fp;

    } elsif($cgi->param('view')) {

        $gps = 1;

        # logging
        my $dt = DateTime->now(time_zone => 'Asia/Tokyo');
        open my $fp, '>>', $config->{log}.'iarea.log';
        print $fp $cgi->param('view')."\t".
            DateTime::Format::W3CDTF->format_datetime($dt)."\t".
            $cgi->param('lat')."\t".
            $cgi->param('lon')."\t".
            $cgi->param('geo')."\t".
            $cgi->param('x-acc')."\n";
        close $fp;

    }


    my $dt = DateTime->now(time_zone => 'Asia/Tokyo');
    $dt = DateTime::Format::W3CDTF->format_datetime($dt);

    print $cgi->header(-type => 'text/html', -charset => 'utf-8');
    print <<EOD;
<html><body>$dt<div align="center">
@{[$gps ? qq() : qq(<form method="get" action="@{[$config->{testhost}]}/geo/iarea/iarea.cgi" lcs><input type="hidden" name="view" value="@{[$cgi->param('view')]}"><input type="hidden" name="AREACODE" value="@{[$cgi->param('AREACODE')]}"><input type="hidden" name="LAT" value="@{[$cgi->param('LAT')]}"><input type="hidden" name="LON" value="@{[$cgi->param('LON')]}"><input type="hidden" name="GEO" value="@{[$cgi->param('GEO')]}"><input type="hidden" name="XACC" value="@{[$cgi->param('XACC')]}"><input type="submit" name="ok" value="G P S"></form><hr>)]}
<form method="post" action="http://w1m.docomo.ne.jp/cp/iarea">
<input type="hidden" name="ecode" value="OPENAREACODE">
<input type="hidden" name="msn" value="OPENAREAKEY">
<input type="hidden" name="nl" value="@{[$config->{testhost}]}/geo/iarea/iarea.cgi">
<input type="hidden" name="arg1" value="view=@{[$dt]}">
<input type="hidden" name="posinfo" value="1">
<input type="submit" name="ok" value="iArea Check">
</form><hr></div>
@{[$cgi->param('AREACODE') ? qq(Area&nbsp;@{[$cgi->param('AREACODE')]}<br>) : qq()]}
@{[$cgi->param('LAT')      ? qq(LAT:&nbsp;@{[$cgi->param('LAT')]}<br>) : qq()]}
@{[$cgi->param('lat')      ? qq(lat:&nbsp;@{[$cgi->param('lat')]}<br>) : qq()]}
@{[$cgi->param('LON')      ? qq(LON:&nbsp;@{[$cgi->param('LON')]}<br>) : qq()]}
@{[$cgi->param('lon')      ? qq(lon:&nbsp;@{[$cgi->param('lon')]}<br>) : qq()]}
@{[$cgi->param('GEO')      ? qq(GEO:&nbsp;@{[$cgi->param('GEO')]}<br>) : qq()]}
@{[$cgi->param('geo')      ? qq(geo:&nbsp;@{[$cgi->param('geo')]}<br>) : qq()]}
@{[$cgi->param('XACC')     ? qq(ACC:&nbsp;@{[$cgi->param('XACC')]}<br>) : qq()]}
@{[$cgi->param('x-acc')    ? qq(acc:&nbsp;@{[$cgi->param('x-acc')]}<br>) : qq()]}
@{[$cgi->param('view')     ? qq(view&nbsp;@{[$cgi->param('view')]}<br>) : qq()]}
</body></html>
EOD

