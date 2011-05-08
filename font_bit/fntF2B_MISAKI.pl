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
	my $fontname = 'D:\_work\BOX\_sakura\mskfnt\MISAKI.TTF';
#	my $fontname = 'C:\WINDOWS\Fonts\sazanami-gothic.ttf';
	my $ptsize   = 6;
	my @bg       = &str2rgb('ffffff');
	my @fg       = &str2rgb('000000');
	my $string   = '学校で行われる対面式に先だって入舎式が行われます。寄宿舎の新入生には入舎式でエンジェルが紹介されます。新入生（チャイルド）は担当の高校３年生（エンジェル）に名前を呼ばれて寄宿舎生活がスタートします。';

	GD::Image->trueColor(1);
	my $image = GD::Image->new(1, 1);
	my $bg = $image->colorAllocate(@bg);
	my $fg = $image->colorAllocate(@fg);
	my @bounds = $image->stringFT($fg, $fontname, $ptsize, 0, 0, 0, $string);

	if(!$image or !@bounds) { die 'failure...'; }
	print '// ';
	foreach (@bounds) { print $_.', '; }
	print "\n";

	$image = GD::Image->new($bounds[2] + $bounds[0], 8);
	$image->fill(0, 0, $bg);
	$image->stringFT($fg, $fontname, $ptsize, 0, 0, 8, $string);

	my($width, $height) = $image->getBounds();

	print "// [Font] $fontname / [Width] $width / [Height] $height\n";
	print "// [start] $starttimes\n\n";

	print "const byte scroll_image[] = {\n";

	my $zerocount = 0;
	for(my $x = 0; $x < $width; $x++) {
		my $code = '';
		for(my $y = $height - 1; $y >= 0; $y--) {

			my($r, $g, $b) = $image->rgb($image->getPixel($x, $y));
			$code .= ($r+$g+$b > 0) ? '0' : '1';

		}
		if($code eq '00000000') { $zerocount++; }
		else{ $zerocount = 0; }
		if($zerocount <= 1) { print "B$code,\n"; }
		if($zerocount > 6) { print "B00000000,\nB00000000,\n"; $zerocount = 0; }
	}

	for(1..8) { print "B00000000,\n"; }
	print "};\n";

	my $endtimes = time;
	my $stay = $endtimes - $starttimes;
	print "\n// [end] $endtimes  -> $stay sec\n";


sub str2rgb {
	my $str = shift;
	return unless $str;
	$str =~ /(..)(..)(..)/;
	return map { hex($_); } ($1, $2, $3);
}

