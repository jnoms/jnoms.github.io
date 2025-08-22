#!/usr/bin/env python3

# Simple publications markdown generator for Jason Nomburg's website
# No pandas dependency - uses standard Python libraries

import csv
import os

# HTML escape function for YAML safety
html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
}

def html_escape(text):
    """Produce entities within text."""
    if not text or text == "":
        return ""
    return "".join(html_escape_table.get(c,c) for c in str(text))

# Clear existing publications directory
publications_dir = "../_publications/"
if not os.path.exists(publications_dir):
    os.makedirs(publications_dir)

# Read the publications TSV file
with open("publications_nomburg.tsv", 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='\t')
    
    publication_count = 0
    for row in reader:
        publication_count += 1
        
        md_filename = str(row['pub_date']) + "-" + row['url_slug'] + ".md"
        html_filename = str(row['pub_date']) + "-" + row['url_slug']
        year = row['pub_date'][:4]
        
        ## YAML variables
        md = "---\ntitle: \""   + html_escape(row['title']) + '"\n'
        md += """collection: publications\n"""
        
        # Categorize publications
        venue = str(row['venue']).lower()
        if 'nature' in venue or 'cell' in venue or 'science' in venue:
            md += """category: manuscripts\n"""
        elif 'biorxiv' in venue or 'arxiv' in venue:
            md += """category: preprints\n"""
        else:
            md += """category: manuscripts\n"""
        
        md += """\npermalink: /publication/""" + html_filename
        
        if len(str(row['excerpt'])) > 5:
            md += "\nexcerpt: '" + html_escape(row['excerpt']) + "'"
        
        md += "\ndate: " + str(row['pub_date']) 
        md += "\nvenue: '" + html_escape(row['venue']) + "'"
        
        if len(str(row['paper_url'])) > 5:
            md += "\npaperurl: '" + str(row['paper_url']) + "'"
        
        md += "\ncitation: '" + html_escape(row['citation']) + "'"
        md += "\n---"
        
        ## Markdown description for individual page
        if len(str(row['excerpt'])) > 5:
            md += "\n\n" + html_escape(row['excerpt']) + "\n"
        
        if len(str(row['paper_url'])) > 5:
            md += "\n\n<a href='" + str(row['paper_url']) + "'>Download paper here</a>\n" 
            
        # Bold the author's name in citation
        citation = html_escape(row['citation'])
        citation = citation.replace("Nomburg J", "**Nomburg J**")
        citation = citation.replace("Nomburg JL", "**Nomburg JL**")
        md += "\n\n" + citation
        
        # Write the markdown file
        md_filename = os.path.basename(md_filename)
        with open(publications_dir + md_filename, 'w', encoding='utf-8') as f:
            f.write(md)
        
        print(f"Generated: {md_filename}")

print(f"\nGenerated {publication_count} publication files in {publications_dir}")
