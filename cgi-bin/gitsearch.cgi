#!/usr/bin/perl

if ($ENV{'REQUEST_METHOD'} eq 'POST') {
    
    read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
    
    @pairs = split(/&/, $buffer);
    
   
    print "Content-type: text/html\n\n";
    print "<HTML>\n";
    print "<HEAD>\n";
    print "<TITLE>gitsearch</TITLE>\n";
    print "</HEAD>\n";
    print "<BODY BGCOLOR=#DDDDEE TEXT=#000000>\n";
    print "<H1>Search results</H1>\n\n";
    
    foreach $pair (@pairs) {
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	print "$name : $value <BR/>\n";
    }      
    print "</BODY>\n</HTML>\n";

    exit(0);
}
