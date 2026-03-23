from fpdf import FPDF
import os
import uuid

def generate_resume(
    name, email, phone, location, career_objective, education,
    technical_skills, non_technical_skills, projects, mini_projects,
    internships, achievements, workshops, languages, career_path,
    resume_format="modern"
):
    # Sanitize all text fields
    name = sanitize_text(name)
    email = sanitize_text(email)
    phone = sanitize_text(phone)
    location = sanitize_text(location)
    career_objective = sanitize_text(career_objective)
    education = sanitize_dict(education)
    technical_skills = [sanitize_text(s) for s in technical_skills]
    non_technical_skills = [sanitize_text(s) for s in non_technical_skills]
    projects = [sanitize_text(s) for s in projects]
    mini_projects = [sanitize_text(s) for s in mini_projects]
    internships = [sanitize_text(s) for s in internships]
    achievements = [sanitize_text(s) for s in achievements]
    workshops = [sanitize_text(s) for s in workshops]
    languages = [sanitize_text(s) for s in languages]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Professional Header Section
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, name.upper(), ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"{phone} | {email}", ln=True)
    pdf.cell(0, 7, f"{location}", ln=True)

    # Add LinkedIn and GitHub (placeholder - can be made dynamic)
    pdf.set_font("Arial", "I", 11)
    pdf.cell(0, 7, f"LinkedIn: linkedin.com/in/yourprofile | GitHub: github.com/yourprofile", ln=True)
    pdf.cell(0, 7, f"Career Focus: {career_path}", ln=True)

    pdf.ln(4)
    pdf.set_draw_color(180,180,180)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # Helper function for professional section titles
    def section_title(title):
        pdf.set_font("Arial", "B", 13)
        pdf.set_text_color(0,0,0)
        pdf.cell(0,8,title,ln=True)
        pdf.set_draw_color(200,200,200)
        pdf.line(10,pdf.get_y(),200,pdf.get_y())
        pdf.ln(3)

    # Professional Summary (NEW - Very Important)
    section_title("Professional Summary")
    pdf.set_font("Arial","",11)
    
    summary = f"""Motivated {career_path} with strong interest in software development,
machine learning and data analysis. Experienced in building projects
using modern technologies and eager to contribute to innovative
technology teams."""
    
    pdf.multi_cell(0,6,summary)
    pdf.ln(4)

    # Career Objective
    section_title("Career Objective")
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, career_objective)
    pdf.ln(4)

    # Education (Improved Format)
    section_title("Education")
    pdf.set_font("Arial","",11)
    
    pdf.cell(0,6,f"B.Tech - {education['btech']['college']}",ln=True)
    pdf.cell(0,6,f"CGPA: {education['btech']['cgpa']} | {education['btech']['duration']}",ln=True)
    pdf.ln(2)
    
    pdf.cell(0,6,f"Intermediate - {education['inter']['college']}",ln=True)
    pdf.cell(0,6,f"Percentage: {education['inter']['percentage']}%",ln=True)
    pdf.ln(2)
    
    pdf.cell(0,6,f"SSC - {education['ssc']['school']}",ln=True)
    pdf.cell(0,6,f"Percentage: {education['ssc']['percentage']}%",ln=True)
    pdf.ln(4)

    # Technical Skills (ATS-Friendly Format)
    section_title("Technical Skills")
    pdf.set_font("Arial","",11)
    
    if technical_skills:
        skills_line = " | ".join(technical_skills)
        pdf.multi_cell(0,6,skills_line)
    pdf.ln(3)

    # Non-Technical Skills
    section_title("Non-Technical Skills")
    pdf.set_font("Arial","",11)
    
    if non_technical_skills:
        skills_line = " | ".join(non_technical_skills)
        pdf.multi_cell(0,6,skills_line)
    pdf.ln(4)

    # Projects (Improved Format)
    if projects:
        section_title("Projects")
        pdf.set_font("Arial","",11)
        for proj in projects:
            # Use ASCII bullet instead of Unicode
            pdf.multi_cell(0,6,f"- {to_latin1_safe(proj)}")
            pdf.ln(1)
        pdf.ln(2)

    # Mini Projects
    if mini_projects:
        section_title("Mini/Community Projects")
        pdf.set_font("Arial","",11)
        for proj in mini_projects:
            # Use ASCII bullet instead of Unicode
            pdf.multi_cell(0,6,f"- {to_latin1_safe(proj)}")
            pdf.ln(1)
        pdf.ln(2)

    # Internships
    if internships:
        section_title("Internships")
        pdf.set_font("Arial","",11)
        for intern in internships:
            # Use ASCII bullet instead of Unicode
            pdf.multi_cell(0,6,f"- {to_latin1_safe(intern)}")
            pdf.ln(1)
        pdf.ln(2)

    # Achievements
    if achievements:
        section_title("Achievements & Certifications")
        pdf.set_font("Arial","",11)
        for ach in achievements:
            # Use ASCII bullet instead of Unicode
            pdf.multi_cell(0,6,f"- {to_latin1_safe(ach)}")
            pdf.ln(1)
        pdf.ln(2)

    # Workshops
    if workshops:
        section_title("Workshops & Volunteering")
        pdf.set_font("Arial","",11)
        for work in workshops:
            # Use ASCII bullet instead of Unicode
            pdf.multi_cell(0,6,f"- {to_latin1_safe(work)}")
            pdf.ln(1)
        pdf.ln(2)

    # Languages
    section_title("Languages")
    pdf.set_font("Arial","",11)
    if languages:
        languages_line = ", ".join([to_latin1_safe(s) for s in languages])
        pdf.multi_cell(0,6,languages_line)
    pdf.ln(4)

    # Declaration
    section_title("Declaration")
    pdf.set_font("Arial","",11)
    pdf.multi_cell(0,6,to_latin1_safe("I hereby declare that the information provided above is true to the best of my knowledge."))
    pdf.cell(0,6,to_latin1_safe(f"Place: {location}"),ln=True)
    pdf.cell(0,6,to_latin1_safe(f"Signature: {name.split()[0][0]}. {name.split()[-1]}"),ln=True)

    # Save
    output_dir = "generated_resumes"
    os.makedirs(output_dir, exist_ok=True)
    unique_id = uuid.uuid4().hex[:8]
    pdf_path = os.path.join('generated_resumes', f"{name.replace(' ', '_')}_{unique_id}.pdf")
    pdf.output(pdf_path)
    return pdf_path


