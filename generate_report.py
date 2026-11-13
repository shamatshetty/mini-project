import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

TEMPLATE_PATH = r"C:/Users/ASUS/.gemini/antigravity/brain/67939757-124b-4dee-9122-0cf9a8f5927d/.user_uploaded/media_1794596017373_67a86bce.docx"
OUTPUT_DOCX = r"c:/Users/ASUS/Documents/ds project/Hostel_Room_Allocation_System_Report.docx"
OUTPUT_FALLBACK_DOCX = r"c:/Users/ASUS/Documents/ds project/Data_Structures_Mini_Project_Report_Filled.docx"
OUTPUT_ARTIFACT_DOCX = r"C:/Users/ASUS/.gemini/antigravity/brain/67939757-124b-4dee-9122-0cf9a8f5927d/Hostel_Room_Allocation_System_Report.docx"
OUTPUT_MD = r"c:/Users/ASUS/Documents/ds project/REPORT.md"

STUDENTS = [
    ("1", "Shamat Ganapati Shetty", "NB25ISE205"),
    ("2", "Sanjit Sholapurkar", "NB25ISE200"),
    ("3", "Nishchal Vishwanath", "NB25ISE160"),
    ("4", "Praveen Patil", "NB25ISE174")
]

FONT_FAMILY = "Times New Roman"

