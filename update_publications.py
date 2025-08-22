#!/usr/bin/env python3
"""
Simple Publication Updater for Academic Website
===============================================

This script reads publications.csv and updates your Jekyll website.

Usage:
    python update_publications.py

CSV Format:
    Date,Title,Authors,Journal,DOI,Description
    
Author Formatting:
    * = co-first author (e.g., "Smith A*, Jones B*")
    # = co-corresponding author (e.g., "Smith A#, Jones B#")
    
The script will:
    1. Read publications.csv
    2. Generate markdown files in _publications/
    3. Bold your name automatically
    4. Style co-first (*) and co-corresponding (#) authors
    5. Link titles to DOI URLs
"""

import csv
import os
import re
from datetime import datetime

# Configuration
AUTHOR_NAME = "Nomburg J"  # Your name variations to bold
AUTHOR_VARIATIONS = ["Nomburg J", "Nomburg JL", "Nomburg JE"]

def clean_filename(title):
    """Convert title to a clean filename slug."""
    # Remove special characters, convert to lowercase, replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:50]  # Limit length

def format_authors(authors):
    """Format author list with styling for co-first (*) and co-corresponding (#) authors."""
    # Replace * with red styling for co-first authors (only the asterisk is red)
    formatted = re.sub(r'(\w+\s+\w+)\*', r'\1<span style="color:red">*</span>', authors)
    
    # Replace # with blue styling for co-corresponding authors (only the # is blue)
    formatted = re.sub(r'(\w+\s+\w+)#', r'\1<span style="color:blue">#</span>', formatted)
    
    # Bold the target author name variations using HTML tags
    for name_var in AUTHOR_VARIATIONS:
        # Handle cases where the author name might have * or # after it with styling
        # Look for the name followed by styled * or #
        pattern_red = f'({re.escape(name_var)})<span style="color:red">\\*</span>'
        replacement_red = r'<strong>\1</strong><span style="color:red">*</span>'
        formatted = re.sub(pattern_red, replacement_red, formatted)
        
        pattern_blue = f'({re.escape(name_var)})<span style="color:blue">#</span>'
        replacement_blue = r'<strong>\1</strong><span style="color:blue">#</span>'
        formatted = re.sub(pattern_blue, replacement_blue, formatted)
        
        # Handle regular name without * or #
        pattern_plain = f'\\b{re.escape(name_var)}\\b(?!<)'
        replacement_plain = f'<strong>{name_var}</strong>'
        formatted = re.sub(pattern_plain, replacement_plain, formatted)
    
    return formatted

def create_citation(authors, year, title, journal):
    """Create a properly formatted citation."""
    formatted_authors = format_authors(authors)
    return f'{formatted_authors} ({year}). "{title}" <i>{journal}</i>.'

def generate_markdown(row):
    """Generate markdown content for a publication."""
    date = row['Date']
    title = row['Title'] 
    authors = row['Authors']
    journal = row['Journal']
    doi = row['DOI']
    description = row['Description']
    
    # Create URL slug
    slug = clean_filename(title)
    
    # Extract year from date
    year = date[:4]
    
    # Create citation
    citation = create_citation(authors, year, title, journal)
    
    # Create DOI URL
    doi_url = f"https://doi.org/{doi}"
    
    # Generate markdown content
    md_content = f"""---
title: "{title}"
collection: publications
category: manuscripts
permalink: /publication/{date}-{slug}
excerpt: '{description}'
date: {date}
venue: '{journal}'
paperurl: '{doi_url}'
citation: '{citation}'
---

{description}

<a href='{doi_url}'>Download paper here</a>

{citation}
"""
    
    return f"{date}-{slug}.md", md_content

def main():
    """Main function to update publications."""
    print("🚀 Starting publication update...")
    
    # Check if CSV exists
    if not os.path.exists('publications.csv'):
        print("❌ Error: publications.csv not found!")
        print("📝 Create a publications.csv file with columns: Date,Title,Authors,Journal,DOI,Description")
        return
    
    # Create publications directory if it doesn't exist
    publications_dir = "_publications"
    if not os.path.exists(publications_dir):
        os.makedirs(publications_dir)
    
    # Clear existing publications
    print("🧹 Clearing existing publications...")
    for file in os.listdir(publications_dir):
        if file.endswith('.md'):
            os.remove(os.path.join(publications_dir, file))
    
    # Read CSV and generate markdown files
    print("📚 Processing publications...")
    publication_count = 0
    
    with open('publications.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            filename, content = generate_markdown(row)
            
            # Write markdown file
            filepath = os.path.join(publications_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as md_file:
                md_file.write(content)
            
            publication_count += 1
            print(f"  ✅ Generated: {filename}")
    
    print(f"\n🎉 Successfully generated {publication_count} publications!")
    print(f"📂 Files created in {publications_dir}/")
    print("\n📋 Next steps:")
    print("  1. Review the generated files")
    print("  2. git add . && git commit -m 'Update publications' && git push")
    print("  3. Your website will update automatically!")

if __name__ == "__main__":
    main()
