# export_demo.py
import sqlite3

KEEP = {"solution", "case_study", "blog_posts", "gallery_image", "testimonial"}  # adjust
src = sqlite3.connect("database.db")

with open("demo_data.sql", "w", encoding="utf-8") as f:
    for line in src.iterdump():
        if line.startswith("INSERT INTO"):
            table = line.split('"')[1] if '"' in line else line.split()[2]
            if table in KEEP:
                f.write(line.replace("INSERT INTO", "INSERT OR IGNORE INTO", 1) + "\n")