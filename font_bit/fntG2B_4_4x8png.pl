#!/usr/local/bin/perl
#!/usr/bin/perl
#!perl

use strict;
use warnings;
use utf8;
use Encode;
use GD;
#use Config::Pit;

	my $starttimes = time;
	my $codecount = 0;
	my $fontsizeX = 4;
	my $fontsizeY = 8;
	my $fileimage = '4x8.png';

	GD::Image->trueColor(1);
	my $image = GD::Image->new($fileimage);
	if(! $image) {
		print "failure...\n";
		return(0);
	}
	my($width, $height) = $image->getBounds();

	print '// [File] '.$fileimage.' / [Width] '.$width.' / [Height] '.$height."\n";
	print '// [start] '.$starttimes."\n\n";

	for(my $y = 0; $y < $height; $y += $fontsizeY) {
		for(my $x = 0; $x < $width; $x += $fontsizeX) {

			for(my $fx = 0; $fx < $fontsizeX; $fx++) {
				print 'B';
				for(my $fy = $fontsizeY - 1; $fy >= 0; $fy--) {

					my($r, $g, $b) = $image->rgb($image->getPixel($x + $fx, $y + $fy));
					my $m = ($r > 0) ? '0' : '1';
					print $m;

				}
				print ",\n";
			}

			print "\n";
		}
		print "\n";
	}

	my $endtimes = time;
	my $stay = $endtimes - $starttimes;
	print '[end] '.$endtimes."\n";
	print ' -> '.$stay."sec\n";

