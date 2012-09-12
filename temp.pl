@words;

while (<STDIN>) {
	chomp;
	$legal = 1;
	$word = $_;
	next unless length($word) >= 3;
	for (@words) {
		if ($word =~ /^$_/) {
			$legal = 0;
		}
	}
	print STDERR "$word checked, $legal\n" if $legal;
	push @words,$word if $legal;
}
for (@words) {
	print "$_\n";
}

