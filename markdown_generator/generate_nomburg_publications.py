#!/usr/bin/env python3

# Publications markdown generator for Jason Nomburg's website
# Modified from the academicpages template

import pandas as pd
import os

# HTML escape function for YAML safety
html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
}

def html_escape(text):
    """Produce entities within text."""
    if pd.isna(text):
        return ""
    return "".join(html_escape_table.get(c,c) for c in str(text))

# Read the publications TSV file
publications = pd.read_csv("publications_nomburg.tsv", sep="\t", header=0)

# Clear existing publications directory (backup first if needed)
publications_dir = "../_publications/"
if not os.path.exists(publications_dir):
    os.makedirs(publications_dir)

# Generate markdown files for each publication
for row, item in publications.iterrows():
    
    md_filename = str(item.pub_date) + "-" + item.url_slug + ".md"
    html_filename = str(item.pub_date) + "-" + item.url_slug
    year = item.pub_date[:4]
    
    ## YAML variables
    md = "---\ntitle: \""   + html_escape(item.title) + '"\n'
    md += """collection: publications\n"""
    
    # Categorize publications
    venue = str(item.venue).lower()
    if 'nature' in venue or 'cell' in venue or 'science' in venue:
        md += """category: manuscripts\n"""
    elif 'biorxiv' in venue or 'arxiv' in venue:
        md += """category: preprints\n"""
    else:
        md += """category: manuscripts\n"""
    
    md += """\npermalink: /publication/""" + html_filename
    
    if len(str(item.excerpt)) > 5:
        md += "\nexcerpt: '" + html_escape(item.excerpt) + "'"
    
    md += "\ndate: " + str(item.pub_date) 
    md += "\nvenue: '" + html_escape(item.venue) + "'"
    
    if len(str(item.paper_url)) > 5:
        md += "\npaperurl: '" + str(item.paper_url) + "'"
    
    md += "\ncitation: '" + html_escape(item.citation) + "'"
    md += "\n---"
    
    ## Markdown description for individual page
    if len(str(item.excerpt)) > 5:
        md += "\n\n" + html_escape(item.excerpt) + "\n"
    
    if len(str(item.paper_url)) > 5:
        md += "\n\n<a href='" + str(item.paper_url) + "'>Download paper here</a>\n" 
        
    md += "\n\nRecommended citation: " + html_escape(item.citation)
    
    # Write the markdown file
    md_filename = os.path.basename(md_filename)
    with open(publications_dir + md_filename, 'w') as f:
        f.write(md)
    
    print(f"Generated: {md_filename}")

print(f"\nGenerated {len(publications)} publication files in {publications_dir}")
