#!/usr/bin/perl -w
use strict;
use File::Temp qw ( tempfile tempdir );
use File::Copy;
use Git::Repository;  # At least I mean to use this.
use JSON::XS;
use Encode;

sub create_git_repos($$)
{
    my ($fname, $projname) = @_;
    my $report =  "<h1>create git repos: $fname <h1>\n"; 
    
    my $tmpdir = tempdir();
    
    print "Created $tmpdir<br/>";
    chdir("$tmpdir") or die "Unknown error $!";
    system("tar", "xf", "/web/upload/$fname");
    system("git", "init");
    system("git", "add", ".");
    system("git", "commit", "-m \"Initial entry\"");
    chdir("/web/repos");
    system("git", "clone", "--bare", $tmpdir, $projname);
       
    my $json = JSON::XS->new->utf8;
    my $CRLF = "\x0D\x0A";

    print $json->encode( {a => [2]} );
    return ($report);
}
1;