def set_font_run(run, font_name=FONT_FAMILY, size_pt=12, bold=False, italic=False, color_rgb=None):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color_rgb:
        run.font.color.rgb = color_rgb
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def format_table(table, col_widths, header_bg="E2E8F0"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for row_idx, row in enumerate(table.rows):
        for col_idx, cell in enumerate(row.cells):
            cell.width = col_widths[col_idx]
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            if row_idx == 0:
                set_cell_background(cell, header_bg)
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.line_spacing = 1.0
                    for r in p.runs:
                        set_font_run(r, FONT_FAMILY, 10.5, bold=True)
            else:
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.line_spacing = 1.0
                    for r in p.runs:
                        set_font_run(r, FONT_FAMILY, 10, bold=r.bold, italic=r.italic, color_rgb=r.font.color.rgb if r.font.color else None)

def add_body_paragraph(after_element, text, bold_prefix="", space_before=0, space_after=6, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size_pt=12):
    new_p = docx.oxml.OxmlElement('w:p')
    after_element.addnext(new_p)
    p = docx.text.paragraph.Paragraph(new_p, after_element.getparent())
    p.paragraph_format.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        set_font_run(r_pre, FONT_FAMILY, size_pt, bold=True)
    if text:
        r_text = p.add_run(text)
        set_font_run(r_text, FONT_FAMILY, size_pt, bold=False)
    return new_p

def add_code_block(after_element, code_text, space_before=4, space_after=6):
    new_p = docx.oxml.OxmlElement('w:p')
    after_element.addnext(new_p)
    p = docx.text.paragraph.Paragraph(new_p, after_element.getparent())
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(code_text)
    set_font_run(r, FONT_FAMILY, 9.5, bold=False, color_rgb=RGBColor(0x0F, 0x17, 0x2A))
    return new_p

def main():
    doc = docx.Document(TEMPLATE_PATH)
    doc.styles['Normal'].font.name = FONT_FAMILY
    doc.styles['Normal'].font.size = Pt(12)

    # Save direct references to original 5 tables before any new tables are added
    t_cover = doc.tables[0]
    t_cert = doc.tables[1]
    t_ds = doc.tables[2]
    t_tests = doc.tables[3]
    t_complexity = doc.tables[4]

    # -------------------------------------------------------------
    # 1. COVER PAGE FORMATTING & ALIGNMENT
    # -------------------------------------------------------------
    cover_updates = {
        0: ("NITTE MEENAKSHI INSTITUTE OF TECHNOLOGY", 16, True, WD_ALIGN_PARAGRAPH.CENTER, 0, 2),
        1: ("Nitte (Deemed to be University)", 12, False, WD_ALIGN_PARAGRAPH.CENTER, 0, 18),
        3: ("MINI PROJECT REPORT", 14, True, WD_ALIGN_PARAGRAPH.CENTER, 0, 2),
        4: ("ON", 12, False, WD_ALIGN_PARAGRAPH.CENTER, 0, 6),
        5: ("SMART HOSTEL ROOM ALLOCATION AND FIFO WAITING LIST MANAGEMENT SYSTEM", 15, True, WD_ALIGN_PARAGRAPH.CENTER, 0, 18),
        8: ("Submitted in partial fulfillment of the requirements for the course", 11, False, WD_ALIGN_PARAGRAPH.CENTER, 0, 2),
        9: ("DATA STRUCTURES (25CSE201)", 13, True, WD_ALIGN_PARAGRAPH.CENTER, 0, 2),
        10: ("Semester 3 Section A", 11, False, WD_ALIGN_PARAGRAPH.CENTER, 0, 14),
        12: ("Submitted by:", 12, True, WD_ALIGN_PARAGRAPH.CENTER, 0, 6),
    }

    for idx, (txt, sz, bld, aln, sp_b, sp_a) in cover_updates.items():
        if idx < len(doc.paragraphs):
            p = doc.paragraphs[idx]
            p.text = txt
            p.paragraph_format.alignment = aln
            p.paragraph_format.space_before = Pt(sp_b)
            p.paragraph_format.space_after = Pt(sp_a)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, sz, bold=bld)

    # Institution block at bottom of Cover Page
    for p in doc.paragraphs:
        if "Academic Year: [2026" in p.text or "Academic Year: [20262027]" in p.text or "Department of Information Science" in p.text:
            p.text = "Department of Information Science and Engineering\nNITTE MEENAKSHI INSTITUTE OF TECHNOLOGY\nAcademic Year: 2026–2027"
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 11.5, bold=True)

    # Table 0: Student Members on Cover Page
    t0 = t_cover
    t0_widths = [Inches(0.9), Inches(3.6), Inches(1.8)]
    for row_idx, s in enumerate(STUDENTS, start=1):
        row = t0.rows[row_idx]
        row.cells[0].text = s[0]
        row.cells[1].text = s[1]
        row.cells[2].text = s[2]
        for c_idx, c in enumerate(row.cells):
            for p in c.paragraphs:
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in (0, 2) else WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    set_font_run(r, FONT_FAMILY, 10.5, bold=False)
    # Header cells of Table 0
    t0.rows[0].cells[0].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t0.rows[0].cells[1].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    t0.rows[0].cells[2].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_table(t0, t0_widths)

    # -------------------------------------------------------------
    # 2. CERTIFICATE PAGE
    # -------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip() == "CERTIFICATE":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(12)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
        elif "This is to certify that the mini project entitled" in p.text:
            p.text = (
                "This is to certify that the mini project entitled \"Smart Hostel Room Allocation "
                "and FIFO Waiting List Management System\" has been completed by the students listed "
                "in this report, in partial fulfillment of the requirements for the Data Structures "
                "(25CSE201) course under the guidance of Dr. Deepthi K during the academic year 2026–2027."
            )
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.line_spacing = 1.25
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 12, bold=False)
        elif "Course Instructor: ______________________________" in p.text:
            p.text = "Course Instructor: Dr. Deepthi K, Assistant Professor, Dept. of ISE"
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 11, bold=True)
        elif "Head of the Department: _________________________" in p.text:
            p.text = "Head of the Department: Dr. Prasad N. H., Professor & Head, Dept. of ISE"
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(14)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 11, bold=True)
        elif "Signature of Course Instructor: ________________" in p.text:
            p.text = "Signature of Course Instructor: ______________________________"
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(4)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 11, bold=False)
        elif "Date: ____________________" in p.text:
            p.text = "Date: ____________________"
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 11, bold=False)

    # Table 1: Student Members on Certificate Page
    t1 = t_cert
    for row_idx, s in enumerate(STUDENTS, start=1):
        row = t1.rows[row_idx]
        row.cells[0].text = s[0]
        row.cells[1].text = s[1]
        row.cells[2].text = s[2]
        for c_idx, c in enumerate(row.cells):
            for p in c.paragraphs:
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in (0, 2) else WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    set_font_run(r, FONT_FAMILY, 10.5, bold=False)
    t1.rows[0].cells[0].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t1.rows[0].cells[1].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    t1.rows[0].cells[2].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_table(t1, t0_widths)

    # -------------------------------------------------------------
    # 3. ACKNOWLEDGEMENT PAGE
    # -------------------------------------------------------------
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == "ACKNOWLEDGEMENT":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(14)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
            
            # Set body text in next paragraph
            p_ack_body = doc.paragraphs[i + 1]
            p_ack_body.text = (
                "We would like to express our deepest gratitude to our respected Course Instructor, "
                "Dr. Deepthi K, Assistant Professor, Department of Information Science and Engineering, "
                "Nitte Meenakshi Institute of Technology, for her invaluable guidance, inspiring suggestions, "
                "and constructive critiques throughout the conceptualization, system modeling, and implementation "
                "of this mini-project.\n\n"
                "We express our sincere thanks to Dr. Prasad N. H., Professor and Head, Department of Information "
                "Science and Engineering, for providing excellent departmental infrastructure and state-of-the-art "
                "laboratory facilities that enabled us to write, compile, benchmark, and verify our software solutions.\n\n"
                "We also convey our sincere appreciation to our esteemed Principal and the Management of Nitte "
                "Meenakshi Institute of Technology (Nitte Deemed to be University) for fostering an atmosphere of "
                "academic inquiry, technical rigor, and hands-on engineering practice.\n\n"
                "Finally, we extend our heartfelt gratitude to our parents, laboratory staff, and peer classmates "
                "for their constant encouragement, insightful discussions, and technical camaraderie during the "
                "development and testing of this project."
            )
            p_ack_body.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_ack_body.paragraph_format.space_before = Pt(6)
            p_ack_body.paragraph_format.space_after = Pt(12)
            p_ack_body.paragraph_format.line_spacing = 1.25
            for r in p_ack_body.runs:
                set_font_run(r, FONT_FAMILY, 12, bold=False)
            p_ack_body.add_run().add_break(WD_BREAK.PAGE)
            break

    # -------------------------------------------------------------
    # 4. ABSTRACT PAGE
    # -------------------------------------------------------------
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == "ABSTRACT":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(14)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
            
            p_abs_body = doc.paragraphs[i + 1]
            p_abs_body.text = (
                "Hostel accommodation allocation in educational institutions is a classic resource-allocation "
                "problem marked by severe demand spikes during admission cycles and dynamic bed vacancies. Traditional "
                "manual ledgers and unorganized queues frequently suffer from human bias, lack of transparency, double "
                "bookings, and severe waitlist starvation. Naive software implementations using linear array queues "
                "further suffer from the structural flaw of queue drift, where vacant memory slots at the front cannot "
                "be reclaimed without prohibitively expensive O(N) memory element shifting.\n\n"
                "This project presents the Smart Hostel Room Allocation and FIFO Waiting List Management System, "
                "an academic, robust software solution engineered strictly in standard C (ISO C11 specification) "
                "leveraging fundamental linear data structures: Contiguous 1D Arrays and an Array-based Circular FIFO "
                "Queue (Ring Buffer). Contiguous 1D arrays of custom composite structures are deployed to maintain "
                "fixed student academic profiles (Student struct) and multi-bed hostel room allotments (Room struct, "
                "with a fixed constraint of maximum 4 beds per room). An Array-based Circular FIFO Waiting Queue is "
                "engineered with modular pointer arithmetic ((rear + 1) % MAX and (front + 1) % MAX), ensuring "
                "strictly O(1) enqueue and dequeue operations while perpetually recycling reclaimed array cells "
                "without memory shifting or queue drift.\n\n"
                "The system guarantees strict FIFO fairness: new accommodation requests are never permitted to bypass "
                "waiting applicants, and whenever a bed is vacated or a new room is constructed, the bed is automatically "
                "and atomically allocated to the front-most waiting student in O(1) time without human intervention. "
                "The project includes comprehensive input validations (unique ID/USN enforcement, capacity boundary "
                "checks, queue underflow/overflow guards) and an automated test harness with 63 passing unit and "
                "integration test cases confirming mathematical FIFO fairness and circular wrap-around integrity."
            )
            p_abs_body.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_abs_body.paragraph_format.space_before = Pt(6)
            p_abs_body.paragraph_format.space_after = Pt(12)
            p_abs_body.paragraph_format.line_spacing = 1.25
            for r in p_abs_body.runs:
                set_font_run(r, FONT_FAMILY, 12, bold=False)
            p_abs_body.add_run().add_break(WD_BREAK.PAGE)
            break

    # -------------------------------------------------------------
    # 5. TABLE OF CONTENTS: PROFESSIONAL ALIGNED TABLE
    # -------------------------------------------------------------
    toc_p = None
    for p in doc.paragraphs:
        if p.text.strip() == "TABLE OF CONTENTS":
            toc_p = p
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(14)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
            break

    # Delete the old crude spaced paragraphs (P59 to P72)
    to_delete = []
    found_toc = False
    for p in doc.paragraphs:
        if p.text.strip() == "TABLE OF CONTENTS":
            found_toc = True
            continue
        if found_toc:
            if "CHAPTER 1: INTRODUCTION" in p.text:
                break
            to_delete.append(p)

    for p in to_delete:
        p._p.getparent().remove(p._p)

    # Insert a real, perfectly aligned 3-column table for Table of Contents
    toc_entries = [
        ("1.", "Introduction", "1"),
        ("2.", "Problem Statement", "2"),
        ("3.", "Objectives", "3"),
        ("4.", "Data Structures Used", "4"),
        ("5.", "System Design and Methodology", "6"),
        ("6.", "Algorithm and Pseudocode", "9"),
        ("7.", "Implementation", "13"),
        ("8.", "Results and Output", "18"),
        ("9.", "Time and Space Complexity", "23"),
        ("10.", "Applications", "25"),
        ("11.", "Limitations and Future Enhancements", "26"),
        ("12.", "Conclusion", "27"),
        ("13.", "References", "28")
    ]

    toc_table = doc.add_table(rows=len(toc_entries) + 1, cols=3)
    toc_p._p.addnext(toc_table._tbl)
    toc_widths = [Inches(0.9), Inches(4.5), Inches(1.0)]

    # Header
    toc_table.rows[0].cells[0].text = "Sl. No."
    toc_table.rows[0].cells[1].text = "Topic"
    toc_table.rows[0].cells[2].text = "Page No."
    toc_table.rows[0].cells[0].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    toc_table.rows[0].cells[1].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    toc_table.rows[0].cells[2].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    for row_idx, (sl, topic, pg) in enumerate(toc_entries, start=1):
        row = toc_table.rows[row_idx]
        row.cells[0].text = sl
        row.cells[1].text = topic
        row.cells[2].text = pg
        row.cells[0].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[1].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        row.cells[2].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    format_table(toc_table, toc_widths)

    # Add a page break after TOC table
    p_after_toc = docx.oxml.OxmlElement('w:p')
    toc_table._tbl.addnext(p_after_toc)
    p_br_toc = docx.text.paragraph.Paragraph(p_after_toc, doc)
    p_br_toc.add_run().add_break(WD_BREAK.PAGE)

    # -------------------------------------------------------------
    # 6. CHAPTER 1: INTRODUCTION
    # -------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip() == "CHAPTER 1: INTRODUCTION":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
        elif "[Introduce the problem, its background, relevance, and how data structures help solve it.]" in p.text or "Educational institutions accommodate hundreds or thousands" in p.text:
            p.text = (
                "Educational institutions accommodate hundreds or thousands of outstation students each academic "
                "year. Residential hostel accommodation is an indispensable prerequisite for student welfare and "
                "academic performance. However, hostel infrastructure is physically constrained by finite room and "
                "bed capacity. When demand for rooms outstrips institutional capacity during peak admission cycles, "
                "hostel wardens face the difficult logistical challenge of managing overflow candidates transparently "
                "and impartially.\n\n"
                "In traditional manual or ad-hoc hostel management systems, allocation records are maintained in physical "
                "registers or unstructured flat spreadsheets. This introduces several critical operational vulnerabilities: "
                "unintentional double allocation of the same bed to multiple candidates, delayed bed re-allocation when an "
                "occupant vacates, human favoritism or arbitrary bypassing of waiting candidates, and clerical record inconsistencies. "
                "Furthermore, naive software implementations utilizing linear arrays for waiting queues suffer from 'queue drift' "
                "or false overflow—where newly vacated queue slots at the front cannot be reused because the rear pointer has reached "
                "the end of the array, requiring costly O(N) memory shifting of all waiting records.\n\n"
                "Fundamental Data Structures provide the definitive mathematical and algorithmic remedy to these challenges:\n"
                "1. Contiguous Fixed-size Arrays allow instant O(1) indexed lookup, deterministic memory layout, and zero dynamic "
                "heap allocation vulnerabilities.\n"
                "2. Array-based Circular FIFO Queues (Ring Buffers) model the waiting list with strict temporal fairness "
                "(First-In, First-Out). By employing modular pointer arithmetic ((idx + 1) % MAX), vacated front slots are seamlessly "
                "reused without data movement, guaranteeing optimal O(1) enqueue and dequeue operations.\n\n"
                "This project demonstrates the rigorous application of Arrays and Circular FIFO Queues in the C11 programming "
                "language to engineer an automated, robust, and transparent Hostel Room Allocation and Waiting List Management System."
            )
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 12, bold=False)

    # -------------------------------------------------------------
    # 7. CHAPTER 2: PROBLEM STATEMENT
    # -------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip() == "CHAPTER 2: PROBLEM STATEMENT":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
        elif "[Clearly define the problem addressed by the project and explain the need for the proposed solution.]" in p.text or "Problem Definition:\nGiven a collegiate residential hostel" in p.text:
            p.text = (
                "Problem Definition:\n"
                "Given a collegiate residential hostel with R rooms, where each room supports a bounded capacity of 1 to 4 beds, "
                "and an incoming stream of N student accommodation applicants (where N may exceed total bed capacity M), design "
                "and implement a deterministic, memory-efficient, and starvation-free allocation system in C using fixed-size "
                "arrays and a circular FIFO queue.\n\n"
                "Operational Requirements & Constraints:\n"
                "1. Immediate Allocation: If vacant beds exist in the hostel, incoming applicants must be immediately allocated "
                "the first available room and bed.\n"
                "2. FIFO Waiting Queue Fairness: When all beds are 100% occupied, overflow applicants must be enqueued into an "
                "order-preserving waiting list. If any students are currently in the waiting queue, subsequent new applicants must "
                "strictly join the REAR of the queue; under no circumstance may a newly arrived student bypass waiting candidates.\n"
                "3. Instant Vacate & Handoff: When an allocated student vacates their bed, the system must immediately mark the bed "
                "vacant, check the waiting queue, and if non-empty, atomically dequeue the student at FRONT and allocate the freed bed "
                "to them in O(1) time without user intervention.\n"
                "4. Room Expansion Handoff: When new rooms are added to an already full hostel, its beds must be automatically "
                "distributed to waiting students in FIFO order until the queue is exhausted or room capacity is filled.\n"
                "5. Data Integrity & Validation: The system must enforce strict uniqueness on Student IDs and University Seat "
                "Numbers (USNs), disallow duplicate room additions, prevent out-of-bounds capacities (> 4 beds), and handle queue "
                "overflow and underflow gracefully without segmentation faults or data corruption."
            )
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 12, bold=False)

    # -------------------------------------------------------------
    # 8. CHAPTER 3: OBJECTIVES
    # -------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip() == "CHAPTER 3: OBJECTIVES":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
        elif "1. [Objective 1]" in p.text or "1. Design and implement contiguous fixed-size 1D arrays" in p.text:
            p.text = (
                "1. Design and implement contiguous fixed-size 1D arrays of C structures to represent student demographic "
                "profiles (Student) and multi-bed hostel room occupancy states (Room) with zero dynamic memory allocation.\n"
                "2. Implement an Array-based Circular FIFO Queue (Ring Buffer) with FRONT and REAR pointer tracking and modular "
                "arithmetic ((rear + 1) % MAX, (front + 1) % MAX) to eliminate queue drift and achieve O(1) time complexity.\n"
                "3. Develop an automated bed allocation engine that provides immediate assignment during bed availability and "
                "enforces strict FIFO queuing when all beds are occupied.\n"
                "4. Implement an automatic handoff mechanism during room vacating and room addition that pops the FRONT waiting student "
                "and immediately binds them to the newly available bed.\n"
                "5. Incorporate comprehensive validation routines to prevent duplicate Student IDs, duplicate USNs, double bed allotments, "
                "and invalid room capacities (> 4 beds per room).\n"
                "6. Construct an interactive 12-option console interface alongside an automated demonstration mode and a 63-test "
                "automated test suite validating FIFO fairness, circular wrap-around, and edge-case handling."
            )
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 12, bold=False)

    # -------------------------------------------------------------
    # 9. CHAPTER 4: DATA STRUCTURES USED & TABLE 2
    # -------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip() == "CHAPTER 4: DATA STRUCTURES USED":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
        elif "[Name each data structure and explain why it is suitable for the problem.]" in p.text or "The architecture of the Smart Hostel Room Allocation System is built entirely upon two foundational" in p.text:
            p.text = (
                "The architecture of the Smart Hostel Room Allocation System is built entirely upon two foundational "
                "data structures: Contiguous Fixed-size Arrays and an Array-based Circular FIFO Queue.\n\n"
                "1. Contiguous Fixed-Size Arrays (Student & Room Records):\n"
                "- Structure Definition: Two global static arrays are declared: Student students[MAX_STUDENTS] (capacity 100) "
                "and Room rooms[MAX_ROOMS] (capacity 50).\n"
                "- Suitability: Arrays guarantee contiguous physical memory placement, granting instantaneous O(1) random access "
                "via index arithmetic (e.g., students[idx]). Statically sizing the arrays at compile-time completely prevents runtime "
                "memory fragmentation, memory leaks, and pointer aliasing bugs that commonly afflict dynamic heap allocations.\n"
                "- Internal Representation: Each Room structure contains an internal fixed-size integer array bedStatus[4] (0 = Vacant, "
                "1 = Occupied) and bedOwner[4] (storing the corresponding student array index). This models the physical reality of a "
                "multi-bed room concisely.\n\n"
                "2. Array-based Circular FIFO Queue (Ring Buffer):\n"
                "- Structure Definition: The waiting queue is defined via a CircularQueue structure containing items[MAX_QUEUE] "
                "(capacity 50), front, rear, max, and count.\n"
                "- Overcoming Linear Queue Flaw: In a standard linear array queue, dequeuing elements causes front to advance towards the "
                "end of the array. Once rear reaches MAX_QUEUE - 1, no further elements can be enqueued, even if all front slots are completely "
                "vacant (false overflow). Resolving this via linear shifting requires O(N) operations per dequeue. The Circular Queue solves "
                "this mathematically by wrapping indices circularly: rear = (rear + 1) % MAX and front = (front + 1) % MAX. This enables infinite "
                "continuous reuse of memory cells with strict O(1) enqueue and dequeue performance."
            )
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 12, bold=False)

    t2 = t_ds
    t2_widths = [Inches(0.8), Inches(1.8), Inches(2.3), Inches(1.5)]
    t2_data = [
        ("1", "Fixed-size 1D Array of Structs (Student)", "Stores contiguous student demographic profiles, USNs, and room allotment status.", "student_register(), student_find_by_id(), student_find_by_usn(), student_display_all()"),
        ("2", "Fixed-size 1D Array of Structs (Room)", "Manages room capacity (max 4 beds/room) and tracks per-bed status and student indices.", "room_add(), room_find_first_vacant(), room_allocate_bed(), room_vacate_by_student()"),
        ("3", "Circular FIFO Queue (Ring Buffer Array)", "Maintains order-preserving waitlist for overflow applicants with zero queue drift and O(1) ops.", "cq_enqueue(), cq_dequeue(), cq_peek(), cq_is_empty(), cq_is_full(), cq_display()")
    ]
    t2.rows[0].cells[0].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t2.rows[0].cells[1].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    t2.rows[0].cells[2].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    t2.rows[0].cells[3].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for row_idx, d in enumerate(t2_data, start=1):
        row = t2.rows[row_idx]
        for col_idx in range(4):
            row.cells[col_idx].text = d[col_idx]
            for p in row.cells[col_idx].paragraphs:
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    set_font_run(r, FONT_FAMILY, 10, bold=(col_idx == 1))
    format_table(t2, t2_widths)

    # -------------------------------------------------------------
    # 10. CHAPTER 5: SYSTEM DESIGN AND METHODOLOGY
    # -------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip() == "CHAPTER 5: SYSTEM DESIGN AND METHODOLOGY":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
        elif "[Describe the system architecture, modules, inputs, outputs, and workflow. Insert a block diagram or flowchart.]" in p.text or "System Architecture & Modularity:\nThe project is engineered" in p.text:
            p.text = (
                "System Architecture & Modularity:\n"
                "The project is engineered following clean software modularity principles in C11. The codebase is divided into "
                "three distinct service modules and a central coordination controller:\n"
                "1. Student Module (student.h, student.c): Responsible for registering student records, maintaining the students[] "
                "array, performing linear search scans for unique Student IDs and USNs, and updating allocation states.\n"
                "2. Room Module (room.h, room.c): Encapsulates room creation, bed status management (up to 4 beds per room), first-vacant "
                "bed search scans, and bed vacancy de-allocation.\n"
                "3. Circular Queue Module (queue.h, queue.c): Implements pure ring buffer operations (enqueue, dequeue, peek, wrap-around "
                "detection, and array slot visualization) using student array indices.\n"
                "4. Controller Engine (main.c): Orchestrates application workflow, coordinates room availability with waiting queue status, "
                "enforces FIFO non-bypassing fairness, and executes automated demonstration suites.\n\n"
                "System Workflows:\n"
                "A. Accommodation Request Workflow:\n"
                "   [Student Requests Bed] -> [Check if Waiting Queue is Non-Empty]\n"
                "   |-- If Queue NOT Empty: Enqueue student at REAR (Strict FIFO: no bypassing existing waiting students).\n"
                "   |-- If Queue IS Empty: Scan Room Array for First Vacant Bed.\n"
                "       |-- Vacant Bed Found: Allocate immediately -> Set Status ALLOCATED.\n"
                "       |-- No Bed Found (100% Full): Enqueue student at REAR -> Set Status WAITING.\n\n"
                "B. Bed Vacating Workflow:\n"
                "   [Student Vacates Bed] -> [Locate Bed in Room Array] -> [Mark Bed Status VACANT]\n"
                "   -> [Check Waiting Queue]\n"
                "   |-- If Queue Empty: Bed remains vacant for future requests.\n"
                "   |-- If Queue NOT Empty: DEQUEUE student at FRONT -> Automatically allocate the freed bed -> Set Status ALLOCATED.\n\n"
                "C. Room Addition Workflow:\n"
                "   [Admin Adds New Room] -> [Validate Capacity 1..4] -> [Check Waiting Queue]\n"
                "   -> While beds remain available in new room AND Waiting Queue is not empty:\n"
                "      DEQUEUE student at FRONT -> Assign bed -> Update records."
            )
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 11.5, bold=False)

    # -------------------------------------------------------------
    # 11. CHAPTER 6: ALGORITHM AND PSEUDOCODE
    # -------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip() == "CHAPTER 6: ALGORITHM AND PSEUDOCODE":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
        elif "Algorithm 1: [Name of operation]" in p.text or "Algorithm 1: Student Registration (student_register)" in p.text:
            p.text = (
                "Algorithm 1: Student Registration (student_register)\n"
                "Input: Student ID (id), Name (name), USN (usn), Department (dept), Academic Year (year)\n"
                "Output: Index of newly registered student on success, or negative error code on failure\n"
                "Steps:\n"
                "1. If student_count >= MAX_STUDENTS, Return -1 (Array Overflow).\n"
                "2. For i = 0 to student_count - 1:\n"
                "   a. If students[i].id == id, Return -2 (Duplicate ID Error).\n"
                "   b. If students[i].usn == usn, Return -3 (Duplicate USN Error).\n"
                "3. Set idx = student_count.\n"
                "4. Copy id, name, usn, dept, year into students[idx].\n"
                "5. Set students[idx].roomNumber = -1, bedNumber = -1, status = STATUS_UNALLOCATED.\n"
                "6. Increment student_count by 1.\n"
                "7. Return idx.\n\n"
                "Algorithm 2: Circular Queue Enqueue (cq_enqueue)\n"
                "Input: CircularQueue pointer (Q), Student array index (studentIdx)\n"
                "Output: 1 on success, 0 on Queue Overflow\n"
                "Steps:\n"
                "1. If Q.count == Q.max, Return 0 (Queue Full).\n"
                "2. If Q.front == -1 (Queue was empty):\n"
                "   Set Q.front = 0, Q.rear = 0.\n"
                "3. Else:\n"
                "   Set Q.rear = (Q.rear + 1) % Q.max.\n"
                "4. Set Q.items[Q.rear] = studentIdx.\n"
                "5. Increment Q.count by 1.\n"
                "6. Return 1.\n\n"
                "Algorithm 3: Circular Queue Dequeue (cq_dequeue)\n"
                "Input: CircularQueue pointer (Q)\n"
                "Output: Dequeued student array index, or -1 on Queue Underflow\n"
                "Steps:\n"
                "1. If Q.count == 0, Return -1 (Queue Empty).\n"
                "2. Set dequeuedIdx = Q.items[Q.front].\n"
                "3. If Q.front == Q.rear (Last remaining element removed):\n"
                "   Set Q.front = -1, Q.rear = -1.\n"
                "4. Else:\n"
                "   Set Q.front = (Q.front + 1) % Q.max.\n"
                "5. Decrement Q.count by 1.\n"
                "6. Return dequeuedIdx.\n\n"
                "Algorithm 4: Request Accommodation & Fair FIFO Allocation\n"
                "Input: Student index (studentIdx)\n"
                "Output: None (Updates student and room array states)\n"
                "Steps:\n"
                "1. If students[studentIdx].status == STATUS_ALLOCATED, Print error and Return.\n"
                "2. If cq_get_count(waitingQueue) > 0 (Waiting queue is non-empty):\n"
                "   a. Call cq_enqueue(waitingQueue, studentIdx).\n"
                "   b. Set students[studentIdx].status = STATUS_WAITING.\n"
                "   c. Print: Enqueued at REAR to preserve FIFO fairness. Return.\n"
                "3. Call room_find_first_vacant(&roomIdx, &bedIdx).\n"
                "4. If vacant bed found:\n"
                "   a. Call room_allocate_bed(roomIdx, bedIdx, studentIdx).\n"
                "   b. Update students[studentIdx].roomNumber and bedNumber.\n"
                "   c. Set students[studentIdx].status = STATUS_ALLOCATED.\n"
                "5. Else (All beds full):\n"
                "   a. Call cq_enqueue(waitingQueue, studentIdx).\n"
                "   b. Set students[studentIdx].status = STATUS_WAITING.\n\n"
                "Algorithm 5: Vacate Room & Automatic FIFO Handoff\n"
                "Input: Student index (studentIdx)\n"
                "Output: None (Frees bed and triggers automatic waitlist dequeue)\n"
                "Steps:\n"
                "1. If students[studentIdx].status != STATUS_ALLOCATED, Print error and Return.\n"
                "2. Call room_vacate_by_student(studentIdx, &roomNo, &bedNo).\n"
                "3. Set students[studentIdx].status = STATUS_VACATED, roomNumber = -1, bedNumber = -1.\n"
                "4. If cq_is_empty(waitingQueue) == 0:\n"
                "   a. Set nextStudentIdx = cq_dequeue(waitingQueue).\n"
                "   b. Find index of roomNo in room array (roomIdx).\n"
                "   c. Call room_allocate_bed(roomIdx, bedNo - 1, nextStudentIdx).\n"
                "   d. Update students[nextStudentIdx].roomNumber = roomNo, bedNumber = bedNo.\n"
                "   e. Set students[nextStudentIdx].status = STATUS_ALLOCATED.\n"
                "   f. Print: Freed bed automatically allocated to FIFO FRONT student."
            )
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 11, bold=False)

    # -------------------------------------------------------------
    # 12. CHAPTER 7: IMPLEMENTATION
    # -------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip() == "CHAPTER 7: IMPLEMENTATION":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
        elif "[Describe the implementation in C. Explain important functions. Paste the complete, commented C source code here or include it in an appendix.]" in p.text or "Technical Environment & Standards:\n- Language & Compiler: Standard C" in p.text:
            p.text = (
                "Technical Environment & Standards:\n"
                "- Language & Compiler: Standard C (ISO/IEC 9899:2011 C11 Standard) compiled using GCC 14.2.0 with flags -Wall -Wextra -std=c11.\n"
                "- Platform: Windows 11 console environment.\n"
                "- Memory Management: Strictly static buffer allocation; zero dynamic heap allocations (no malloc, calloc, or free), guaranteeing "
                "deterministic predictability, immune to heap exhaustion or pointer leaks.\n\n"
                "Key Structures & Function Specifications:\n\n"
                "1. Student Structure (student.h):\n"
                "typedef struct {\n"
                "    char id[16];\n"
                "    char name[64];\n"
                "    char usn[20];\n"
                "    char department[32];\n"
                "    int year;\n"
                "    int roomNumber;\n"
                "    int bedNumber;\n"
                "    AllocationStatus status; // UNALLOCATED, WAITING, ALLOCATED, VACATED\n"
                "} Student;\n\n"
                "2. Room Structure (room.h):\n"
                "typedef struct {\n"
                "    int roomNumber;\n"
                "    int capacity;                     // 1 to 4 beds\n"
                "    int occupiedCount;\n"
                "    int bedStatus[4];                 // 0 = Vacant, 1 = Occupied\n"
                "    int bedOwner[4];                  // Index into students[] array\n"
                "} Room;\n\n"
                "3. Circular Queue Structure (queue.h):\n"
                "typedef struct {\n"
                "    int items[50];                    // Student array indices\n"
                "    int front;                        // Index of front element (-1 if empty)\n"
                "    int rear;                         // Index of rear element (-1 if empty)\n"
                "    int max;                          // Maximum capacity (50)\n"
                "    int count;                        // Active waiting student count\n"
                "} CircularQueue;\n\n"
                "Core Function Implementation Highlights:\n"
                "- cq_enqueue(CircularQueue *q, int studentIdx): Computes q->rear = (q->rear + 1) % q->max. Detects wrap-around if rear < front.\n"
                "- cq_dequeue(CircularQueue *q): Retrieves q->items[q->front] and advances q->front = (q->front + 1) % q->max. Resets both to -1 when count reaches 0.\n"
                "- room_find_first_vacant(int *outRoomIdx, int *outBedIdx): Iterates through rooms and checks bedStatus[b] == 0, guaranteeing deterministic bed filling.\n"
                "- room_vacate_by_student(int studentIdx, ...): Clears bedStatus and triggers immediate FIFO dequeue handoff."
            )
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 11, bold=False)

    # -------------------------------------------------------------
    # 13. CHAPTER 8: RESULTS AND OUTPUT & TABLE 3
    # -------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip() == "CHAPTER 8: RESULTS AND OUTPUT":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
        elif "[Include screenshots or console output and explain the results.]" in p.text or "The system was rigorously verified through an automated unit" in p.text:
            p.text = (
                "The system was rigorously verified through an automated unit and integration test harness (tests/test_fifo.c) "
                "as well as manual console verification and dedicated automated demonstration modes (--demo and --wrap-demo). "
                "All 63 automated tests passed with zero failures (100% success rate)."
            )
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(10)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 12, bold=False)

    t3 = t_tests
    t3_widths = [Inches(1.2), Inches(1.4), Inches(1.5), Inches(1.5), Inches(0.8)]
    while len(t3.rows) < 8:
        t3.add_row()

    t3_data = [
        ("TC01: Registration", "STU001, Alice Smith, 1MS23CS001, CSE, 2", "Record saved at index 0; count = 1", "Registered at index 0; count = 1", "PASS"),
        ("TC02: Duplicate USN", "STU002, Bob, 1MS23CS001 (Duplicate)", "Reject registration with error code -3", "Rejected: Duplicate USN detected", "PASS"),
        ("TC03: Bed Allocation", "Hostel has vacant beds; STU001 requests", "Assigned Room 101 Bed 1; ALLOCATED", "Assigned Room 101 Bed 1; ALLOCATED", "PASS"),
        ("TC04: Queue Enqueue", "All beds full; STU005 requests bed", "Enqueued at items[0]; FRONT=0, REAR=0", "Enqueued; FRONT=0, REAR=0; WAITING", "PASS"),
        ("TC05: Vacate & Handoff", "Bed 101-1 vacated; STU005 at FRONT", "Bed freed; STU005 dequeued & allocated", "STU005 auto-allocated Bed 101-1", "PASS"),
        ("TC06: Queue Wrap-Around", "MAX=6; Enqueue 6, Dequeue 3, Enqueue 2", "REAR wraps (5+1)%6=0; REAR < FRONT", "REAR wrapped to index 1; FRONT = 3", "PASS"),
        ("TC07: Room Addition Auto-Alloc", "2 students waiting; Room 201 (cap 2) added", "Auto-allocate 2 beds; Queue empty", "2 students dequeued & allocated; Queue count 0", "PASS")
    ]
    t3.rows[0].cells[0].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t3.rows[0].cells[1].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    t3.rows[0].cells[2].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    t3.rows[0].cells[3].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    t3.rows[0].cells[4].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for row_idx, d in enumerate(t3_data, start=1):
        row = t3.rows[row_idx]
        for col_idx in range(5):
            row.cells[col_idx].text = d[col_idx]
            for p in row.cells[col_idx].paragraphs:
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in (0, 4) else WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    set_font_run(r, FONT_FAMILY, 9.5, bold=(col_idx in (0, 4)), color_rgb=RGBColor(0x16, 0x65, 0x34) if col_idx == 4 else None)
    format_table(t3, t3_widths)

    for p in doc.paragraphs:
        if "[Insert program screenshots / sample output below.]" in p.text or "Console Output of Automated FIFO Demonstration" in p.text:
            p.text = (
                "Console Output of Automated FIFO Demonstration (hostel.exe --demo):\n\n"
                "[STEP 1] Configuring Hostel with 2 Rooms (2 beds each = 4 beds total)...\n"
                "Room 101: [B1: VAC] [B2: VAC] | Room 102: [B1: VAC] [B2: VAC]\n"
                "Total Rooms: 2 | Total Beds: 4 | Occupied: 0 | Available: 4\n\n"
                "[STEP 2] Registering 4 students and requesting accommodation...\n"
                " -> Allocated 'Alice Smith' to Room 101, Bed 1\n"
                " -> Allocated 'Bob Johnson' to Room 101, Bed 2\n"
                " -> Allocated 'Charlie Ray' to Room 102, Bed 1\n"
                " -> Allocated 'Diana Prince' to Room 102, Bed 2\n"
                "Hostel Bed Status: Occupied: 4 | Available: 0 (100% FULL)\n\n"
                "[STEP 3] Registering 3 additional students when hostel is 100% FULL...\n"
                "[ENQUEUE] 'Evan Wright' (STU005) -> FRONT = 0 | REAR = 0 | items[0]\n"
                "[ENQUEUE] 'Fiona Gallagher' (STU006) -> FRONT = 0 | REAR = 1 | items[1]\n"
                "[ENQUEUE] 'George Clark' (STU007) -> FRONT = 0 | REAR = 2 | items[2]\n"
                "Queue Pointers -> FRONT: 0 | REAR: 2 | Total Waiting: 3\n\n"
                "[STEP 5] Alice Smith (STU001) vacates Room 101, Bed 1...\n"
                "[VACATE SUCCESS] Room 101, Bed 1 is freed. Student 'Alice Smith' status set to VACATED.\n"
                "Triggering FIFO Dequeue for the newly freed bed...\n"
                "[DEQUEUE] Dequeued Student 'Evan Wright' (STU005) from items[0]\n"
                "Updated Pointers: FRONT = 1 | REAR = 2 | Queue Total Size: 2 / 50\n"
                ">>> RESULT: Bed 101-1 automatically allocated to FIFO FRONT student: 'Evan Wright' (STU005)!\n\n"
                "Test Suite Summary:\n"
                "===============================================================\n"
                "TEST RESULTS: 63 / 63 TESTS PASSED (100% SUCCESS RATE)\n"
                "==============================================================="
            )
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.left_indent = Inches(0.25)
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.line_spacing = 1.05
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 9.5, bold=False)

    # -------------------------------------------------------------
    # 14. CHAPTER 9: TIME AND SPACE COMPLEXITY & TABLE 4
    # -------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip() == "CHAPTER 9: TIME AND SPACE COMPLEXITY":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
        elif "[Analyze the time and space complexity of implemented operations. Specify best, average, and worst cases where applicable.]" in p.text or "Complexity Analysis:\nThe system achieves optimal" in p.text:
            p.text = (
                "Complexity Analysis:\n"
                "The system achieves optimal computational efficiency by leveraging circular pointer arithmetic and flat contiguous arrays. "
                "Unlike a linear array queue that suffers from O(N) data relocation on each dequeue, the circular queue executes in "
                "strict O(1) constant time for both enqueue and dequeue."
            )
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(10)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 12, bold=False)

    t4 = t_complexity
    t4_widths = [Inches(1.4), Inches(1.2), Inches(1.0), Inches(2.8)]
    while len(t4.rows) < 6:
        t4.add_row()

    t4_data = [
        ("Circular Enqueue (cq_enqueue)", "Best: O(1)\nAvg: O(1)\nWorst: O(1)", "O(1) Aux", "rear = (rear + 1) % MAX. Direct assignment into items[rear]; no element shifting."),
        ("Circular Dequeue (cq_dequeue)", "Best: O(1)\nAvg: O(1)\nWorst: O(1)", "O(1) Aux", "front = (front + 1) % MAX. Immediate index retrieval from items[front]; no array shifting."),
        ("Student Registration", "Best: O(1)\nAvg: O(N)\nWorst: O(N)", "O(1) Aux", "Linear scan across N existing students to verify unique Student ID and USN before insertion."),
        ("Find First Vacant Bed", "Best: O(1)\nAvg: O(R*B)\nWorst: O(R*B)", "O(1) Aux", "Iterates across R rooms (R <= 50) and examines B beds (B <= 4). Bounded constant time in practice."),
        ("Vacate Bed & Auto-Allocate", "Best: O(R*B) + O(1)\nWorst: O(R*B) + O(1)", "O(1) Aux", "Locates bed via ownership scan O(R*B) and performs strict O(1) dequeue and bed allotment.")
    ]
    t4.rows[0].cells[0].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    t4.rows[0].cells[1].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t4.rows[0].cells[2].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t4.rows[0].cells[3].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for row_idx, d in enumerate(t4_data, start=1):
        row = t4.rows[row_idx]
        for col_idx in range(4):
            row.cells[col_idx].text = d[col_idx]
            for p in row.cells[col_idx].paragraphs:
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in (1, 2) else WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    set_font_run(r, FONT_FAMILY, 9.5, bold=(col_idx == 0))
    format_table(t4, t4_widths)

    # -------------------------------------------------------------
    # 15. CHAPTER 10: APPLICATIONS
    # -------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip() == "CHAPTER 10: APPLICATIONS":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
        elif "[List practical applications relevant to your project.]" in p.text or "The core principles demonstrated in this project—contiguous array record" in p.text:
            p.text = (
                "The core principles demonstrated in this project—contiguous array record tracking combined with "
                "circular FIFO queue waitlists—have widespread applications across real-world computing and logistics domains:\n\n"
                "1. University & Corporate Campus Accommodation: Automated assignment of hostel rooms, dormitories, and executive "
                "quarters with zero human bias and instant vacancy reallocation.\n"
                "2. Hospital Bed & ICU Patient Waitlists: Managing limited intensive care beds, ventilators, and surgical operating "
                "theaters where incoming patients must be placed in order-preserving queues during emergency surges.\n"
                "3. Operating System Process Scheduling: Circular FIFO ready-queues in round-robin CPU schedulers and I/O request "
                "buffers, where processes take turns utilizing finite computational hardware.\n"
                "4. Network Router Ring Buffers & Print Spoolers: Packet queue management in network interface controllers (NICs) "
                "and printer job queues, where incoming requests must be processed in temporal sequence without dropping packets.\n"
                "5. Transportation & Reservation Systems: Railway waiting list allotment (e.g., Tatkal/RAC reservation upgrades) where "
                "canceled tickets are automatically transferred to the first waiting passenger."
            )
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 12, bold=False)

    # -------------------------------------------------------------
    # 16. CHAPTER 11: LIMITATIONS AND FUTURE ENHANCEMENTS
    # -------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip() == "CHAPTER 11: LIMITATIONS AND FUTURE ENHANCEMENTS":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
        elif "Limitations:\n[Describe current limitations.]" in p.text or "Limitations:\n1. Static Array Capacity" in p.text:
            p.text = (
                "Limitations:\n"
                "1. Static Array Capacity: Fixed compile-time bounds (MAX_STUDENTS = 100, MAX_ROOMS = 50, MAX_QUEUE = 50). When system "
                "capacity is exceeded, additional registrations require re-compilation with enlarged constant definitions.\n"
                "2. Volatile In-Memory Storage: The current implementation stores all records in RAM; shutting down the application resets "
                "all records unless persistent file storage is interfaced.\n"
                "3. Single Waitlist Tier: All applicants are treated under a strict uniform FIFO discipline without priority quotas "
                "(e.g., medical emergency, sports quota, or senior student precedence).\n\n"
                "Future Enhancements:\n"
                "1. File I/O & Persistent Storage: Integrating binary file serialization or CSV database dumping to persist hostel state "
                "across application restarts.\n"
                "2. Multi-Queue Priority Tiering: Incorporating multi-level queues to balance FIFO fairness with special institutional "
                "quotas (e.g., international students, differently-abled quotas).\n"
                "3. Networked Client-Server Architecture: Exposing the C allocation engine through a lightweight TCP socket or REST API "
                "to allow concurrent web and mobile applications to submit accommodation requests."
            )
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 12, bold=False)

    # -------------------------------------------------------------
    # 17. CHAPTER 12: CONCLUSION
    # -------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip() == "CHAPTER 12: CONCLUSION":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
        elif "[Summarize the work completed, data structures applied, and outcomes achieved.]" in p.text or "The Smart Hostel Room Allocation and FIFO Waiting List Management System successfully demonstrates" in p.text:
            p.text = (
                "The Smart Hostel Room Allocation and FIFO Waiting List Management System successfully demonstrates how foundational "
                "linear data structures can be synthesized to engineer a high-performance, robust, and mathematically fair solution "
                "to real-world logistics challenges.\n\n"
                "By pairing contiguous 1D arrays with an array-based Circular FIFO Queue, the project achieves two paramount objectives:\n"
                "1. Eliminates queue drift and memory shifting penalties, delivering constant O(1) time complexity for enqueue and dequeue "
                "operations through elegant modulo pointer arithmetic.\n"
                "2. Guarantees absolute temporal fairness and non-bypassing priority in student room allotments, ensuring that vacant beds "
                "are automatically transferred to the rightful front-most candidate without administrative delays.\n\n"
                "The project was implemented in strict accordance with the C11 standard with zero heap allocation vulnerabilities, backed by "
                "a rigorous 63-test automated verification suite that validates 100% functional correctness, pointer wrap-around handling, and "
                "system stability."
            )
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 12, bold=False)

    # -------------------------------------------------------------
    # 18. CHAPTER 13: REFERENCES
    # -------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip() == "CHAPTER 13: REFERENCES":
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 14, bold=True)
        elif "1. [Reference 1]" in p.text or "1. Reema Thareja, \"Data Structures Using C\"" in p.text:
            p.text = (
                "1. Reema Thareja, \"Data Structures Using C\", 2nd Edition, Oxford University Press, 2014, Chapters 4 & 8 (Arrays, Queues and Circular Ring Buffers).\n"
                "2. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, \"Introduction to Algorithms\", 3rd Edition, MIT Press, 2009, Chapter 10 (Elementary Data Structures: Stacks and Queues).\n"
                "3. Brian W. Kernighan and Dennis M. Ritchie, \"The C Programming Language\", 2nd Edition, Prentice Hall PTR, 1988 (Structures, Pointers, and Arrays in C).\n"
                "4. Ellis Horowitz, Sartaj Sahni, and Susan Anderson-Freed, \"Fundamentals of Data Structures in C\", 2nd Edition, Silicon Press, 2008.\n"
                "5. ISO/IEC 9899:2011, \"Information Technology — Programming Languages — C\" (C11 Standard), International Organization for Standardization, Geneva, Switzerland, 2011."
            )
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                set_font_run(r, FONT_FAMILY, 11, bold=False)

    # -------------------------------------------------------------
    # 19. GLOBAL FONT ENFORCEMENT & NORMALIZATION
    # -------------------------------------------------------------
    # Ensure EVERY single run in the entire document uses Times New Roman
    for p in doc.paragraphs:
        for r in p.runs:
            set_font_run(r, FONT_FAMILY, r.font.size.pt if r.font.size else 12, bold=r.bold, italic=r.italic, color_rgb=r.font.color.rgb if r.font.color else None)

    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        set_font_run(r, FONT_FAMILY, r.font.size.pt if r.font.size else 10, bold=r.bold, italic=r.italic, color_rgb=r.font.color.rgb if r.font.color else None)

    # Save to primary location
    doc.save(OUTPUT_DOCX)
    print(f"Saved primary DOCX: {OUTPUT_DOCX}")

    try:
        shutil.copyfile(OUTPUT_DOCX, OUTPUT_FALLBACK_DOCX)
        print(f"Updated secondary DOCX: {OUTPUT_FALLBACK_DOCX}")
    except Exception as e:
        print(f"Note: {OUTPUT_FALLBACK_DOCX} is currently open in Word. Saved to {OUTPUT_DOCX}.")

    # Copy to Artifacts
    shutil.copyfile(OUTPUT_DOCX, OUTPUT_ARTIFACT_DOCX)
    print(f"Copied to Artifacts: {OUTPUT_ARTIFACT_DOCX}")

if __name__ == "__main__":
    main()
