!pip install pandas reportlab

import subprocess

# Install necessary packages
subprocess.check_call(['pip', 'install', 'pandas', 'reportlab'])

from google.colab import drive
drive.mount('/content/drive')
drive.mount("/content/drive", force_remount=True)

!pip install PyPDF2

# @title Default title text
import streamlit as st
import pandas as pd
#from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from IPython.display import FileLink
from reportlab.lib.units import inch,mm
from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib import colors
import io
from io import BytesIO
import os
from reportlab.lib.pagesizes import letter , A4
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle# Import getSampleStyleSheet here


st.title("CSV to PDF Generator with Predefined Logo and Base PDF")
uploaded_csv = st.file_uploader("Upload a CSV file", type=["csv"])

# Load the CSV data (ensure the correct path to your CSV file)
data = pd.read_csv('/content/drive/My Drive/Colab Notebooks/CGA.csv')

# Strip any extra spaces in column names
data.columns = data.columns.str.strip()

# Print column names to check for discrepancies
print(data.columns)

section_intros = {
    "Career Clarity": "Career clarity is the extent to which you are clear about your purpose, career goals, and the steps that you need to take to fulfill your career aspirations.",
    "Professional Satisfaction": "Professional satisfaction is a measure of how satisfied and happy you are with what you do at work and the way you are rewarded for it.",
    "Market Value": "Market Value is the measure of market feedback on the attractiveness of one's profile for the top in demand roles in the job market. Market value is based on market evaluation of your profile and is driven by the supply and demand principles.",
    "Learning Agility": "Learning agility is the intent and ability to unlearn and learn, upskill and re-skill to keep pace with the changing demands of your job and career aspirations.",
    "Workplace Perception": "Workplace perception is people's impression about you at the workplace. This factor determines the degree of reliability, credibility and trustworthiness they show in you before assigning any important task, responsibility, or project."
}

