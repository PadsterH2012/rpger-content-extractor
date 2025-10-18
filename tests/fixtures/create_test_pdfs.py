#!/usr/bin/env python3
"""
Create simple test PDF files for testing
"""

import os
from pathlib import Path

def create_simple_pdf(filename: str, content: str):
    """Create a simple PDF file with text content"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        pdf_path = Path(filename)
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        
        # Add content to PDF
        lines = content.split('\n')
        y_position = 750
        
        for line in lines:
            if y_position < 50:  # Start new page if needed
                c.showPage()
                y_position = 750
            c.drawString(50, y_position, line)
            y_position -= 20
        
        c.save()
        print(f"✅ Created {filename}")
        return True
        
    except ImportError:
        # Fallback: create a simple text file with .pdf extension
        # This won't be a real PDF but will prevent FileNotFoundError
        with open(filename, 'w') as f:
            f.write(f"%PDF-1.4\n")
            f.write(f"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
            f.write(f"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
            f.write(f"3 0 obj\n<< /Type /Page /Parent 2 0 R /Contents 4 0 R >>\nendobj\n")
            f.write(f"4 0 obj\n<< /Length {len(content)} >>\nstream\n")
            f.write(content)
            f.write(f"\nendstream\nendobj\n")
            f.write(f"xref\n0 5\n0000000000 65535 f\n")
            f.write(f"trailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n0\n%%EOF\n")
        
        print(f"✅ Created simple {filename} (text-based)")
        return True

def main():
    """Create all test PDF files"""

    # Create PDFs in the pdfs subdirectory
    pdfs_dir = Path(__file__).parent / "pdfs"
    pdfs_dir.mkdir(exist_ok=True)

    test_files = {
        "test.pdf": """DUNGEONS & DRAGONS
Player's Handbook
5th Edition

CHAPTER 1: STEP-BY-STEP CHARACTERS

Your first step in playing an adventurer in the Dungeons & Dragons game is to imagine and create a character of your own. Your character is a combination of game statistics, roleplaying hooks, and your imagination.

ABILITY SCORES
Six abilities provide a quick description of every creature's physical and mental characteristics:

Strength, measuring physical power
Dexterity, measuring agility
Constitution, measuring endurance
Intelligence, measuring reasoning ability
Wisdom, measuring awareness
Charisma, measuring force of personality

ARMOR CLASS
Your Armor Class (AC) represents how well your character avoids being wounded in battle.""",

        "novel.pdf": """THE HOBBIT
by J.R.R. Tolkien

Chapter 1: An Unexpected Party

In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort.

It had a perfectly round door like a porthole, painted green, with a shiny yellow brass knob in the exact middle. The door opened on to a tube-shaped hall like a tunnel: a very comfortable tunnel without smoke, with panelled walls, and floors tiled and carpeted, provided with polished chairs, and lots and lots of pegs for hats and coats - the hobbit was fond of visitors.""",

        "empty.pdf": "",

        "large.pdf": """PATHFINDER CORE RULEBOOK
Second Edition

""" + "This is a large PDF file with lots of content. " * 1000,

        "scanned.pdf": """This is a scanned PDF with OCR artifacts.
The qu1ck br0wn f0x jumps 0ver the 1azy d0g.
S0me characters are c0nfused by 0CR.
Th1s 1s c0mm0n 1n scanned d0cuments.""",

        "special_chars.pdf": """Special Characters Test
Café, naïve, résumé, piñata
Mathematical symbols: α, β, γ, δ, ∑, ∫, ∞
Currency: €, £, ¥, ₹, $
Quotes: "smart quotes" and 'apostrophes'
Em-dash — and en-dash –""",

        "test_book.pdf": """RPG Source Material
Game Type: D&D
Edition: 5th Edition
ISBN: 978-0-7869-6561-5

This is a test book for metadata extraction."""
    }
    
    print("🔧 Creating test PDF files...")
    
    for filename, content in test_files.items():
        try:
            filepath = pdfs_dir / filename
            create_simple_pdf(str(filepath), content)
        except Exception as e:
            print(f"❌ Failed to create {filename}: {e}")
    
    print("✅ Test PDF creation completed!")

if __name__ == "__main__":
    main()