def to_latin1_safe(s: str) -> str:
    """Convert string to a latin-1-safe representation by replacing common
    unicode characters (bullets, smart quotes, en/em dashes, emojis) with ASCII
    equivalents and removing characters outside latin-1 range.
    """
    if not isinstance(s, str):
        s = str(s)
    
    # First, replace all common unicode punctuation with ASCII
    replacements = {
        # Dashes and bullets - MOST IMPORTANT
        '\u2022': '-',  # bullet point (•)
        '\u2023': '-',  # triangular bullet
        '\u2043': '-',  # hyphen bullet
        '\u204C': '-',  # inverted bullet
        '\u2219': '-',  # bullet operator
        '\u25CB': '-',  # white circle
        '\u25CF': '-',  # black circle
        '\u25E6': '-',  # white bullet
        '\u26AB': '-',  # medium black circle
        '\u26AC': '-',  # medium white circle
        '•': '-',      # bullet (direct)
        '•': '-',      # bullet (alternative)
        '\u2013': '-',  # en dash
        '\u2014': '-',  # em dash
        '–': '-',      # en dash (direct)
        '—': '-',      # em dash (direct)
        # Quotes
        '\u2018': "'",  # left single quote
        '\u2019': "'",  # right single quote
        '\u201B': "'",  # single high-reversed-9 quote
        '\u2039': "'",  # single left-pointing angle quote
        '\u203A': "'",  # single right-pointing angle quote
        '\u201C': '"',  # left double quote
        '\u201D': '"',  # right double quote
        '\u201E': '"',  # double low-9 quote
        '\u2033': '"',  # double prime
        '\u2036': '"',  # reversed double prime
        '\u00AB': '"',  # left-pointing double angle quote
        '\u00BB': '"',  # right-pointing double angle quote
        "'": "'",      # left single quote (direct)
        "'": "'",      # right single quote (direct)
        '"': '"',      # left double quote (direct)
        '"': '"',      # right double quote (direct)
        # Spaces
        '\u00A0': ' ',  # non-breaking space
        '\u2000': ' ',  # en quad
        '\u2001': ' ',  # em quad
        '\u2002': ' ',  # en space
        '\u2003': ' ',  # em space
        '\u2004': ' ',  # three-per-em space
        '\u2005': ' ',  # four-per-em space
        '\u2006': ' ',  # six-per-em space
        '\u2007': ' ',  # figure space
        '\u2008': ' ',  # punctuation space
        '\u2009': ' ',  # thin space
        '\u200A': ' ',  # hair space
        '\u202F': ' ',  # narrow no-break space
        '\u205F': ' ',  # medium mathematical space
        '\u3000': ' ',  # ideographic space
        # Common emojis and symbols
        '\U0001f4e7': 'Email',  # 📧
        '\U0001f4f1': 'Phone',  # 📱
        '\U0001f4cd': 'Location',  # 📍
        '\U0001faf5': 'Career',  # 🎯
        '📧': 'Email',
        '📱': 'Phone', 
        '📍': 'Location',
        '🎯': 'Career',
        '✓': '✓',
        '✗': '✗',
        '→': '->',
        '←': '<-',
        '↑': '^',
        '↓': 'v',
        # Additional problematic characters
        '…': '...',  # ellipsis
        '—': '-',    # em dash
        '–': '-',    # en dash
        '"': '"',    # smart quotes
        "'": "'",    # smart quotes
        '"': '"',    # smart quotes
        "'": "'",    # smart quotes
    }
    
    for k, v in replacements.items():
        s = s.replace(k, v)

    # Remove any character that cannot be encoded in latin-1
    safe_chars = []
    for ch in s:
        try:
            ch.encode('latin-1')
            safe_chars.append(ch)
        except UnicodeEncodeError:
            # Replace with safe ASCII character
            if ch in '–—••':
                safe_chars.append('-')
            elif ch in '\u2018\u2019\u2018\u2019':  # left and right single quotes
                safe_chars.append("'")
            elif ch in '\u201c\u201d\u201c\u201d':  # left and right double quotes
                safe_chars.append('"')
            elif ch == ' ':
                safe_chars.append(' ')
            else:
                safe_chars.append('?')  # fallback for unknown characters
    return ''.join(safe_chars)

def sanitize_text(text):
    # Replace EN DASH and EM DASH with a regular hyphen
    if isinstance(text, str):
        return text.replace("–", "-").replace("—", "-")
    return text

def sanitize_dict(d):
    # Recursively sanitize all strings in a dict
    if isinstance(d, dict):
        return {k: sanitize_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [sanitize_dict(x) for x in d]
    else:
        return sanitize_text(d)
