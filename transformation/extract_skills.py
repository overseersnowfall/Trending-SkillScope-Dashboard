import sys, os, re
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_connection
from skills_list import get_all_skills

def find_skills_in_text(text, skills):
    """Return the list of skills that appear in the given text."""
    if not text:
        return []
    
    text_lower = text.lower()
    found = []

    for skill in skills:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found.append(skill)
    return found

def count_skills_by_role(conn):
    """
    Read every job from raw_jobs, find skills in each description,
    and count skill occurrences grouped by role.
    Returns a nested dict: {role: {skill: count}}
    """
    skills = get_all_skills()
    counts = defaultdict(lambda: defaultdict(int))

    cursor = conn.cursor()
    cursor.execute("SELECT source, description FROM raw_jobs WHERE description IS NOT NULL")
    rows = cursor.fetchall()
    cursor.close()

    print(f"Processing {len(rows)} job descriptions...")
    for role, description in rows:
        found_skills = find_skills_in_text(description, skills)
        for skill in found_skills:
            counts[role][skill] += 1
    return counts

def save_skill_counts(conn, counts):
    """Clear old counts and write the new ones into skill_counts."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM skill_counts")

    sql = """
        INSERT INTO skill_counts (role, skill, count)
        VALUES (%s, %s, %s)
    """
    for role, skill_dict in counts.items():
        for skill, count in skill_dict.items():
            cursor.execute(sql, (role, skill, count))
    conn.commit()
    cursor.close()

if __name__ == "__main__":
    conn = get_connection()
    counts = count_skills_by_role(conn)
    save_skill_counts(conn, counts)
    conn.close()
    print("\nTop skills per role:")
    for role, skill_dict in counts.items():
        topskills = sorted(skill_dict.items(), key=lambda x: x[1], reverse=True)[:10]#5 for top 5 skills
        print(f"\n{role}:")
        for skill, count in topskills:
            print(f"  {skill}: {count}")