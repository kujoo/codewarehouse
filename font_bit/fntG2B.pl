#!/usr/local/bin/perl
#!/usr/bin/perl
#!perl

use strict;
use warnings;
use utf8;
use Encode;
use GD;
#use GD::Text;
#use Config::Pit;

	my $fileimage = 'misaki.png';
	my $codecount = 0;
	my $fontsizeX = 8;
	my $fontsizeY = 8;
	my $bgColor = 255*255*255;
	my $textColor = 0;
	my $fontname = 'MISAKI.TTF';
	my $ptsize = 6;
	my $angle = 0;
	my $string = 'I am Fonts.';

	GD::Image->trueColor(1);
	my $image = new GD::Image(128, 32);
#	my $font = new GD::Font()
#	my $gd_text = new GD::Text(
#		text => 'I am Fonts.',
#		font => 'MISAKI.TTF',
#		ptsize => 8,
#	);

	$image->fill(128, 32, $bgColor);
	$image->string(gdSmallFont, 0, 0, $string, $textColor);
#	$image->stringFT($textColor, $fontname, $ptsize, $angle, 0, 0, $string);

	if(! $image) {
		print "failure...\n";
		return(0);
	}

	my($width, $height) = $image->getBounds();
	my $starttimes = time;

	print '// [File] '.$fileimage.' / [Width] '.$width.' / [Height] '.$height."\n";
	print '// [start] '.$starttimes."\n\n";

	for(my $y = 0; $y < $height; $y += $fontsizeY) {
		for(my $x = 0; $x < $width; $x += $fontsizeX) {

			for(my $fx = 0; $fx < $fontsizeX; $fx++) {
				print 'B';
				for(my $fy = $fontsizeY - 1; $fy >= 0; $fy--) {

					my($r, $g, $b) = $image->rgb($image->getPixel($x + $fx, $y + $fy));
					my $m = ($r+$g+$b > 0) ? '0' : '1';
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

