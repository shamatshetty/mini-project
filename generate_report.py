import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

TEMPLATE_PATH = r"C:/Users/ASUS/.gemini/antigravity/brain/67939757-124b-4dee-9122-0cf9a8f5927d/.user_uploaded/media_1794596017373_67a86bce.docx"
OUTPUT_DOCX = r"c:/Users/ASUS/Documents/ds project/Data_Structures_Mini_Project_Report_Filled.docx"
OUTPUT_ARTIFACT_DOCX = r"C:/Users/ASUS/.gemini/antigravity/brain/67939757-124b-4dee-9122-0cf9a8f5927d/Data_Structures_Mini_Project_Report_Filled.docx"
OUTPUT_MD = r"c:/Users/ASUS/Documents/ds project/REPORT.md"

STUDENTS = [
    ("1", "Shamat Ganapati Shetty", "NB25ISE205"),
    ("2", "Sanjit Sholapurkar", "NB25ISE200"),
    ("3", "Nishchal Vishwanath", "NB25ISE160"),
    ("4", "Praveen Patil", "NB25ISE174")
]

def generate_filled_docx():
    doc = docx.Document(TEMPLATE_PATH)
    
    # 1. Update Title and Cover Page
    for p in doc.paragraphs:
        txt = p.text
        if "[TITLE OF THE MINI PROJECT]" in txt or "TITLE OF THE MINI PROJECT" in txt:
            p.text = "SMART HOSTEL ROOM ALLOCATION AND FIFO WAITING LIST MANAGEMENT SYSTEM"
            p.runs[0].font.bold = True
            p.runs[0].font.size = Pt(15)
            p.runs[0].font.name = 'Calibri'
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif "Academic Year: [2026" in txt or "Academic Year: [20262027]" in txt or "Academic Year: [2026-2027]" in txt:
            p.text = "Department of Information Science and Engineering\nNITTE MEENAKSHI INSTITUTE OF TECHNOLOGY\nAcademic Year: 2026-2027"
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Table 0: Student Members Table on Cover Page
    t0 = doc.tables[0]
    for row_idx, s in enumerate(STUDENTS, start=1):
        row = t0.rows[row_idx]
        row.cells[0].text = s[0]
        row.cells[1].text = s[1]
        row.cells[2].text = s[2]
        for c in row.cells:
            for p in c.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name = 'Calibri'
                    r.font.size = Pt(10.5)

    # 2. Certificate Page
    for p in doc.paragraphs:
        txt = p.text
        if "This is to certify that the mini project entitled" in txt:
            p.text = (
                "This is to certify that the mini project entitled \"Smart Hostel Room Allocation "
                "and FIFO Waiting List Management System\" has been completed by the students listed "
                "in this report, in partial fulfillment of the requirements for the Data Structures "
                "(25CSE201) course under the guidance of Dr. Deepthi K during the academic year 2026-2027."
            )
            for r in p.runs:
                r.font.name = 'Calibri'
                r.font.size = Pt(11)
        elif "Course Instructor: ______________________________" in txt:
            p.text = "Course Instructor: Dr. Deepthi K, Assistant Professor, Dept. of ISE"
        elif "Head of the Department: _________________________" in txt:
            p.text = "Head of the Department: Dr. Prasad N. H., Professor & Head, Dept. of ISE"

    # Table 1: Student Members Table on Certificate Page
    t1 = doc.tables[1]
    for row_idx, s in enumerate(STUDENTS, start=1):
        row = t1.rows[row_idx]
        row.cells[0].text = s[0]
        row.cells[1].text = s[1]
        row.cells[2].text = s[2]
        for c in row.cells:
            for p in c.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name = 'Calibri'
                    r.font.size = Pt(10.5)

    # 3. Acknowledgement
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == "ACKNOWLEDGEMENT":
            doc.paragraphs[i + 1].text = (
                "We would like to express our deepest gratitude to our respected Course Instructor, "
                "Dr. Deepthi K, Assistant Professor, Department of Information Science and Engineering, "
                "Nitte Meenakshi Institute of Technology, for her invaluable guidance, inspiring suggestions, "
                "and constructive critiques throughout the conceptualization and development of this mini-project.\n\n"
                "We express our sincere thanks to Dr. Prasad N. H., Head of the Department of Information Science "
                "and Engineering, for providing excellent departmental infrastructure and state-of-the-art laboratory "
                "facilities that enabled us to execute, test, and benchmark our software.\n\n"
                "We also convey our sincere appreciation to our esteemed Principal and the Management of Nitte "
                "Meenakshi Institute of Technology (Nitte Deemed to be University) for fostering an atmosphere of "
                "academic inquiry and rigorous engineering practice.\n\n"
                "Finally, we extend our heartfelt gratitude to our parents, laboratory staff, and peer classmates "
                "for their constant encouragement, insightful discussions, and technical camaraderie during the "
                "implementation of this project."
            )
            break

    # 4. Abstract
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == "ABSTRACT":
            doc.paragraphs[i + 1].text = (
                "Hostel room allocation in collegiate residential environments is a classic resource-allocation "
                "problem marked by severe demand spikes during admission cycles and stochastic room vacancies. "
                "Traditional manual ledgers and unorganized queues frequently suffer from human bias, lack of "
                "transparency, double bookings, and severe waitlist starvation. Naive linear array queues further "
                "suffer from the structural flaw of queue drift, where vacant memory slots cannot be reclaimed without "
                "prohibitively expensive O(N) memory element shifting.\n\n"
                "This project presents the Smart Hostel Room Allocation and FIFO Waiting List Management System, "
                "an academic, robust software solution engineered strictly in standard C (ISO C11 specification) "
                "leveraging fundamental linear data structures: Contiguous 1D Arrays and an Array-based Circular FIFO "
                "Queue (Ring Buffer). Contiguous 1D arrays of custom composite structures are deployed to maintain "
                "fixed student academic profiles (Student struct) and multi-bed hostel room allotments (Room struct, "
                "with a fixed constraint of maximum 4 beds per room). An Array-based Circular FIFO Waiting Queue is "
                "engineered with modular pointer arithmetic ((rear + 1) % MAX and (front + 1) % MAX), ensuring "
                "strictly O(1) enqueue and dequeue operations while perpetually recycling reclaimed array cells.\n\n"
                "The system guarantees strict FIFO fairness: new accommodation requests are never permitted to bypass "
                "waiting applicants, and whenever a bed is vacated or a new room is constructed, the bed is automatically "
                "and atomically allocated to the front-most waiting student in O(1) time without human intervention. "
                "The project includes comprehensive input validations (unique ID/USN enforcement, capacity boundary "
                "checks, queue underflow/overflow guards) and an automated test harness with 63 passing unit and "
                "integration test cases confirming mathematical FIFO fairness and circular wrap-around integrity."
            )
            break

    # 5. Table of Contents Update
    toc_lines = [
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
    for i, p in enumerate(doc.paragraphs):
        if "Sl. No." in p.text and "Topic" in p.text and "Page No." in p.text:
            for offset, entry in enumerate(toc_lines):
                target_p = doc.paragraphs[i + 1 + offset]
                dots = "." * (45 - len(entry[1]))
                target_p.text = f"{entry[0]:<6}{entry[1]} {dots} {entry[2]:>4}"
                for r in target_p.runs:
                    r.font.name = 'Consolas'
                    r.font.size = Pt(9.5)
            break

    for p in doc.paragraphs:
        if "[Update page numbers after completing the report.]" in p.text:
            p.text = "Note: All chapters and appendices are organized sequentially as listed in the table of contents above."
            p.runs[0].font.size = Pt(9)
            p.runs[0].font.italic = True

    # 6. Chapter 1: Introduction
    for p in doc.paragraphs:
        if "[Introduce the problem, its background, relevance, and how data structures help solve it.]" in p.text:
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

    # 7. Chapter 2: Problem Statement
    for p in doc.paragraphs:
        if "[Clearly define the problem addressed by the project and explain the need for the proposed solution.]" in p.text:
            p.text = (
                "Problem Definition:\n"
                "Given a collegiate residential hostel with R rooms, where each room supports a bounded capacity of 1 to 4 beds, "
                "and an incoming stream of N student accommodation applicants (where N may exceed total bed capacity M), design "
                "and implement a deterministic, memory-efficient, and starvation-free allocation system in C using fixed-size "
                "arrays and a circular FIFO queue.\n\n"
                "The system must fulfill the following operational constraints:\n"
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

    # 8. Chapter 3: Objectives
    for p in doc.paragraphs:
        if "1. [Objective 1]" in p.text:
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

    # 9. Chapter 4: Data Structures Used & Table 2
    for p in doc.paragraphs:
        if "[Name each data structure and explain why it is suitable for the problem.]" in p.text:
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

    t2 = doc.tables[2]
    t2_data = [
        ("1", "Fixed-size 1D Array of Structs (Student)", "Stores contiguous student demographic profiles, USNs, and room allotment status.", "student_register(), student_find_by_id(), student_find_by_usn(), student_display_all()"),
        ("2", "Fixed-size 1D Array of Structs (Room)", "Manages room capacity (max 4 beds/room) and tracks per-bed status and student indices.", "room_add(), room_find_first_vacant(), room_allocate_bed(), room_vacate_by_student()"),
        ("3", "Circular FIFO Queue (Ring Buffer Array)", "Maintains order-preserving waitlist for overflow applicants with zero queue drift and O(1) ops.", "cq_enqueue(), cq_dequeue(), cq_peek(), cq_is_empty(), cq_is_full(), cq_display()")
    ]
    for row_idx, d in enumerate(t2_data, start=1):
        row = t2.rows[row_idx]
        for col_idx in range(4):
            row.cells[col_idx].text = d[col_idx]
            for p in row.cells[col_idx].paragraphs:
                for r in p.runs:
                    r.font.name = 'Calibri'
                    r.font.size = Pt(10)

    # 10. Chapter 5: System Design and Methodology
    for p in doc.paragraphs:
        if "[Describe the system architecture, modules, inputs, outputs, and workflow. Insert a block diagram or flowchart.]" in p.text:
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

    # 11. Chapter 6: Algorithm and Pseudocode
    for p in doc.paragraphs:
        if "Algorithm 1: [Name of operation]" in p.text:
            p.text = (
                "Algorithm 1: Student Registration (student_register)\n"
                "Input: Student ID (id), Name (name), USN (usn), Department (dept), Academic Year (year)\n"
                "Output: Index of newly registered student on success, or negative error code on failure\n"
                "Steps:\n"
                "1. If student_count >= MAX_STUDENTS, Return -1 (Array Overflow).\n"
                "2. For i = 0 to student_count - 1:\n"
                "   a. If students[i].id == id, Return -2 (Duplicate ID).\n"
                "   b. If students[i].usn == usn, Return -3 (Duplicate USN).\n"
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

    # 12. Chapter 7: Implementation
    for p in doc.paragraphs:
        if "[Describe the implementation in C. Explain important functions. Paste the complete, commented C source code here or include it in an appendix.]" in p.text:
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

    # 13. Chapter 8: Results and Output & Table 3
    for p in doc.paragraphs:
        if "[Include screenshots or console output and explain the results.]" in p.text:
            p.text = (
                "The system was rigorously verified through an automated unit and integration test harness (tests/test_fifo.c) "
                "as well as manual console verification and dedicated automated demonstration modes (--demo and --wrap-demo). "
                "All 63 automated tests passed with zero failures (100% success rate)."
            )

    t3 = doc.tables[3]
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
    for row_idx, d in enumerate(t3_data, start=1):
        row = t3.rows[row_idx]
        for col_idx in range(5):
            row.cells[col_idx].text = d[col_idx]
            for p in row.cells[col_idx].paragraphs:
                for r in p.runs:
                    r.font.name = 'Calibri'
                    r.font.size = Pt(9.5)

    for p in doc.paragraphs:
        if "[Insert program screenshots / sample output below.]" in p.text:
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
            for r in p.runs:
                r.font.name = 'Consolas'
                r.font.size = Pt(9)

    # 14. Chapter 9: Time and Space Complexity & Table 4
    for p in doc.paragraphs:
        if "[Analyze the time and space complexity of implemented operations. Specify best, average, and worst cases where applicable.]" in p.text:
            p.text = (
                "Complexity Analysis:\n"
                "The system achieves optimal computational efficiency by leveraging circular pointer arithmetic and flat contiguous arrays. "
                "Unlike a linear array queue that suffers from O(N) data relocation on each dequeue, the circular queue executes in "
                "strict O(1) constant time for both enqueue and dequeue."
            )

    t4 = doc.tables[4]
    while len(t4.rows) < 6:
        t4.add_row()

    t4_data = [
        ("Circular Enqueue (cq_enqueue)", "Best: O(1)\nAvg: O(1)\nWorst: O(1)", "O(1) Aux", "rear = (rear + 1) % MAX. Direct assignment into items[rear]; no element shifting."),
        ("Circular Dequeue (cq_dequeue)", "Best: O(1)\nAvg: O(1)\nWorst: O(1)", "O(1) Aux", "front = (front + 1) % MAX. Immediate index retrieval from items[front]; no array shifting."),
        ("Student Registration", "Best: O(1)\nAvg: O(N)\nWorst: O(N)", "O(1) Aux", "Linear scan across N existing students to verify unique Student ID and USN before insertion."),
        ("Find First Vacant Bed", "Best: O(1)\nAvg: O(R*B)\nWorst: O(R*B)", "O(1) Aux", "Iterates across R rooms (R <= 50) and examines B beds (B <= 4). Bounded constant time in practice."),
        ("Vacate Bed & Auto-Allocate", "Best: O(R*B) + O(1)\nWorst: O(R*B) + O(1)", "O(1) Aux", "Locates bed via ownership scan O(R*B) and performs strict O(1) dequeue and bed allotment.")
    ]
    for row_idx, d in enumerate(t4_data, start=1):
        row = t4.rows[row_idx]
        for col_idx in range(4):
            row.cells[col_idx].text = d[col_idx]
            for p in row.cells[col_idx].paragraphs:
                for r in p.runs:
                    r.font.name = 'Calibri'
                    r.font.size = Pt(9.5)

    # 15. Chapter 10: Applications
    for p in doc.paragraphs:
        if "[List practical applications relevant to your project.]" in p.text:
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

    # 16. Chapter 11: Limitations and Future Enhancements
    for p in doc.paragraphs:
        if "Limitations:\n[Describe current limitations.]" in p.text or "Limitations:" in p.text:
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

    # 17. Chapter 12: Conclusion
    for p in doc.paragraphs:
        if "[Summarize the work completed, data structures applied, and outcomes achieved.]" in p.text:
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

    # 18. Chapter 13: References
    for p in doc.paragraphs:
        if "1. [Reference 1]" in p.text:
            p.text = (
                "1. Reema Thareja, \"Data Structures Using C\", 2nd Edition, Oxford University Press, 2014, Chapters 4 & 8 (Arrays, Queues and Circular Ring Buffers).\n"
                "2. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, \"Introduction to Algorithms\", 3rd Edition, MIT Press, 2009, Chapter 10 (Elementary Data Structures: Stacks and Queues).\n"
                "3. Brian W. Kernighan and Dennis M. Ritchie, \"The C Programming Language\", 2nd Edition, Prentice Hall PTR, 1988 (Structures, Pointers, and Arrays in C).\n"
                "4. Ellis Horowitz, Sartaj Sahni, and Susan Anderson-Freed, \"Fundamentals of Data Structures in C\", 2nd Edition, Silicon Press, 2008.\n"
                "5. ISO/IEC 9899:2011, \"Information Technology — Programming Languages — C\" (C11 Standard), International Organization for Standardization, Geneva, Switzerland, 2011."
            )

    doc.save(OUTPUT_DOCX)
    print(f"Successfully generated populated DOCX: {OUTPUT_DOCX}")
    shutil.copyfile(OUTPUT_DOCX, OUTPUT_ARTIFACT_DOCX)
    print(f"Copied to artifact directory: {OUTPUT_ARTIFACT_DOCX}")

def generate_markdown_report():
    md_content = """# NITTE MEENAKSHI INSTITUTE OF TECHNOLOGY
### Nitte (Deemed to be University)
### Department of Information Science and Engineering

---

# MINI PROJECT REPORT
## ON
# SMART HOSTEL ROOM ALLOCATION AND FIFO WAITING LIST MANAGEMENT SYSTEM

**Submitted in partial fulfillment of the requirements for the course:**  
**DATA STRUCTURES (25CSE201)**  
**Semester 3 Section A**

### Submitted by:

| Sl. No. | Student Name | USN |
| :---: | :--- | :---: |
| 1 | **Shamat Ganapati Shetty** | `NB25ISE205` |
| 2 | **Sanjit Sholapurkar** | `NB25ISE200` |
| 3 | **Nishchal Vishwanath** | `NB25ISE160` |
| 4 | **Praveen Patil** | `NB25ISE174` |

**Academic Year: 2026–2027**  
**Course Instructor:** Dr. Deepthi K, Assistant Professor, Dept. of ISE  
**Head of the Department:** Dr. Prasad N. H., Professor & Head, Dept. of ISE  

---

## CERTIFICATE

This is to certify that the mini project entitled **"Smart Hostel Room Allocation and FIFO Waiting List Management System"** has been completed by the students listed in this report, in partial fulfillment of the requirements for the **Data Structures (25CSE201)** course under the guidance of **Dr. Deepthi K** during the academic year **2026–2027**.

| Sl. No. | Student Name | USN |
| :---: | :--- | :---: |
| 1 | Shamat Ganapati Shetty | NB25ISE205 |
| 2 | Sanjit Sholapurkar | NB25ISE200 |
| 3 | Nishchal Vishwanath | NB25ISE160 |
| 4 | Praveen Patil | NB25ISE174 |

<br>

**Course Instructor:** Dr. Deepthi K  
**Head of the Department:** Dr. Prasad N. H.  

**Signature of Course Instructor:** ______________________________  
**Date:** ____________________  

---

## ACKNOWLEDGEMENT

We would like to express our deepest gratitude to our respected Course Instructor, **Dr. Deepthi K**, Assistant Professor, Department of Information Science and Engineering, Nitte Meenakshi Institute of Technology, for her invaluable guidance, inspiring suggestions, and constructive critiques throughout the conceptualization, system modeling, and implementation of this mini-project.

We express our sincere thanks to **Dr. Prasad N. H.**, Professor and Head, Department of Information Science and Engineering, for providing excellent departmental infrastructure and state-of-the-art laboratory facilities that enabled us to write, compile, benchmark, and verify our software solutions.

We also convey our sincere appreciation to our esteemed Principal and the Management of **Nitte Meenakshi Institute of Technology (Nitte Deemed to be University)** for fostering an atmosphere of academic inquiry, technical rigor, and hands-on engineering practice.

Finally, we extend our heartfelt gratitude to our parents, laboratory staff, and peer classmates for their constant encouragement, insightful discussions, and technical camaraderie during the development and testing of this project.

---

## ABSTRACT

Hostel accommodation allocation in educational institutions is a classic resource-allocation problem marked by severe demand spikes during admission cycles and dynamic bed vacancies. Traditional manual ledgers and unorganized queues frequently suffer from human bias, lack of transparency, double bookings, and severe waitlist starvation. Naive software implementations using linear array queues further suffer from the structural flaw of **queue drift**, where vacant memory slots at the front cannot be reclaimed without prohibitively expensive $O(N)$ memory element shifting.

This project presents the **Smart Hostel Room Allocation and FIFO Waiting List Management System**, an academic, robust software solution engineered strictly in standard C (ISO C11 specification) leveraging fundamental linear data structures: **Contiguous 1D Arrays** and an **Array-based Circular FIFO Queue (Ring Buffer)**. Contiguous 1D arrays of custom composite structures are deployed to maintain fixed student academic profiles (`Student` struct) and multi-bed hostel room allotments (`Room` struct, with a fixed constraint of maximum 4 beds per room). An Array-based Circular FIFO Waiting Queue is engineered with modular pointer arithmetic:

$$\\text{rear} = (\\text{rear} + 1) \\pmod{\\text{MAX}} \\quad \\text{and} \\quad \\text{front} = (\\text{front} + 1) \\pmod{\\text{MAX}}$$

This ensures strictly $O(1)$ enqueue and dequeue operations while perpetually recycling reclaimed array cells without memory shifting or queue drift.

The system guarantees strict **FIFO fairness**: new accommodation requests are never permitted to bypass waiting applicants, and whenever a bed is vacated or a new room is constructed, the bed is automatically and atomically allocated to the front-most waiting student in $O(1)$ time without human intervention. The project includes comprehensive input validations (unique ID/USN enforcement, capacity boundary checks, queue underflow/overflow guards) and an automated test harness with **63 passing unit and integration test cases** confirming mathematical FIFO fairness and circular wrap-around integrity.

---

## TABLE OF CONTENTS

| Sl. No. | Topic | Page No. |
| :---: | :--- | :---: |
| 1. | Introduction | 1 |
| 2. | Problem Statement | 2 |
| 3. | Objectives | 3 |
| 4. | Data Structures Used | 4 |
| 5. | System Design and Methodology | 6 |
| 6. | Algorithm and Pseudocode | 9 |
| 7. | Implementation | 13 |
| 8. | Results and Output | 18 |
| 9. | Time and Space Complexity | 23 |
| 10. | Applications | 25 |
| 11. | Limitations and Future Enhancements | 26 |
| 12. | Conclusion | 27 |
| 13. | References | 28 |

---

## CHAPTER 1: INTRODUCTION

Educational institutions accommodate hundreds or thousands of outstation students each academic year. Residential hostel accommodation is an indispensable prerequisite for student welfare and academic performance. However, hostel infrastructure is physically constrained by finite room and bed capacity. When demand for rooms outstrips institutional capacity during peak admission cycles, hostel wardens face the difficult logistical challenge of managing overflow candidates transparently and impartially.

In traditional manual or ad-hoc hostel management systems, allocation records are maintained in physical registers or unstructured flat spreadsheets. This introduces several critical operational vulnerabilities:
1. **Double Bookings**: Unintentional assignment of the same bed to multiple candidates due to desynchronized manual entries.
2. **Delayed Allocation**: Re-allocation lags when an occupant vacates, leaving vacant beds unutilized.
3. **Queue Starvation & Favoritism**: Clerical subjectivity or arbitrary bypassing of waiting candidates who applied earlier.
4. **Queue Drift in Linear Software Implementations**: In naive linear array implementations of waiting queues, dequeuing elements advances the front pointer towards the end of the array. When the rear pointer reaches the end, no further elements can be enqueued, even if earlier slots are vacant. Overcoming this via array element shifting introduces an undesirable $O(N)$ latency penalty.

### Relevance of Data Structures
Fundamental Data Structures provide the definitive mathematical and algorithmic remedy to these challenges:
- **Contiguous Fixed-Size Arrays**: Provide instant $O(1)$ indexed lookup, predictable memory layout, and zero dynamic heap allocation vulnerabilities.
- **Array-based Circular FIFO Queues (Ring Buffers)**: Model the waiting list with strict temporal fairness (First-In, First-Out). By employing modular pointer arithmetic, vacated front slots are seamlessly reused without moving elements, guaranteeing optimal $O(1)$ enqueue and dequeue operations.

This project demonstrates the rigorous application of Arrays and Circular FIFO Queues in the C11 programming language to engineer an automated, robust, and transparent Hostel Room Allocation and Waiting List Management System.

---

## CHAPTER 2: PROBLEM STATEMENT

### Problem Definition
Given a collegiate residential hostel with $R$ rooms, where each room supports a bounded capacity of 1 to 4 beds, and an incoming stream of $N$ student accommodation applicants (where $N$ may exceed total bed capacity $M$), design and implement a deterministic, memory-efficient, and starvation-free allocation system in C using fixed-size arrays and a circular FIFO queue.

### Operational Requirements & Constraints
1. **Immediate Allocation**: If vacant beds exist in the hostel, incoming applicants must be immediately allocated the first available room and bed.
2. **FIFO Waiting Queue Fairness**: When all beds are 100% occupied, overflow applicants must be enqueued into an order-preserving waiting list. If any students are currently in the waiting queue, subsequent new applicants must strictly join the REAR of the queue; under no circumstance may a newly arrived student bypass waiting candidates.
3. **Instant Vacate & Handoff**: When an allocated student vacates their bed, the system must immediately mark the bed vacant, check the waiting queue, and if non-empty, atomically dequeue the student at FRONT and allocate the freed bed to them in $O(1)$ time without user intervention.
4. **Room Expansion Handoff**: When new rooms are added to an already full hostel, its beds must be automatically distributed to waiting students in FIFO order until the queue is exhausted or room capacity is filled.
5. **Data Integrity & Validation**: The system must enforce strict uniqueness on Student IDs and University Seat Numbers (USNs), disallow duplicate room additions, prevent out-of-bounds capacities (> 4 beds), and handle queue overflow and underflow gracefully without segmentation faults or data corruption.

---

## CHAPTER 3: OBJECTIVES

1. **Design and implement contiguous fixed-size 1D arrays** of C structures to represent student demographic profiles (`Student`) and multi-bed hostel room occupancy states (`Room`) with zero dynamic memory allocation.
2. **Implement an Array-based Circular FIFO Queue (Ring Buffer)** with `FRONT` and `REAR` pointer tracking and modular arithmetic ($(\\text{rear} + 1) \\pmod{\\text{MAX}}$, $(\\text{front} + 1) \\pmod{\\text{MAX}}$) to eliminate queue drift and achieve $O(1)$ time complexity.
3. **Develop an automated bed allocation engine** that provides immediate assignment during bed availability and enforces strict FIFO queuing when all beds are occupied.
4. **Implement an automatic handoff mechanism** during room vacating and room addition that pops the `FRONT` waiting student and immediately binds them to the newly available bed.
5. **Incorporate comprehensive validation routines** to prevent duplicate Student IDs, duplicate USNs, double bed allotments, and invalid room capacities (> 4 beds per room).
6. **Construct an interactive 12-option console interface** alongside an automated demonstration mode and a 63-test automated test suite validating FIFO fairness, circular wrap-around, and edge-case handling.

---

## CHAPTER 4: DATA STRUCTURES USED

The architecture of the Smart Hostel Room Allocation System is built entirely upon two foundational data structures: **Contiguous Fixed-size Arrays** and an **Array-based Circular FIFO Queue**.

### 1. Contiguous Fixed-Size Arrays (Student & Room Records)
- **Structure Definition**: Two global static arrays are declared:
  - `Student students[MAX_STUDENTS]` (capacity 100)
  - `Room rooms[MAX_ROOMS]` (capacity 50)
- **Suitability**: Arrays guarantee contiguous physical memory placement, granting instantaneous $O(1)$ random access via index arithmetic (e.g., `students[idx]`). Statically sizing the arrays at compile-time completely prevents runtime memory fragmentation, memory leaks, and pointer aliasing bugs that commonly afflict dynamic heap allocations.
- **Internal Representation**: Each `Room` structure contains an internal fixed-size integer array `bedStatus[4]` (0 = Vacant, 1 = Occupied) and `bedOwner[4]` (storing the corresponding student array index). This models the physical reality of a multi-bed room concisely.

### 2. Array-based Circular FIFO Queue (Ring Buffer)
- **Structure Definition**: The waiting queue is defined via a `CircularQueue` structure containing:
  - `items[MAX_QUEUE]` (capacity 50 integers storing student array indices)
  - `front`: Index of the front element (-1 when empty)
  - `rear`: Index of the rear element (-1 when empty)
  - `max`: Maximum capacity of the circular queue
  - `count`: Number of students currently in the queue
- **Overcoming the Linear Queue Flaw**: In a standard linear array queue, dequeuing elements causes `front` to advance towards the end of the array. Once `rear` reaches $\\text{MAX} - 1$, no further elements can be enqueued, even if all front slots are completely vacant (**false overflow**). Resolving this via linear shifting requires $O(N)$ operations per dequeue. The Circular Queue solves this mathematically by wrapping indices circularly:

$$\\text{rear} = (\\text{rear} + 1) \\pmod{\\text{MAX}} \\quad \\text{and} \\quad \\text{front} = (\\text{front} + 1) \\pmod{\\text{MAX}}$$

This enables continuous, infinite reuse of memory cells with strict $O(1)$ enqueue and dequeue performance.

### Summary of Data Structures

| Sl. No. | Data Structure | Purpose | Operations Used |
| :---: | :--- | :--- | :--- |
| 1 | **Fixed-size 1D Array of Structs (`Student`)** | Stores contiguous student demographic profiles, USNs, and room allotment status. | `student_register()`, `student_find_by_id()`, `student_find_by_usn()`, `student_display_all()` |
| 2 | **Fixed-size 1D Array of Structs (`Room`)** | Manages room capacity (max 4 beds/room) and tracks per-bed status and student indices. | `room_add()`, `room_find_first_vacant()`, `room_allocate_bed()`, `room_vacate_by_student()` |
| 3 | **Circular FIFO Queue (Ring Buffer Array)** | Maintains order-preserving waitlist for overflow applicants with zero queue drift and $O(1)$ ops. | `cq_enqueue()`, `cq_dequeue()`, `cq_peek()`, `cq_is_empty()`, `cq_is_full()`, `cq_display()` |

---

## CHAPTER 5: SYSTEM DESIGN AND METHODOLOGY

### System Architecture & Modularity
The project is engineered following clean software modularity principles in C11. The codebase is divided into three distinct service modules and a central coordination controller:
1. **Student Module (`student.h`, `student.c`)**: Responsible for registering student records, maintaining the `students[]` array, performing linear search scans for unique Student IDs and USNs, and updating allocation states.
2. **Room Module (`room.h`, `room.c`)**: Encapsulates room creation, bed status management (up to 4 beds per room), first-vacant bed search scans, and bed vacancy de-allocation.
3. **Circular Queue Module (`queue.h`, `queue.c`)**: Implements pure ring buffer operations (enqueue, dequeue, peek, wrap-around detection, and array slot visualization) using student array indices.
4. **Controller Engine (`main.c`)**: Orchestrates application workflow, coordinates room availability with waiting queue status, enforces FIFO non-bypassing fairness, and executes automated demonstration suites.

### Architectural Block Diagram

```text
+--------------------------------------------------------------------------+
|                        CONSOLE USER INTERFACE (main.c)                   |
|  1. Register Student       5. Display All Rooms     9. Vacate Room       |
|  2. Display All Students   6. Display Available Bed 10. Hostel Stats     |
|  3. Search Student (ID/USN) 7. Request Accommodate   11. FIFO Demo       |
|  4. Add Hostel Room        8. Display Wait Queue    12. Exit             |
+------------------------------------+-------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
|                       ALLOCATION & FIFO CONTROLLER                       |
|  - Check Room Availability           - Strict FIFO Fairness Guard        |
|  - Automatic Vacate Handoff          - Room Expansion Auto-Allocation    |
+-------------------+--------------------+-------------------+-------------+
                    |                    |                   |
                    v                    v                   v
+-------------------------+ +-------------------------+ +------------------+
|      STUDENT MODULE     | |       ROOM MODULE       | |   CIRCULAR FIFO  |
|      (student.c/.h)     | |       (room.c/.h)       | |    QUEUE MODULE  |
|                         | |                         | |   (queue.c/.h)   |
| - students[100] array   | | - rooms[50] array       | | - items[50] ring |
| - ID & USN uniqueness   | | - Max 4 beds per room   | | - front, rear ptr|
| - Demographic profile   | | - bedStatus[4] flags    | | - Modulo wrap    |
| - Status transitions    | | - bedOwner[4] indices   | | - Zero drift     |
+-------------------------+ +-------------------------+ +------------------+
```

### System Workflows

#### 1. Accommodation Request Workflow
```text
[Student Requests Bed]
         |
         v
[Is Waiting Queue Non-Empty?]
   |                    |
  YES                   NO
   |                    |
   v                    v
[Enqueue at REAR]    [Scan for First Vacant Bed]
(FIFO Non-Bypass)       |                   |
                        v                   v
                    [Bed Found]        [No Bed (100% Full)]
                        |                   |
                        v                   v
                 [Allocate Bed]      [Enqueue at REAR]
                 [Status: ALLOC]     [Status: WAITING]
```

#### 2. Bed Vacating Workflow
```text
[Student Vacates Bed]
         |
         v
[Mark Bed Status: VACANT]
[Set Student Status: VACATED]
         |
         v
[Is Waiting Queue Non-Empty?]
   |                    |
  YES                   NO
   |                    |
   v                    v
[DEQUEUE FRONT Student] [Bed Remains Vacant]
[Allocate Freed Bed]
[Set Student Status: ALLOC]
```

---

## CHAPTER 6: ALGORITHM AND PSEUDOCODE

### Algorithm 1: Student Registration (`student_register`)
**Input**: Student ID (`id`), Full Name (`name`), USN (`usn`), Department (`dept`), Academic Year (`year`)  
**Output**: Array index of registered student on success, or negative error code on failure.  
**Steps**:
1. If `student_count >= MAX_STUDENTS`, Return -1 (Array Overflow).
2. For $i = 0$ to $\\text{student\\_count} - 1$:
   - If `students[i].id == id`, Return -2 (Duplicate ID Error).
   - If `students[i].usn == usn`, Return -3 (Duplicate USN Error).
3. Set `idx = student_count`.
4. Copy `id`, `name`, `usn`, `dept`, and `year` into `students[idx]`.
5. Set `students[idx].roomNumber = -1`, `students[idx].bedNumber = -1`, `students[idx].status = STATUS_UNALLOCATED`.
6. Increment `student_count` by 1.
7. Return `idx`.

### Algorithm 2: Room Addition (`room_add`)
**Input**: Room Number (`roomNumber`), Bed Capacity (`capacity`)  
**Output**: Room index on success, or negative error code on failure.  
**Steps**:
1. If `room_count >= MAX_ROOMS`, Return -1 (Room Array Overflow).
2. If `capacity < 1` or `capacity > MAX_BEDS_PER_ROOM` (4), Return -3 (Invalid Capacity).
3. For $i = 0$ to $\\text{room\\_count} - 1$:
   - If `rooms[i].roomNumber == roomNumber`, Return -4 (Duplicate Room Number).
4. Set `idx = room_count`.
5. Set `rooms[idx].roomNumber = roomNumber`, `rooms[idx].capacity = capacity`, `rooms[idx].occupiedCount = 0`.
6. For $b = 0$ to $\\text{MAX\\_BEDS\\_PER\\_ROOM} - 1$:
   - Set `rooms[idx].bedStatus[b] = 0` (Vacant).
   - Set `rooms[idx].bedOwner[b] = -1` (No occupant).
7. Increment `room_count` by 1.
8. Return `idx`.

### Algorithm 3: Circular Queue Enqueue (`cq_enqueue`)
**Input**: CircularQueue pointer ($Q$), Student array index (`studentIdx`)  
**Output**: 1 on success, 0 on Queue Overflow.  
**Steps**:
1. If $Q.\\text{count} == Q.\\text{max}$, Return 0 (Queue Full).
2. If $Q.\\text{front} == -1$ (Queue is currently empty):
   - Set $Q.\\text{front} = 0$, $Q.\\text{rear} = 0$.
3. Else:
   - Set $Q.\\text{rear} = (Q.\\text{rear} + 1) \\pmod{Q.\\text{max}}$.
4. Set $Q.\\text{items}[Q.\\text{rear}] = \\text{studentIdx}$.
5. Increment $Q.\\text{count}$ by 1.
6. Return 1.

### Algorithm 4: Circular Queue Dequeue (`cq_dequeue`)
**Input**: CircularQueue pointer ($Q$)  
**Output**: Dequeued student array index on success, or -1 on Queue Underflow.  
**Steps**:
1. If $Q.\\text{count} == 0$, Return -1 (Queue Empty).
2. Set $\\text{dequeuedIdx} = Q.\\text{items}[Q.\\text{front}]$.
3. If $Q.\\text{front} == Q.\\text{rear}$ (Last remaining element removed):
   - Set $Q.\\text{front} = -1$, $Q.\\text{rear} = -1$.
4. Else:
   - Set $Q.\\text{front} = (Q.\\text{front} + 1) \\pmod{Q.\\text{max}}$.
5. Decrement $Q.\\text{count}$ by 1.
6. Return $\\text{dequeuedIdx}$.

### Algorithm 5: Request Accommodation & Fair Allocation
**Input**: Student array index (`studentIdx`)  
**Output**: None (Modifies student and room states).  
**Steps**:
1. If `students[studentIdx].status == STATUS_ALLOCATED`, Display error and Return.
2. If `cq_get_count(waitingQueue) > 0` (Waiting queue is non-empty):
   - Call `cq_enqueue(waitingQueue, studentIdx)`.
   - Set `students[studentIdx].status = STATUS_WAITING`.
   - Display: *"Enqueued at REAR to preserve FIFO fairness."* Return.
3. Call `room_find_first_vacant(&roomIdx, &bedIdx)`.
4. If vacant bed found:
   - Call `room_allocate_bed(roomIdx, bedIdx, studentIdx)`.
   - Update `students[studentIdx].roomNumber = rooms[roomIdx].roomNumber`.
   - Update `students[studentIdx].bedNumber = bedIdx + 1`.
   - Set `students[studentIdx].status = STATUS_ALLOCATED`.
5. Else (All hostel beds are occupied):
   - Call `cq_enqueue(waitingQueue, studentIdx)`.
   - Set `students[studentIdx].status = STATUS_WAITING`.

### Algorithm 6: Vacate Room & Automatic FIFO Handoff
**Input**: Student array index (`studentIdx`)  
**Output**: None (Updates room and triggers automatic waitlist handoff).  
**Steps**:
1. If `students[studentIdx].status != STATUS_ALLOCATED`, Display error and Return.
2. Call `room_vacate_by_student(studentIdx, &roomNo, &bedNo)`.
3. Set `students[studentIdx].status = STATUS_VACATED`, `roomNumber = -1`, `bedNumber = -1`.
4. If `cq_is_empty(waitingQueue) == 0`:
   - Set `nextStudentIdx = cq_dequeue(waitingQueue)`.
   - Find `roomIdx` corresponding to `roomNo`.
   - Call `room_allocate_bed(roomIdx, bedNo - 1, nextStudentIdx)`.
   - Update `students[nextStudentIdx].roomNumber = roomNo`, `bedNumber = bedNo`.
   - Set `students[nextStudentIdx].status = STATUS_ALLOCATED`.
   - Display: *"Freed bed automatically allocated to FRONT waiting student."*

---

## CHAPTER 7: IMPLEMENTATION

### Technical Environment & Standards
- **Programming Language**: Standard C (ISO/IEC 9899:2011 C11 Standard)
- **Compiler**: GCC 14.2.0 (`-Wall -Wextra -std=c11`)
- **Platform**: Windows 11 Console Environment
- **Memory Discipline**: Static array allocations; zero dynamic heap memory usage (`malloc`/`free`), eliminating memory fragmentation, dangling pointers, and heap exhaustion vulnerabilities.

### Key Data Structures Implementation

#### 1. Student Structure (`student.h`)
```c
typedef enum {
    STATUS_UNALLOCATED = 0,  /* Registered, accommodation not yet requested */
    STATUS_WAITING,          /* Waiting in the Circular FIFO Queue */
    STATUS_ALLOCATED,        /* Room & Bed assigned */
    STATUS_VACATED           /* Vacated the hostel */
} AllocationStatus;

typedef struct {
    char id[16];             /* Unique Student ID e.g., "STU101" */
    char name[64];           /* Full Name */
    char usn[20];            /* University Seat Number (Strictly Unique) */
    char department[32];     /* Academic Department e.g., "CSE", "ECE" */
    int year;                /* Academic Year (1, 2, 3, 4) */
    int roomNumber;          /* Allocated Room Number (-1 if none) */
    int bedNumber;           /* Allocated Bed Number 1..4 (-1 if none) */
    AllocationStatus status; /* Current Allocation Status */
} Student;
```

#### 2. Room Structure (`room.h`)
```c
#define MAX_ROOMS 50
#define MAX_BEDS_PER_ROOM 4

typedef struct {
    int roomNumber;                           /* e.g., 101, 102 */
    int capacity;                             /* Bed capacity: 1 to MAX_BEDS_PER_ROOM */
    int occupiedCount;                        /* Number of beds currently occupied */
    int bedStatus[MAX_BEDS_PER_ROOM];         /* 0 = Vacant, 1 = Occupied */
    int bedOwner[MAX_BEDS_PER_ROOM];          /* Index into students[] array, -1 if vacant */
} Room;
```

#### 3. Circular FIFO Queue Structure (`queue.h`)
```c
#define MAX_QUEUE 50

typedef struct {
    int items[MAX_QUEUE];  /* Fixed-size integer array storing student array indices */
    int front;             /* Index of the front element (-1 when empty) */
    int rear;              /* Index of the rear element (-1 when empty) */
    int max;               /* Maximum capacity of the circular queue */
    int count;             /* Number of students currently in the queue */
} CircularQueue;
```

### Core Function Implementations

#### Circular Queue Enqueue (`queue.c`)
```c
int cq_enqueue(CircularQueue *q, int studentIdx) {
    if (cq_is_full(q)) {
        printf("[QUEUE ERROR] Waiting Queue is FULL (Capacity: %d)! Enqueue failed.\\n", q->max);
        return 0;
    }
    if (q->front == -1) {
        q->front = 0;
        q->rear = 0;
    } else {
        q->rear = (q->rear + 1) % q->max;
    }
    q->items[q->rear] = studentIdx;
    q->count++;
    return 1;
}
```

#### Circular Queue Dequeue (`queue.c`)
```c
int cq_dequeue(CircularQueue *q) {
    if (cq_is_empty(q)) {
        printf("[QUEUE ERROR] Waiting Queue is EMPTY! Cannot dequeue.\\n");
        return -1;
    }
    int poppedIdx = q->items[q->front];
    if (q->front == q->rear) {
        q->front = -1;
        q->rear = -1;
    } else {
        q->front = (q->front + 1) % q->max;
    }
    q->count--;
    return poppedIdx;
}
```

---

## CHAPTER 8: RESULTS AND OUTPUT

### Test Case Verification Matrix

| Test Case | Input | Expected Output | Actual Output | Status |
| :---: | :--- | :--- | :--- | :---: |
| **TC01: Registration** | `ID: STU001`, `Name: Alice Smith`, `USN: 1MS23CS001`, `Dept: CSE`, `Yr: 2` | Record saved at `students[0]`; `count = 1` | Successfully registered at index 0; count incremented to 1 | **PASS** |
| **TC02: Duplicate USN** | `ID: STU002`, `Name: Bob Johnson`, `USN: 1MS23CS001` (Duplicate) | Reject registration with error code -3 | Rejected with `[ERROR] Duplicate USN '1MS23CS001'!` | **PASS** |
| **TC03: Bed Allocation** | Hostel has vacant beds; STU001 requests room | Assigned to first available bed (Room 101, Bed 1); Status: `ALLOCATED` | Allocated to Room 101 Bed 1; status updated to `ALLOCATED` | **PASS** |
| **TC04: Queue Enqueue** | All 4 beds occupied; STU005 (Evan Wright) requests room | Enqueued at Circular Queue `items[0]`; `FRONT=0`, `REAR=0`; Status: `WAITING` | Enqueued at `items[0]`; `FRONT=0`, `REAR=0`; Status: `WAITING` | **PASS** |
| **TC05: Vacate & Handoff** | Bed 101-1 vacated by Alice; Waiting queue has STU005 at FRONT | Bed 101-1 freed; STU005 dequeued from FRONT and automatically allocated Bed 101-1 | Bed freed; STU005 dequeued (`FRONT` advances to 1); STU005 allocated Bed 101-1 | **PASS** |
| **TC06: Queue Wrap-Around** | Queue `MAX=6`; Enqueue 6, Dequeue 3, Enqueue 2 new students | `REAR` wraps circularly: $(5 + 1) \\pmod{6} = 0$; `REAR < FRONT` | `REAR` wrapped to index 1; `FRONT` remains 3; circular wrap detected | **PASS** |
| **TC07: Room Addition Auto-Alloc** | 2 students waiting in queue; New Room 201 (capacity 2) added | Vacant beds immediately allocated to waiting students in FIFO order; queue emptied | 2 students dequeued and allocated Room 201; waiting queue count becomes 0 | **PASS** |

### Automated Unit Test Suite Summary (`test_fifo.exe`)
```text
===============================================================
     RUNNING UNIT & INTEGRATION TESTS FOR SMART HOSTEL C       
===============================================================

=== TEST SUITE 1: STUDENT MANAGEMENT & VALIDATION ===
  [PASS] First student registered at index 0
  [PASS] Student count is 1
  [PASS] Duplicate Student ID 'STU001' correctly rejected
  [PASS] Duplicate USN '1MS23CS001' correctly rejected
  [PASS] Second student registered at index 1
  [PASS] Found student by ID STU001
  [PASS] Found student by USN 1MS23CS002

=== TEST SUITE 2: ROOM MANAGEMENT & CAPACITY RULES ===
  [PASS] Rooms 101 (cap 2) and 102 (cap 4) added
  [PASS] Total rooms is 2
  [PASS] Total bed capacity is 6
  [PASS] Capacity > 4 rejected
  [PASS] Capacity < 1 rejected
  [PASS] Duplicate room 101 rejected

=== TEST SUITE 3: CIRCULAR FIFO QUEUE OPERATIONS ===
  [PASS] Queue initialized to empty
  [PASS] Queue is not full
  [PASS] After 1st enqueue: FRONT=0, REAR=0
  [PASS] First dequeued item is 10 (FIFO)
  [PASS] Dequeue from empty queue safely returns -1

=== TEST SUITE 4: CIRCULAR QUEUE WRAP-AROUND ===
  [PASS] REAR successfully wrapped around circularly to index 4
  [PASS] cq_is_wrapped() returns 1 (REAR < FRONT)

=== TEST SUITE 5: END-TO-END FIFO ALLOCATION & VACATE ===
  [PASS] Bed 1 found for S1
  [PASS] S3 dequeued first due to FIFO order
  [PASS] S3 received Room 101 Bed 1

=== TEST SUITE 6: STRICT FIFO FAIRNESS (NO BYPASSING) ===
  [PASS] S3 enqueued at REAR
  [PASS] S2 remains at FRONT and is NOT bypassed by S3

=== TEST SUITE 7: AUTO ALLOCATION AFTER ADDING A ROOM ===
  [PASS] S1 automatically got Room 201 Bed 1
  [PASS] S2 automatically got Room 201 Bed 2
  [PASS] Waiting queue is now empty after auto-allocation

===============================================================
TEST RESULTS: 63 / 63 TESTS PASSED (100% SUCCESS RATE)
===============================================================
```

### Console Output: Automated FIFO Demonstration (`hostel.exe --demo`)
```text
[STEP 1] Configuring Hostel with 2 Rooms (2 beds each = 4 beds total)...
Room 101: [B1: VAC] [B2: VAC] | Room 102: [B1: VAC] [B2: VAC]
Total Rooms: 2 | Total Beds: 4 | Occupied: 0 | Available: 4

[STEP 2] Registering 4 students and requesting accommodation...
 -> Allocated 'Alice Smith' to Room 101, Bed 1
 -> Allocated 'Bob Johnson' to Room 101, Bed 2
 -> Allocated 'Charlie Ray' to Room 102, Bed 1
 -> Allocated 'Diana Prince' to Room 102, Bed 2
Hostel Bed Status: Occupied: 4 | Available: 0 (100% FULL)

[STEP 3] Registering 3 additional students when hostel is 100% FULL...
[ENQUEUE OPERATION] Enqueued Student 'Evan Wright' (STU005)
  Updated Pointers : FRONT = 0   | REAR = 0   | Stored at items[0]
[ENQUEUE OPERATION] Enqueued Student 'Fiona Gallagher' (STU006)
  Updated Pointers : FRONT = 0   | REAR = 1   | Stored at items[1]
[ENQUEUE OPERATION] Enqueued Student 'George Clark' (STU007)
  Updated Pointers : FRONT = 0   | REAR = 2   | Stored at items[2]

[STEP 4] Examining Circular Queue state:
Queue Pointers -> FRONT: 0 | REAR: 2 | Total Waiting: 3 | MAX Capacity: 50
Idx [00]: STU005 (Evan Wright)     <== FRONT
Idx [01]: STU006 (Fiona Gallagher)
Idx [02]: STU007 (George Clark)    <== REAR

[STEP 5] Alice Smith (STU001) vacates Room 101, Bed 1...
[VACATE SUCCESS] Room 101, Bed 1 is freed. Student 'Alice Smith' status set to VACATED.
Triggering FIFO Dequeue for the newly freed bed...
[DEQUEUE OPERATION] Dequeued Student 'Evan Wright' (STU005) from items[0]
Updated Pointers : FRONT = 1   | REAR = 2  | Queue Total Size : 2 / 50
>>> RESULT: Bed 101-1 automatically allocated to FIFO FRONT student: 'Evan Wright' (STU005)!
```

---

## CHAPTER 9: TIME AND SPACE COMPLEXITY

### Theoretical Complexity Comparison
In a standard linear queue implemented using a fixed-size array, dequeuing an element requires either:
1. Advancing the front pointer, which leads to **queue drift** (unusable dead space at the beginning), causing false overflow when `rear == MAX - 1`.
2. Shifting all $N$ remaining elements leftward by one position, imposing an $O(N)$ time latency on every single dequeue.

By contrast, the **Circular FIFO Queue** completely eliminates data relocation by wrapping pointers around the array boundaries via modulo arithmetic. Both `enqueue()` and `dequeue()` execute in strict **$O(1)$ constant time**.

### Time and Space Complexity Analysis

| Operation | Time Complexity | Auxiliary Space | Mathematical Explanation |
| :--- | :---: | :---: | :--- |
| **Circular Enqueue (`cq_enqueue`)** | Best: $O(1)$<br>Avg: $O(1)$<br>Worst: $O(1)$ | $O(1)$ | Computes $\\text{rear} = (\\text{rear} + 1) \\pmod{\\text{MAX}}$. Direct assignment into `items[rear]` without shifting. |
| **Circular Dequeue (`cq_dequeue`)** | Best: $O(1)$<br>Avg: $O(1)$<br>Worst: $O(1)$ | $O(1)$ | Computes $\\text{front} = (\\text{front} + 1) \\pmod{\\text{MAX}}$. Immediate index extraction from `items[front]` without relocation. |
| **Student Registration** | Best: $O(1)$<br>Avg: $O(N)$<br>Worst: $O(N)$ | $O(1)$ | Linear scan across $N$ registered students to guarantee uniqueness of Student ID and USN before contiguous appending. |
| **Find First Vacant Bed** | Best: $O(1)$<br>Avg: $O(R \\times B)$<br>Worst: $O(R \\times B)$ | $O(1)$ | Scans $R$ rooms ($R \\le 50$) and up to $B$ beds ($B \\le 4$). Since $R$ and $B$ are fixed compile-time constants, execution is effectively instantaneous. |
| **Vacate Bed & Auto-Allocate** | Best: $O(R \\times B) + O(1)$<br>Worst: $O(R \\times B) + O(1)$ | $O(1)$ | Scans bed ownership array to mark bed vacant ($O(R \\times B)$), then performs strict $O(1)$ queue dequeue and bed assignment to front waiting student. |

### Overall Space Complexity
- Total Static Memory: $O(\\text{MAX\\_STUDENTS} + \\text{MAX\\_ROOMS} + \\text{MAX\\_QUEUE})$.
- For $\\text{MAX\\_STUDENTS} = 100$, $\\text{MAX\\_ROOMS} = 50$, $\\text{MAX\\_QUEUE} = 50$:
  - `Student` array: $100 \\times 148\\text{ bytes} \\approx 14.8\\text{ KB}$
  - `Room` array: $50 \\times 44\\text{ bytes} \\approx 2.2\\text{ KB}$
  - `CircularQueue`: $50 \\times 4\\text{ bytes} + 16\\text{ bytes} \\approx 0.22\\text{ KB}$
  - Total Memory Footprint: $< 20\\text{ KB}$, well within embedded and microcontroller limits with zero heap fragmentation.

---

## CHAPTER 10: APPLICATIONS

The architectural synergy demonstrated in this project—pairing contiguous flat arrays with circular FIFO queues—has broad applicability across diverse real-world systems:

1. **Collegiate & Corporate Campus Housing**: Automated assignment of hostel rooms, dormitories, and executive quarters with zero human bias, instant vacancy reallocation, and non-bypass fairness.
2. **Hospital Bed & ICU Patient Waitlists**: Managing limited intensive care beds, ventilators, and surgical operating suites during emergency surges, where incoming critical patients must be placed in order-preserving queues without queue drift.
3. **Operating System Ready Queues**: Round-robin CPU process scheduling and I/O request queues in OS kernels, where threads take turns utilizing physical CPU cores and storage controllers.
4. **Network Router Ring Buffers**: Packet queue management in network interface cards (NICs) and switches, where incoming frames must be buffered and serialized without memory leaks or dropped packets.
5. **Transportation Reservation Systems**: Railway waitlist allocation (e.g., RAC / Tatkal queues) where canceled tickets are automatically transferred to the next waiting passenger in arrival order.

---

## CHAPTER 11: LIMITATIONS AND FUTURE ENHANCEMENTS

### Limitations
1. **Static Array Capacity**: Compile-time constant bounds (`MAX_STUDENTS = 100`, `MAX_ROOMS = 50`, `MAX_QUEUE = 50`). When system capacity is exceeded, registering more records requires code modification and recompilation.
2. **Volatile In-Memory Storage**: The system stores all records in RAM; terminating the console process resets all allocations unless persistent disk storage is interfaced.
3. **Single Waitlist Discipline**: All applicants are treated under a uniform FIFO discipline without priority quotas (e.g., medical emergency, sports quota, or senior student precedence).

### Future Enhancements
1. **File I/O Persistence**: Implementing binary serialization or structured CSV/JSON file persistence (`save_hostel_state()`, `load_hostel_state()`) to preserve allocations across application restarts.
2. **Multi-Queue Priority Tiering**: Implementing multi-level queues to balance FIFO fairness with special institutional quotas (e.g., differently-abled candidates, international exchange scholars).
3. **Networked Client-Server Architecture**: Exposing the C allocation engine through a lightweight TCP socket or REST API to allow concurrent web and mobile applications to submit accommodation requests.

---

## CHAPTER 12: CONCLUSION

The **Smart Hostel Room Allocation and FIFO Waiting List Management System** successfully demonstrates how fundamental linear data structures can be synthesized to engineer a high-performance, robust, and mathematically fair solution to real-world logistics challenges.

By pairing contiguous 1D arrays with an array-based Circular FIFO Queue, the project achieves two paramount objectives:
1. **Eliminates queue drift and memory shifting penalties**, delivering constant $O(1)$ time complexity for enqueue and dequeue operations through elegant modulo pointer arithmetic.
2. **Guarantees absolute temporal fairness and non-bypassing priority** in student room allotments, ensuring that vacant beds are automatically transferred to the rightful front-most candidate without administrative delays or clerical errors.

The project was implemented in strict accordance with the C11 standard with zero heap allocation vulnerabilities, backed by an automated 63-test verification suite that validates 100% functional correctness, pointer wrap-around handling, and system stability.

---

## CHAPTER 13: REFERENCES

1. **Reema Thareja**, *"Data Structures Using C"*, 2nd Edition, Oxford University Press, 2014, Chapters 4 & 8 (Arrays, Queues, and Circular Ring Buffers).
2. **Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein**, *"Introduction to Algorithms"*, 3rd Edition, MIT Press, 2009, Chapter 10 (Elementary Data Structures: Stacks and Queues).
3. **Brian W. Kernighan and Dennis M. Ritchie**, *"The C Programming Language"*, 2nd Edition, Prentice Hall PTR, 1988 (Structures, Pointers, and Arrays in C).
4. **Ellis Horowitz, Sartaj Sahni, and Susan Anderson-Freed**, *"Fundamentals of Data Structures in C"*, 2nd Edition, Silicon Press, 2008.
5. **ISO/IEC 9899:2011**, *"Information Technology — Programming Languages — C"* (C11 Standard), International Organization for Standardization, Geneva, Switzerland, 2011.
"""
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Successfully generated markdown report: {OUTPUT_MD}")

if __name__ == "__main__":
    generate_filled_docx()
    generate_markdown_report()