# Define the messages for each section
messages = {
    "Career Clarity": {
        "low": """You need to ensure that you are investing sufficient time in getting necessary clarity
        before taking the next big step in your career. We recommend you talk to coaches, mentors, and
        industry experts to understand your strengths, weaknesses, and interest areas, industry trends,
        and future of work. After gaining the necessary career clarity, we recommend you define your
        SMART goals along with a concrete action plan which will help you to channelise your efforts
        in the right direction to have a rewarding career. Failing to do so will result in you
        underachieving in terms of what you truly deserve.You can also seek professional guidance to
        gain systematic clarity and create a personalised Career Evaluation Action Plan (CEAP) so that
        you are not missing out on anything important.""",
        "moderate": """It’s good that you already have decent clarity on what you want in your career.
        But there are a few areas where you still need to gain insights. Make sure you are investing
        sufficient time talking to Industry experts, mentors, and coaches to know your strengths/weaknesses
        and work on it to keep pace with the industry trends and the future of work. We recommend you define
        SMART goals for yourself along with a concrete action plan which will help you channelise your efforts
        and energy in the right direction to have a rewarding career. Failing to do so will result in you
        underachieving in terms of what you truly deserve.You can also seek professional guidance to gain
        systematic clarity and create a personalised Career Evaluation Action Plan (CEAP) so you are not
        missing out on anything important.""",
        "high": "It's great that you know what you want in your career."
    },
    "Professional Satisfaction": {
        "low": """There are elements in your professional life which are not appropriately aligned. You need
        to reflect deeply over your experiences to understand what kind of work makes you feel
        happy/excited and can be pursued as a career option. You can also identify work which makes
        you feel proud and can attract monetary benefits. Acquiring new age skills could be another
        way to increase your professional satisfaction quotient. It will give you better job opportunities,
        compensation, and recognition. It will also increase your degree of freedom to choose from various
        roles/domains/organisations and pursue a career of your choice.It’s very important for you to act at
        this juncture of your career and not taking the right steps will soon result in complete burn-out or
        loss of motivation.You can seek expert advice to understand how you can have a highly satisfied
        professional life and what are the hidden behaviour patterns which are hindering your career growth.""",
        "moderate": """Most of the fundamental elements of your professional life are aligned with your
        strengths and areas of interest but some factors still need recalibration and improvement.
        You need to identify those factors and create an action plan to strengthen them so that they
        are not becoming roadblocks to your future growth. To increase your professional satisfaction
        quotient, you can find work which gives you more happiness, fulfillment or a feeling of
        pride and contentment. You can acquire new age skills which will give you better job opportunities,
        higher compensation, recognition, and job security. It will increase your degree of freedom to choose
        from various roles/domains/organisations and have a higher professional satisfaction.You can seek
        expert advice to carefully plan your next career move which can help you grow professionally without
        losing your true essence and identity. Failing to do so can lead you towards dissonance and demotivation.""",
        "high": "You have high contentment and satisfaction in your professional life."
    },
    "Market Value": {
        "low": """It's high time you start taking actions which could help you build a stronger profile.
        Seek opportunities to work on high-stake and futuristic projects in your current role. This could
        help you showcase your leadership qualities and achieve great results.Plan to upskill and cross-skill
        yourself which can help you move into roles which are more in demand.Work on your visibility to cut
        competition in the market and attract top recruiters. We recommend you create a Blue Ocean Strategy
        for professional networking which could help position you uniquely in the market and establish you as a
        personal brand over a period of time.You are currently lagging behind in comparison to your peers and
        not taking the right steps urgently will lead you to becoming a not so sought after candidate in the
        job market. You can get in touch with professional career coaches to seek the right guidance and early
        interventions.""",
        "moderate": """At this juncture of your career, it’s extremely crucial for you to start working towards
        building a stronger profile which drastically reduces your competition in the job market.Seek
        opportunities to work on high-stake and futuristic projects in your current role.This could help you
        showcase your leadership qualities and achieve greater results.Plan to upskill and cross-skill yourself
        which can help you move into a role which is more in demand.Work on your visibility to cut competition
        in the market and attract top recruiters. We recommend you create a Blue Ocean Strategy for professional
        networking which could help position you as an expert in the industry and establish you as a personal brand.
        Not taking the right steps may lead you to becoming a not so sought after candidate in the job market
        over a period of time. You can get in touch with a professional career coach to seek right guidance and
        early interventions.""",
        "high": "You have a high degree of confidence and visibility in the market."
    },
    "Learning Agility": {
        "low": """With the changing dynamics of the business environment, growth-mode organisations are adopting
        agile work environments. You need to have a high learning agility quotient to keep pace with the
        ever-changing industry standards. You should work on developing a flexible mindset towards adapting to
        change. The skills and competencies which helped you grow till date will not help you reach where you
        want to see yourself in the next four to five years. Make serious commitments to acquire desirable skills
        to keep pace with future demands, create learning plans with a weekly engagement of at least 10-12 hours.
        Unlearning and learning is the need of the hour and not doing so will lead to your current skills becoming
        irrelevant.""",
        "moderate": """You are agile enough to perform well in a dynamic role. You can still work on your
        learning agility quotient to keep pace with evolving career trends. There are times where you take
        more than required time to "test waters" which may result in you losing sight of great opportunities.
        Make sure you are challenging your limits to become the best version of yourself. The skills and
        competencies that helped you grow till date may not help you reach where you want to see yourself in
        the next four to five years. Make serious commitments to acquire desirable skills to keep pace with
        the future demands, create learning plans with a weekly engagement of at least 10-12 hours. With the
        changing dynamics of the business environment, growth-mode organisations are adopting agile work
        environments. You need to make unlearning-learning a part of your life to reap the best results. Not
        doing so may result in your skills becoming irrelevant.""",
        "high": "You are highly agile and able to adapt quickly in dynamic roles."
    },
    "Workplace Perception": {
        "low": """Low score on workplace perception means that you need to re-think about your contribution to
        the workplace. There can be many reasons behind low perception. One could be that your hard/soft skills,
        competencies, and personality traits are not up to the mark as per the requirements of the role.
        Another reason could be that you are a misfit to the role and your skills and personality traits are
        not in line with what is expected out of the role. It could also be possible that you are not able to
        understand the larger view of the organisation and are struggling to align yourself with the same.
        Your ability or way to communicate also plays an important role in building a positive perception.
        On an immediate basis, you need to take help from a coach or expert who could help you reflect over
        the hidden reasons behind low workplace perception and curate a strategy to improve the same.""",
        "moderate": """Moderate score on workplace perception means that perception about you is impacting
        your career growth to some extent and you need to act on this to ensure that this does not become a
        major barrier to your career growth over a period of time. One way could be through building new age
        skills and deep knowledge of your industry. Another way could be evaluating your hard/soft skills,
        competencies, personality traits, and finding a role where these could be valued more. There can be
        a possibility that you lack a holistic/larger view of the company and need to align yourself with the
        organisation’s vision. Working on your way/ability to communicate can also help you improve your
        perception further. We recommend you to take help from a coach or an expert who could help you
        reflect/introspect over the hidden reasons and curate a strategy to build a positive perception.""",
        "high": "High perception score shows strong positive perception at work."
    }
}

