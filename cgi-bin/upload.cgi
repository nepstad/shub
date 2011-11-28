#!/usr/bin/perl -w
use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use lib '/web/cgi-bin';
require "upload.pl";
require "create_git_repos.pl";

$ENV{"PATH"} = "/bin:/usr/bin:/usr/local/bin";
delete @ENV{ 'IFS', 'CDPATH', 'ENV', 'BASH_ENV' };

# Reading the form variables
my $query = new CGI;
my $projname = $query->param("projname");
my $filename = $query->param("datafile");
my $author = $query->param("author");
my $tag = $query->param("tag");
my $projnr = $query->param("projnr");
my $description = $query->param("description");



print $query->header(); 
my ($upload_report, $output_filename) = upload_file($query);
my ($git_create_report) = create_git_repos($output_filename, $projname);

print "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"DTD/xhtml1-strict.dtd\">";
print "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\" lang=\"en\">"; 
print "<head> <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />";
print "<title>Uploaded $output_filename</title>\n";
print "<body>\n";
print $upload_report;
print $git_create_report;
print "</body> </html>";    



# print $filename

