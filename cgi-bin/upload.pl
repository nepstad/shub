#!/usr/bin/perl -wT
use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;

# 10 Mb max
$CGI::POST_MAX = 1024 * 10000; 

sub upload_file($$) {
    
    my( $query ) = @_;
    my $filename = $query->param("datafile");

# Avoid directory exploits
    my $safe_filename_characters = "a-zA-Z0-9_.-";
    
# Setting the upload directory
    my $upload_dir = "/web/upload";
        
    if( !$filename) { 
	print "Couldn't upload file.\n";
	exit;
    }

# Making the filename safe
    my ( $name, $path, $extension ) = fileparse ( $filename, '\..*' ); 
    $filename = $name . $extension;


    $filename =~ tr/ /_/; $filename =~ s/[^$safe_filename_characters]//g;
    if ( $filename =~ /^([$safe_filename_characters]+)$/ ) 
    { 
	$filename = $1; 
    } 
    else 
    { 
	die "Filename contains invalid characters"; 
    }
    
    if(0) {
# Fetching the file
    my $upload_filehandle = $query->upload("datafile");
    open( UPLOADFILE, ">$upload_dir/$filename" ) or die "$!";
    binmode UPLOADFILE;
    while( <$upload_filehandle> ) {
	print UPLOADFILE;
    }
    close UPLOADFILE;
    }
# Generate a report section for this upload
    my $report =  "<h1>File uploaded</h1>";
    $report .= "Uploaded $filename successfully<br/>\n";
#    $report .=  "Project name: $projname<br/>";
#    $report .=  "Project number: $projname<br/>";
#    $report .=  "Author: $author<br/>";
#    $report .=  "Tag: $tag<br/>";

    return ($report, $filename);
}
1;