# Function to calculate the average for each section
def calculate_section_average(scores):
    # Filter out NaN values
    scores = [score for score in scores if pd.notna(score)]

    # Check if there are any valid scores after filtering
    if not scores:  # If the list is empty (no valid scores)
        return 0  # Return 0 (or a default value like np.nan if preferred)

    # Calculate the average
    average = sum(scores) / len(scores)

    # Return the rounded average
    return round(average, 2)

# Load Poppins font
pdfmetrics.registerFont(TTFont('Poppins', '/content/drive/My Drive/Colab Notebooks/Poppins-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Poppins-Bold', '/content/drive/My Drive/Colab Notebooks/Poppins-Bold.ttf'))

# Update path to your logo file
LOGO_PATH ='/content/drive/My Drive/Colab Notebooks/upgrad_logo.png'  # Adjust the path to the location of the upGrad logo

def wrap_text(text, line_width, canvas_obj):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        # Check if adding the word exceeds the line width
        if canvas_obj.stringWidth(line + word + " ") < line_width:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)  # Add the last line
    return lines

def add_details_to_third_page(page, pdf_writer, candidate_data):
    """
    Adds candidate details to the third page of the base PDF with purple heading and additional graphics.
    """
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Set colors
    heading_color = colors.HexColor("#611e9b")  # Purple heading
    box_color = colors.HexColor("#F0F0F0")
    line_color = colors.HexColor("#611e9b")
    text_color = colors.black

    # Heading
    can.setFont("Helvetica-Bold", 16)
    can.setFillColor(heading_color)
    can.drawString(50, 580, "Candidate Profile Overview")  # Position of the heading

    # Draw a decorative line under the heading
    can.setLineWidth(2)
    can.line(50, 575, 300, 575)

    # Dimensions for rectangles
    rect_width = 220
    rect_height = 100
    rect_y = 450

    # Draw first rectangle (Current details)
    can.setFillColor(box_color)
    can.rect(50, rect_y, rect_width, rect_height, fill=1)

    # Draw second rectangle (Target details)
    can.setFillColor(box_color)
    can.rect(320, rect_y, rect_width, rect_height, fill=1)

    # Centered arrow calculations
    arrow_y = rect_y + rect_height / 2  # Midpoint of rectangles (Y-axis)
    arrow_start_x = 270
    arrow_end_x = 320

    # Draw centered arrow
    can.setStrokeColor(line_color)
    can.setLineWidth(2)
    can.line(arrow_start_x, arrow_y, arrow_end_x, arrow_y)  # Arrow shaft
    can.line(arrow_end_x - 10, arrow_y + 10, arrow_end_x, arrow_y)  # Arrowhead (top)
    can.line(arrow_end_x - 10, arrow_y - 10, arrow_end_x, arrow_y)  # Arrowhead (bottom)

    # Set text properties
    can.setFont("Helvetica", 10)
    can.setFillColor(text_color)

    # Current details
    current_details = {
        "Current Domain": candidate_data.get('Current Domain', 'N/A'),
        "Current CTC": f"{candidate_data.get('Current CTC(LPA)', 'N/A')} LPA",
        "Role": candidate_data.get('Nature of Role', 'N/A'),
        "Level": candidate_data.get('Level', 'N/A')
    }

    # Target details
    target_details = {
        "Target Domain": candidate_data.get('Target Work Domain', 'N/A'),
        "Target CTC": f"{candidate_data.get('Target CTC(LPA)', 'N/A')} LPA"
    }

    # Draw text in the first rectangle (Current details)
    x_start = 60
    y_start = rect_y + rect_height - 20
    for label, value in current_details.items():
        can.drawString(x_start, y_start, f"{label}: {value}")
        y_start -= 20  # Line spacing

    # Draw text in the second rectangle (Target details)
    x_start = 330
    y_start = rect_y + rect_height - 20
    for label, value in target_details.items():
        can.drawString(x_start, y_start, f"{label}: {value}")
        y_start -= 20  # Line spacing

    # Finalize and merge
    can.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)
    page.merge_page(new_pdf.pages[0])
    pdf_writer.add_page(page)



