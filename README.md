# Smart Hostel Room Allocation & FIFO Waiting List Management System

A robust Data Structures mini-project in **C11**, strictly utilizing **Fixed-size Arrays** and a **Circular FIFO Queue**. Built for GCC with zero warnings (`-Wall -Wextra -std=c11`).

---

## 1. Project Overview & Data Structures

- **Language**: Standard C (C11 standard)
- **Data Structures**:
  1. **Fixed Arrays**: Contiguous storage for student records (`students[]`) and room configurations (`rooms[]`).
  2. **Circular FIFO Queue**: Array-based ring buffer maintaining `FRONT`, `REAR`, `MAX`, and `count` to manage the waiting list fairly without queue drift.
- **Rules**:
  - Max 4 beds per room (`bedStatus[4]`, `bedOwner[4]`).
  - Unique Student ID & Unique USN strictly enforced.
  - Vacating a bed automatically triggers a `dequeue()` from `FRONT` to assign the bed to the first waiting applicant.

---

## 2. Compilation & Execution

### Compile with GCC
Using the provided `make.bat` or standard GCC:
```bash
gcc -Wall -Wextra -std=c11 main.c student.c room.c queue.c -o hostel.exe
```

### Run the Interactive Menu
```bash
.\hostel.exe
```

### Run the 1-Click Automated FIFO Demonstration
```bash
.\hostel.exe --demo
```

### Run All Unit & Integration Tests (51 Tests)
```bash
.\run_tests.bat
```

---

## 3. Menu Options

```
====================================================================
    SMART HOSTEL ROOM ALLOCATION & FIFO WAITING LIST SYSTEM        
====================================================================
  1. Register Student
  2. Display All Students
  3. Search Student (by ID or USN)
  4. Add Hostel Room
  5. Display All Rooms
  6. Display Available Beds
  7. Request Hostel Accommodation
  8. Display FIFO Waiting Queue
  9. Vacate Room
 10. Display Hostel Statistics
 11. Run FIFO Demonstration Mode
  0. Exit System
====================================================================
```

---

## 4. Visual Web Dashboard

Open `web/index.html` in any web browser, or view the generated artifact dashboard:
- Visual floor plan of all hostel rooms & bed occupancy
- Real-time animated circular queue ring buffer
- Live statistics bar
- Step-by-step interactive FIFO demonstration runner

---

## 5. Deliverables & Documentation

- Comprehensive Academic Report: [`REPORT.md`](file:///c:/Users/ASUS/Documents/ds%20project/REPORT.md)
- Unit & Integration Test Suite: [`tests/test_fifo.c`](file:///c:/Users/ASUS/Documents/ds%20project/tests/test_fifo.c)