def add_dynamic_table(page, pdf_writer, sections, candidate_data):
    """Adds a dynamic table to the specified page of the base PDF.

    Args:
        page: The page object from PyPDF2 for the given page.
        pdf_writer: The PdfWriter object to which the modified page will be added.
        sections: A dictionary with section names as keys and a list of related questions as values.
        candidate_data: A dictionary with candidate responses where the key is the question name.
        logo_path: Path to the logo image for branding."""

    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    styles = getSampleStyleSheet()
    style_normal = styles['BodyText']

    width, height = letter
    left_margin = 50
    top_margin = height - 50





    # Prepare data for the table
    y_position = height - 200
    data = [["Factor", "Score", "Recommended Action"]]
    for section, questions in sections.items():
        section_scores = [candidate_data.get(q, 0) for q in questions]
        average_score = sum(section_scores) / len(section_scores) if section_scores else 0
        recommendation = (
            f"Your career health score for {section} is high. Keep up the great work!"
            if average_score >= 8 else
            f"Your career health score for {section} is moderate. Consider improving in this area."
            if 5 <= average_score < 8 else
            f"Your career health score for {section} is low. Take action to improve this factor."
        )
        data.append([Paragraph(section, style_normal), f"{average_score:.1f}", Paragraph(recommendation, style_normal)])

    # Draw the table
    table = Table(data, colWidths=[150, 60, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Adjust table position and draw
    table.wrapOn(can, left_margin, y_position - 50)
    table.drawOn(can, left_margin, y_position - 200)

    can.save()

    # Merge the content with the original page
    packet.seek(0)
    new_pdf = PdfReader(packet)
    page.merge_page(new_pdf.pages[0])

    # Add the updated page to the PDF writer
    pdf_writer.add_page(page)


def create_report_content_pdf(candidate_data, messages):
    name = candidate_data['Name']
    report_filename = f"/content/{name}_report_content.pdf"
    c = canvas.Canvas(report_filename, pagesize=A4)
    width, height = A4
    left_margin = 80



    sections = {
        "Career Clarity": ['I am fully aware of the current job market trends and know what will be in demand over the next four to five years.', 'I clearly know which skills I lack and how critical it is for me to acquire them to have a rewarding and bright career in the next 3 years.', 'I am clear about the top five companies that I need to strive after to achieve my career aspirations.'],
        "Professional Satisfaction": ['Going to work makes me extremely happy and I thoroughly enjoy my current work.', 'I am extremely happy and satisfied with my current salary and compensation.', 'I am proud that I have achieved my career goals which I dreamt of two to three years ago.'],
        "Market Value": ['If I were to change my job, I am highly confident to get a desired job and good salary hike in next 30 days.', 'I have been approached by a lot of recruiters in the last six months due to my niche skills and unique value proposition.', 'I have a strong network of top professionals who can help me in getting my next dream job.'],
        "Learning Agility": ['I am willing to sacrifice my comfort zone to continuously work towards improving myself.', 'If required, I am willing to devote 10-12 hours each week to upskill in pursuit of my career growth.', 'I can easily unlearn and learn new skills to keep pace with changing work demands like automation and industry trends.'],
        "Workplace Perception": ['I believe I am a highly valuable resource to my organization for the skills I possess and my educational background.', 'My colleagues/peers have a high regard for me due to my contribution towards work.', 'I am considered to be a high potential employee in my organization and my managers foresee me in a bigger role in the next two to three years.']
    }

    total_average = 0
    section_count = 0

    logo_x = 165 * mm  # Position horizontally, adjust to fit your layout
    logo_y = 15 * mm   # Position vertically, ensure no overlap with other elements
    logo_width = 35 * mm
    logo_height = 10.85 * mm
    logo_path = '/content/drive/My Drive/Colab Notebooks/logo.jpeg'

    for section, question_columns in sections.items():
    # Calculate section scores and average
      section_scores = [candidate_data[col] for col in question_columns]
      section_average = calculate_section_average(section_scores)

      # Fetch the section introduction
      section_intro = section_intros.get(section, "No introduction provided")

      # Accumulate averages for total calculation
      total_average += section_average
      section_count += 1

      # Section title rectangle
      c.setFillColor(HexColor("#611e9b"))
      c.roundRect(left_margin, height - 130, width - 2 * left_margin, 25, 10, fill=1, stroke=0)
      c.setFillColor(HexColor("#ffffff"))
      c.setFont("Poppins-Bold", 14)
      c.drawCentredString(width / 2, height - 125, f"{section}")

      # Display average score in the top-right corner
      c.setFillColor(HexColor("#611e9b"))
      c.circle(width - 100, height - 125, 50, fill=1)
      c.setFillColor(HexColor("#ffffff"))
      c.setFont("Poppins-Bold", 12)
      c.drawCentredString(width - 100, height - 130, f"Avg Score: {section_average:.2f}")

      # Section introduction rectangle
      intro_y_position = height - 180
      intro_padding = 10
      intro_text = wrap_text(section_intro, width - 2 * left_margin - 40, c)
      intro_height = len(intro_text) * 15 + intro_padding * 2

      c.setFillColor(HexColor("#f4f4f4"))
      c.rect(left_margin - intro_padding, intro_y_position - intro_height + intro_padding,
            width - 2 * left_margin + 2 * intro_padding, intro_height, fill=1, stroke=0)

      # Draw section introduction text
      c.setFillColor(HexColor("#414041"))
      c.setFont("Poppins", 10.2)
      y_text_position = intro_y_position - intro_padding
      for line in intro_text:
          c.drawString(left_margin, y_text_position, line)
          y_text_position -= 15

      # Determine message based on section average
      y_message_position = intro_y_position - intro_height - 20
      if section_average < 7:
          message = messages[section]["low"]
      elif 7 <= section_average <= 8.99:
          message = messages[section]["moderate"]
      else:
          message = messages[section]["high"]

      # Message rectangle
      message_padding = 10
      wrapped_message = wrap_text(message, width - 2 * left_margin - 40, c)
      message_height = len(wrapped_message) * 15 + message_padding * 2

      c.setFillColor(HexColor("#f4f4f4"))
      c.rect(left_margin - message_padding, y_message_position - message_height + message_padding,
            width - 2 * left_margin + 2 * message_padding, message_height, fill=1, stroke=0)

      # Draw the message text
      c.setFillColor(HexColor("#414041"))
      y_message_text_position = y_message_position - message_padding
      for line in wrapped_message:
          c.drawString(left_margin, y_message_text_position, line)
          y_message_text_position -= 15

      # Add the logo
      c.drawImage(logo_path, logo_x, height - logo_y, width=logo_width, height=logo_height)

      c.showPage()

      overall_average = round(total_average / section_count, 2) if section_count > 0 else 0
    c.setFont("Poppins-Bold", 11)
    c.setFillColor(HexColor("#6119eb"))
    c.drawString(left_margin, height - 50, f"Overall Average Score: {overall_average}")

    # Determine the overall message based on the average score
    if overall_average < 7:
        overall_message = """Your overall performance indicates a need for improvement across multiple areas. Consider
        seeking personalized counseling to identify the specific areas where you can grow.
        With focused guidance, you can work on building your strengths and addressing any gaps.
        Together, we can help you chart a path to success."""
    elif 7 <= overall_average <= 8.99:
        overall_message = """Your overall performance is decent, but there are areas where you can excel further. We
        recommend personalized counseling to help you refine your skills and enhance your performance.
        Targeted guidance can help you push your limits and unlock your full potential, leading to even greater success."""
    else:
        overall_message = """Excellent performance! Keep up the high standards and consistency. To further accelerate
        your growth, personalized counseling can help you maintain your edge.
        It will also help you explore ways to deepen your expertise, stay ahead of the curve, and continually challenge yourself."""

    # Wrap the message text
    wrapped_message = wrap_text(overall_message, width - 2 * left_margin - 20, c)

    # Set the background color for the message
    message_background_color = HexColor("#f4f4f4")
    text_height = len(wrapped_message) * 15 + 10
    c.setFillColor(message_background_color)
    c.rect(left_margin, height - 105 - text_height, width - 2 * left_margin, text_height, fill=1, stroke=0)

    # Set the text color to #414041 and draw the wrapped message
    c.setFillColor(HexColor("#414041"))
    y_position = height - 120
    for line in wrapped_message:
        c.drawString(left_margin + 10, y_position, line)
        y_position -= 15
    c.drawImage(logo_path, logo_x, height - logo_y, width=logo_width, height=logo_height)
    c.save()


    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    styles = getSampleStyleSheet()
    style_normal = styles['BodyText']

    width, height = letter
    left_margin = 50
    top_margin = height - 50

    # Calculate overall average score
    total_average = sum(candidate_data.get(q, 0) for q in sections.keys())
    section_count = len(sections)
    overall_average = round(total_average / section_count, 2) if section_count > 0 else 0

    # Draw Overall Average Score
    can.setFont("Helvetica-Bold", 11)
    can.setFillColor(HexColor("#6119eb"))
    can.drawString(left_margin, top_margin, f"Overall Average Score: {overall_average}")

    # Determine the overall message
    if overall_average < 7:
        overall_message = """Your overall performance indicates a need for improvement across multiple areas..."""
    elif 7 <= overall_average <= 8.99:
        overall_message = """Your overall performance is decent, but there are areas where you can excel further..."""
    else:
        overall_message = """Excellent performance! Keep up the high standards and consistency..."""

    wrapped_message = wrap_text(overall_message, width - 2 * left_margin - 20, can)

    # Draw the message background
    text_height = len(wrapped_message) * 15 + 10
    can.setFillColor(HexColor("#f4f4f4"))
    can.rect(left_margin, top_margin - 20 - text_height, width - 2 * left_margin, text_height, fill=1, stroke=0)

    # Draw the message text
    can.setFillColor(HexColor("#414041"))
    y_position = top_margin - 35
    for line in wrapped_message:
        can.drawString(left_margin + 10, y_position, line)
        y_position -= 15


    return report_filename


def create_name_overlay(name):
    """Creates an overlay PDF with the candidate's name, formatted with a larger font and centered."""
    overlay_buffer = BytesIO()
    c = canvas.Canvas(overlay_buffer, pagesize=A4)

    # Set a larger font size (e.g., 20)
    font_size = 20
    c.setFont("Poppins", font_size)

    # Calculate text width and position to center the text
    text = f"Candidate Name: {name}"
    text_width = c.stringWidth(text, "Poppins", font_size)
    x_position = (A4[0] - text_width) / 2  # A4[0] is the width of the page

    # Position the text vertically, here it's 400, you can adjust it as per your requirement
    y_position = 200  # Adjust as needed

    # Draw the centered text
    c.setFillColor(black)  # Set text color to black
    c.drawString(x_position, y_position, text)

    c.showPage()
    c.save()

    overlay_buffer.seek(0)  # Ensure we return the buffer to the beginning
    return overlay_buffer

def generate_final_report(candidate_data, base_pdf_path, messages):
    """
    Generate a final report for a candidate by applying overlays, adding content, and modifying pages.
    """
    candidate_name = candidate_data['Name']


    # Load base PDF
    with open(base_pdf_path, 'rb') as base_pdf_file:
        pdf_reader = PdfReader(base_pdf_file)
        pdf_writer = PdfWriter()


        sections = {
        "Career Clarity": ['I am fully aware of the current job market trends and know what will be in demand over the next four to five years.', 'I clearly know which skills I lack and how critical it is for me to acquire them to have a rewarding and bright career in the next 3 years.', 'I am clear about the top five companies that I need to strive after to achieve my career aspirations.'],
        "Professional Satisfaction": ['Going to work makes me extremely happy and I thoroughly enjoy my current work.', 'I am extremely happy and satisfied with my current salary and compensation.', 'I am proud that I have achieved my career goals which I dreamt of two to three years ago.'],
        "Market Value": ['If I were to change my job, I am highly confident to get a desired job and good salary hike in next 30 days.', 'I have been approached by a lot of recruiters in the last six months due to my niche skills and unique value proposition.', 'I have a strong network of top professionals who can help me in getting my next dream job.'],
        "Learning Agility": ['I am willing to sacrifice my comfort zone to continuously work towards improving myself.', 'If required, I am willing to devote 10-12 hours each week to upskill in pursuit of my career growth.', 'I can easily unlearn and learn new skills to keep pace with changing work demands like automation and industry trends.'],
        "Workplace Perception": ['I believe I am a highly valuable resource to my organization for the skills I possess and my educational background.', 'My colleagues/peers have a high regard for me due to my contribution towards work.', 'I am considered to be a high potential employee in my organization and my managers foresee me in a bigger role in the next two to three years.']
    }
        # Add overlay to the first page
        overlay_pdf = create_name_overlay(candidate_name)
        overlay_reader = PdfReader(overlay_pdf)

        # Apply the overlay to the first page
        first_page = pdf_reader.pages[0]  # Read the first page
        first_page.merge_page(overlay_reader.pages[0])  # Apply the overlay
        pdf_writer.add_page(first_page)


        logo_path = '/content/drive/My Drive/Colab Notebooks/logo.jpeg'
        # Add remaining pages (skip the first page)
        for page_number in range(1, len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            if page_number == 2:  # Modify the third page
                print("Modifying third page...")
                add_details_to_third_page(page, pdf_writer, candidate_data)
            else:
                pdf_writer.add_page(page)


        # Add content pages
        content_pdf = create_report_content_pdf(candidate_data, messages)
        content_reader = PdfReader(content_pdf)
        skipped_page = None  # Variable to store the sixth page
        for page_number, page in enumerate(content_reader.pages, start=1):
            if page_number == 6:
                skipped_page = page  # Save the sixth page
                continue  # Skip adding this page to the writer
            pdf_writer.add_page(page)  # Add all other pages
        #for page in content_reader.pages:
         #   pdf_writer.add_page(page)

        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        styles = getSampleStyleSheet()
        style_normal = styles['BodyText']

        width, height = letter
        left_margin = 50
        top_margin = height - 50





        # Prepare data for the table
        y_position = height - 200
        data = [["Factor", "Score", "Recommended Action"]]
        for section, questions in sections.items():
            section_scores = [candidate_data.get(q, 0) for q in questions]
            average_score = sum(section_scores) / len(section_scores) if section_scores else 0
            recommendation = (
                f"Your career health score for {section} is high. Keep up the great work!"
                if average_score >= 8 else
                f"Your career health score for {section} is moderate. Consider improving in this area."
                if 5 <= average_score < 8 else
                f"Your career health score for {section} is low. Take action to improve this factor."
            )
            data.append([Paragraph(section, style_normal), f"{average_score:.1f}", Paragraph(recommendation, style_normal)])

        # Draw the table
        table = Table(data, colWidths=[150, 60, 300])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Adjust table position and draw
        table.wrapOn(can, left_margin, y_position - 50)
        table.drawOn(can, left_margin, y_position - 200)

        can.save()

        # Merge the content with the original page
        packet.seek(0)
        new_pdf = PdfReader(packet)
        page.merge_page(new_pdf.pages[0])

        # Add the updated page to the PDF writer
        pdf_writer.add_page(page)


        #blank_page = pdf_writer.add_blank_page()
        #add_dynamic_table(page, pdf_writer, sections, candidate_data)

        # Append the End_pdf
        with open('/content/drive/My Drive/Colab Notebooks/Base_PDF/End_pdf.pdf', 'rb') as end_pdf_file:
            end_pdf_reader = PdfReader(end_pdf_file)
            for end_page in end_pdf_reader.pages:
                pdf_writer.add_page(end_page)


        # Save the final report
        final_filename = f"/content/{candidate_name}_final_report.pdf"
        with open(final_filename, "wb") as out_file:
            pdf_writer.write(out_file)

        print(f"Generated PDF for {candidate_name}: {final_filename}")
    return final_filename

#csv_file_path = '/content/drive/My Drive/Colab Notebooks/CGA.csv'

# Load the CSV file into a Pandas DataFrame
#data = pd.read_csv(csv_file_path)

# Mapping of Target Work Domain to Base PDF Paths
domain_to_pdf_path = {
    'Analytics': '/content/drive/My Drive/Colab Notebooks/Base_PDF/Analytics.pdf',
    'Digital Marketing': '/content/drive/My Drive/Colab Notebooks/Base_PDF/Digital_Marketing.pdf',
    'Software and Tech': '/content/drive/My Drive/Colab Notebooks/Base_PDF/Soft&Tech.pdf',
    'Education and Training': '/content/drive/My Drive/Colab Notebooks/Base_PDF/Education&Training.pdf',
    'Management': '/content/drive/My Drive/Colab Notebooks/Base_PDF/Management.pdf',
    'Core Engineering': '/content/drive/My Drive/Colab Notebooks/Base_PDF/CoreEngg.pdf',
    'Operations': '/content/drive/My Drive/Colab Notebooks/Base_PDF/Operations.pdf',
    'Media and Communication': '/content/drive/My Drive/Colab Notebooks/Base_PDF/Media&Comm.pdf',
    'Animation and Graphics': '/content/drive/My Drive/Colab Notebooks/Base_PDF/Animation&Graphics.pdf',
    'Sales': '/content/drive/My Drive/Colab Notebooks/Base_PDF/Sales.pdf',
    'Leadership': '/content/drive/My Drive/Colab Notebooks/Base_PDF/Leadership.pdf',
    'Banking': '/content/drive/My Drive/Colab Notebooks/Base_PDF/Banking.pdf'

    # Add other domains and their corresponding PDF paths here
}

# Fetch base PDF paths for each candidate




# Load End PDF and process each candidate's report
#base_pdf_path = "/content/drive/My Drive/Colab Notebooks/base_pdf_pages.pdf"  # Store the path to the base PDF

# Button to generate PDFs
if st.button("Generate PDFs"):
        generated_pdfs = []

        for _, row in data.iterrows():
            base_pdf_path = domain_to_pdf_path.get(row['Target Work Domain'], None)
            if base_pdf_path:
                # Prepare candidate data dictionary
                candidate_data = {
                    "Name": row["Name"],
                    "Current Domain": row["Current Domain"],
                    "Current CTC(LPA)": row["Current CTC(LPA)"],
                    "Nature of Role": row["Nature of Role"],
                    "Level": row["Level"]
                }
                # Generate the final PDF
                final_pdf = generate_final_report(candidate_data, base_pdf_path)
                generated_pdfs.append((row["Name"], final_pdf))
            else:
                st.warning(f"Domain '{row['Target Work Domain']}' not found. Skipping candidate: {row['Name']}")

        # Combine generated PDFs into a downloadable ZIP file
        if generated_pdfs:
            from zipfile import ZipFile

            zip_buffer = BytesIO()
            with ZipFile(zip_buffer, 'w') as zip_file:
                for name, pdf in generated_pdfs:
                    zip_file.writestr(f"{name}.pdf", pdf.getvalue())
            zip_buffer.seek(0)

            # Provide the ZIP file for download
            st.download_button(
                label="Download All PDFs as ZIP",
                data=zip_buffer.getvalue(),
                file_name="candidate_reports.zip",
                mime="application/zip",
            )
        else:
            st.info("No reports were generated. Please check your CSV and domain mapping.")

        
