#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "student.h"
#include "room.h"
#include "queue.h"

/* Global Circular FIFO Waiting Queue */
static CircularQueue waitingQueue;

/* Input Helper Functions */
static void read_line(const char *prompt, char *buffer, int size) {
    if (prompt) {
        printf("%s", prompt);
    }
    if (fgets(buffer, size, stdin)) {
        size_t len = strlen(buffer);
        if (len > 0 && buffer[len - 1] == '\n') {
            buffer[len - 1] = '\0';
        }
    } else {
        buffer[0] = '\0';
        clearerr(stdin);
    }
}

static int read_int(const char *prompt, int minVal, int maxVal) {
    char line[64];
    int val;
    while (1) {
        read_line(prompt, line, sizeof(line));
        if (sscanf(line, "%d", &val) == 1) {
            if (val >= minVal && val <= maxVal) {
                return val;
            }
            printf("[INVALID] Please enter a value between %d and %d.\n", minVal, maxVal);
        } else {
            printf("[INVALID] Numerical input expected. Please try again.\n");
        }
    }
}

/* Feature 1: Register Student */
static void handle_register_student(void) {
    char id[ID_LEN], name[NAME_LEN], usn[USN_LEN], dept[DEPT_LEN];
    int year;

    printf("\n--- REGISTER NEW STUDENT ---\n");
    read_line("Enter Student ID (e.g. STU101): ", id, sizeof(id));
    if (strlen(id) == 0) {
        printf("[ERROR] Student ID cannot be empty.\n");
        return;
    }
    if (student_find_by_id(id) != -1) {
        printf("[ERROR] Student ID '%s' is already registered!\n", id);
        return;
    }

    read_line("Enter Student Name: ", name, sizeof(name));
    if (strlen(name) == 0) {
        printf("[ERROR] Name cannot be empty.\n");
        return;
    }

    read_line("Enter USN (e.g. 1MS23CS001): ", usn, sizeof(usn));
    if (strlen(usn) == 0) {
        printf("[ERROR] USN cannot be empty.\n");
        return;
    }
    if (student_find_by_usn(usn) != -1) {
        printf("[ERROR] Duplicate USN '%s' rejected! Already registered.\n", usn);
        return;
    }

    read_line("Enter Department (e.g. CSE, ECE, MECH): ", dept, sizeof(dept));
    year = read_int("Enter Year of Study (1 - 4): ", 1, 4);

    int idx = student_register(id, name, usn, dept, year);
    if (idx >= 0) {
        printf("\n[SUCCESS] Student '%s' (%s) registered successfully at array index %d!\n", name, id, idx);
    }
}

/* Feature 2: Display All Students */
static void handle_display_all_students(void) {
    student_display_all();
}

/* Feature 3: Search Student */
static void handle_search_student(void) {
    printf("\n--- SEARCH STUDENT RECORD ---\n");
    printf("1. Search by Student ID\n");
    printf("2. Search by USN\n");
    int choice = read_int("Choose search mode (1-2): ", 1, 2);

    int idx = -1;
    if (choice == 1) {
        char id[ID_LEN];
        read_line("Enter Student ID to search: ", id, sizeof(id));
        idx = student_find_by_id(id);
    } else {
        char usn[USN_LEN];
        read_line("Enter USN to search: ", usn, sizeof(usn));
        idx = student_find_by_usn(usn);
    }

    if (idx == -1) {
        printf("[NOT FOUND] No student matching the criteria was found in the database.\n");
    } else {
        printf("\n[RECORD FOUND] Student details at array index %d:\n", idx);
        student_display_single(idx);
    }
}

/* Feature 4: Add Hostel Room (with Automatic Allocation to Waiting Queue) */
static void handle_add_room(void) {
    printf("\n--- ADD HOSTEL ROOM ---\n");
    int roomNum = read_int("Enter Room Number (e.g. 101, 102): ", 1, 9999);
    int cap = read_int("Enter Bed Capacity (1 to 4): ", 1, MAX_BEDS_PER_ROOM);

    int newRoomIdx = room_add(roomNum, cap);
    if (newRoomIdx >= 0) {
        printf("[SUCCESS] Room %d with capacity %d beds added successfully.\n", roomNum, cap);

        /*
         * AUTOMATIC ALLOCATION AFTER ADDING A ROOM:
         * Check the waiting queue. If students are currently waiting,
         * immediately allocate the newly available beds to waiting students in FIFO order.
         */
        if (!cq_is_empty(&waitingQueue)) {
            printf("\n>>> AUTOMATIC ALLOCATION TRIGGERED BY NEW ROOM <<<\n");
            printf("Waiting queue contains %d student(s). Allocating newly added beds in FIFO order...\n",
                   cq_get_count(&waitingQueue));

            Room *newRoom = room_get_by_index(newRoomIdx);
            int allocatedCount = 0;

            for (int b = 0; b < newRoom->capacity && !cq_is_empty(&waitingQueue); b++) {
                if (newRoom->bedStatus[b] == 0) {
                    int nextStudentIdx = cq_dequeue(&waitingQueue);
                    if (nextStudentIdx >= 0) {
                        Student *nextStudent = student_get_by_index(nextStudentIdx);
                        room_allocate_bed(newRoomIdx, b, nextStudentIdx);
                        nextStudent->roomNumber = newRoom->roomNumber;
                        nextStudent->bedNumber = b + 1;
                        nextStudent->status = STATUS_ALLOCATED;
                        allocatedCount++;

                        printf("  -> Bed %d allocated to FRONT student: '%s' (%s, USN: %s)\n",
                               b + 1, nextStudent->name, nextStudent->id, nextStudent->usn);
                    }
                }
            }
            printf("[AUTO-ALLOCATION COMPLETE] %d bed(s) in Room %d allocated to waiting students.\n",
                   allocatedCount, roomNum);
            printf("Remaining in Waiting Queue: %d student(s).\n", cq_get_count(&waitingQueue));
        } else {
            printf("[INFO] Waiting queue is empty. All %d beds in Room %d remain vacant for incoming requests.\n",
                   cap, roomNum);
        }
    }
}

/* Feature 5: Display All Rooms */
static void handle_display_all_rooms(void) {
    room_display_all();
}

/* Feature 6: Display Available Beds */
static void handle_display_available_beds(void) {
    room_display_vacant_beds();
}

/* Feature 7: Request Hostel Accommodation (Strict FIFO Fairness Enforced) */
static void handle_request_accommodation(void) {
    printf("\n--- REQUEST HOSTEL ACCOMMODATION ---\n");
    char searchKey[ID_LEN];
    read_line("Enter Student ID or USN: ", searchKey, sizeof(searchKey));

    int sIdx = student_find_by_id(searchKey);
    if (sIdx == -1) {
        sIdx = student_find_by_usn(searchKey);
    }

    if (sIdx == -1) {
        printf("[ERROR] Student '%s' is not registered. Please register first (Option 1).\n", searchKey);
        return;
    }

    Student *s = student_get_by_index(sIdx);

    /* VALIDATION: Prevent double room allocation */
    if (s->status == STATUS_ALLOCATED) {
        printf("[VALIDATION NOTICE] Double allocation prevented! Student '%s' (%s) is ALREADY allocated Room %d, Bed %d.\n",
               s->name, s->id, s->roomNumber, s->bedNumber);
        return;
    }

    /* VALIDATION: Prevent duplicate waiting queue entry */
    if (s->status == STATUS_WAITING) {
        printf("[VALIDATION NOTICE] Student '%s' (%s) is ALREADY in the FIFO Waiting Queue.\n",
               s->name, s->id);
        return;
    }

    /*
     * 1. FIFO FAIRNESS ENFORCEMENT:
     * If the waiting queue is not empty, every new accommodation request must enter
     * the REAR of the queue. Never allow a newly registered student to bypass existing waiting students!
     * Always allocate vacant beds to the student at FRONT first.
     */
    if (!cq_is_empty(&waitingQueue)) {
        printf("\n[FIFO FAIRNESS ENFORCED] Waiting queue contains %d student(s) waiting.\n",
               cq_get_count(&waitingQueue));
        printf("New applicant '%s' (%s) CANNOT bypass waiting students and must enter the REAR of the queue.\n",
               s->name, s->id);

        int enqRes = cq_enqueue(&waitingQueue, sIdx);
        if (enqRes == 0) {
            printf("[WAITING LIST] Student '%s' added to REAR of Waiting Queue (Position #%d).\n",
                   s->name, cq_get_count(&waitingQueue));
        }

        /* If any vacant bed is available anywhere in the hostel, allocate it to the FRONT student first */
        int rIdx = -1, bIdx = -1;
        while (!cq_is_empty(&waitingQueue) && room_find_first_vacant(&rIdx, &bIdx)) {
            int frontStudentIdx = cq_dequeue(&waitingQueue);
            if (frontStudentIdx >= 0) {
                Student *fs = student_get_by_index(frontStudentIdx);
                room_allocate_bed(rIdx, bIdx, frontStudentIdx);
                Room *r = room_get_by_index(rIdx);
                fs->roomNumber = r->roomNumber;
                fs->bedNumber = bIdx + 1;
                fs->status = STATUS_ALLOCATED;

                printf("\n>>> [FIFO BED ALLOCATION] Vacant Bed in Room %d (Bed %d) allocated to FRONT student: '%s' (%s)!\n",
                       fs->roomNumber, fs->bedNumber, fs->name, fs->id);
            }
        }
        return;
    }

    /*
     * If the waiting queue is empty, check if any vacant bed is available in any room.
     */
    int roomIdx = -1, bedIdx = -1;
    int foundVacant = room_find_first_vacant(&roomIdx, &bedIdx);

    if (foundVacant) {
        /* Allocate the bed directly */
        room_allocate_bed(roomIdx, bedIdx, sIdx);
        Room *r = room_get_by_index(roomIdx);

        s->roomNumber = r->roomNumber;
        s->bedNumber = bedIdx + 1; /* 1-based index for bed */
        s->status = STATUS_ALLOCATED;

        printf("\n========================================================\n");
        printf(">>> ACCOMMODATION ALLOCATED IMMEDIATELY! <<<\n");
        printf("Student   : %s (%s)\n", s->name, s->id);
        printf("Room No   : %d\n", s->roomNumber);
        printf("Bed No    : %d\n", s->bedNumber);
        printf("Status    : ALLOCATED\n");
        printf("========================================================\n");
    } else {
        /* No beds free -> Insert student into Circular FIFO Waiting Queue */
        printf("\n[HOSTEL FULL] No vacant beds currently available.\n");
        printf("Enqueuing student '%s' into FIFO Waiting Queue...\n", s->name);

        int enqRes = cq_enqueue(&waitingQueue, sIdx);
        if (enqRes == 0) {
            printf("[WAITING LIST] Student '%s' (%s) is queued at REAR=%d.\n",
                   s->name, s->id, cq_get_rear(&waitingQueue));
        }
    }
}

/* Feature 8: Display FIFO Waiting Queue (with Full Indexes and Wrap-Around Visualization) */
static void handle_display_queue(void) {
    cq_display(&waitingQueue);
}

/* Feature 9: Vacate Room */
static void handle_vacate_room(void) {
    printf("\n--- VACATE ROOM & BED ---\n");
    char searchKey[ID_LEN];
    read_line("Enter Student ID or USN vacating accommodation: ", searchKey, sizeof(searchKey));

    int sIdx = student_find_by_id(searchKey);
    if (sIdx == -1) {
        sIdx = student_find_by_usn(searchKey);
    }

    if (sIdx == -1) {
        printf("[ERROR] Student '%s' not found.\n", searchKey);
        return;
    }

    Student *s = student_get_by_index(sIdx);
    if (s->status != STATUS_ALLOCATED) {
        printf("[ERROR] Student '%s' (%s) does not currently occupy any hostel bed (Status: %s).\n",
               s->name, s->id, student_status_to_string(s->status));
        return;
    }

    int vacatedRoom = s->roomNumber;
    int vacatedBed = s->bedNumber;

    /* Free the bed from room records */
    int roomIdx = room_find_by_number(vacatedRoom);
    int bedIdx = vacatedBed - 1;

    room_update_bed_status(vacatedRoom, vacatedBed, 0, -1);

    /* Update student record to VACATED */
    s->roomNumber = -1;
    s->bedNumber = -1;
    s->status = STATUS_VACATED;

    printf("\n[BED FREED] Room %d, Bed %d has been vacated by '%s' (%s).\n",
           vacatedRoom, vacatedBed, s->name, s->id);

    /* FIFO RULE: Check whether the waiting queue contains students */
    if (!cq_is_empty(&waitingQueue)) {
        printf("\n>>> AUTOMATIC FIFO ALLOCATION TRIGGERED <<<\n");
        printf("Waiting Queue is not empty. Dequeuing FRONT student to allocate freed bed...\n");

        int nextStudentIdx = cq_dequeue(&waitingQueue);
        if (nextStudentIdx >= 0) {
            Student *nextStudent = student_get_by_index(nextStudentIdx);
            room_allocate_bed(roomIdx, bedIdx, nextStudentIdx);

            nextStudent->roomNumber = vacatedRoom;
            nextStudent->bedNumber = vacatedBed;
            nextStudent->status = STATUS_ALLOCATED;

            printf("\n============================================================\n");
            printf(">>> BED REALLOCATED TO WAITING STUDENT (FIFO) <<<\n");
            printf("Assigned To : %s (ID: %s, USN: %s)\n", nextStudent->name, nextStudent->id, nextStudent->usn);
            printf("Room Number : %d\n", nextStudent->roomNumber);
            printf("Bed Number  : %d\n", nextStudent->bedNumber);
            printf("Status      : ALLOCATED\n");
            printf("============================================================\n");
        }
    } else {
        printf("[QUEUE EMPTY] No students in waiting queue. Bed remains VACANT for new requests.\n");
    }
}

/* Feature 10: Display Hostel Statistics & Comprehensive Report */
static void handle_hostel_statistics(void) {
    int totalRooms = room_get_count();
    int totalCapacity = room_get_total_capacity();
    int totalOccupied = room_get_total_occupied();
    int totalVacant = room_get_total_vacant();
    int waitingCount = cq_get_count(&waitingQueue);
    int totalRegistered = student_get_count();

    int allocatedCount = 0;
    int vacatedCount = 0;
    int unallocatedCount = 0;

    for (int i = 0; i < totalRegistered; i++) {
        Student *s = student_get_by_index(i);
        if (s) {
            if (s->status == STATUS_ALLOCATED) allocatedCount++;
            else if (s->status == STATUS_VACATED) vacatedCount++;
            else if (s->status == STATUS_UNALLOCATED) unallocatedCount++;
        }
    }

    double occRate = (totalCapacity > 0) ? ((double)totalOccupied / totalCapacity) * 100.0 : 0.0;

    printf("\n====================================================================\n");
    printf("                    HOSTEL OCCUPANCY & SYSTEM REPORT                \n");
    printf("====================================================================\n");
    printf("  1. Total Rooms Configured     : %d\n", totalRooms);
    printf("  2. Total Beds (Capacity)      : %d\n", totalCapacity);
    printf("  3. Total Occupied Beds        : %d\n", totalOccupied);
    printf("  4. Total Vacant / Free Beds   : %d\n", totalVacant);
    printf("  5. Total Waiting Students     : %d\n", waitingCount);
    printf("  6. Hostel Occupancy Percentage: %.2f%%\n", occRate);
    printf("--------------------------------------------------------------------\n");
    printf("  Student Status Distribution:\n");
    printf("    - Registered (Total)        : %d\n", totalRegistered);
    printf("    - Allocated Bed             : %d\n", allocatedCount);
    printf("    - In Waiting Queue          : %d\n", waitingCount);
    printf("    - Unallocated (New)         : %d\n", unallocatedCount);
    printf("    - Vacated                   : %d\n", vacatedCount);
    printf("--------------------------------------------------------------------\n");
    printf("  Circular FIFO Queue Pointer Status:\n");
    printf("    - FRONT Pointer Index       : %d\n", cq_get_front(&waitingQueue));
    printf("    - REAR Pointer Index        : %d\n", cq_get_rear(&waitingQueue));
    printf("    - Queue Current Count       : %d\n", waitingCount);
    printf("    - Queue Maximum Capacity    : %d\n", waitingQueue.max);
    printf("    - Circular Wrap-Around?     : %s\n", cq_is_wrapped(&waitingQueue) ? "ACTIVE (REAR < FRONT)" : "NO");
    printf("    - Queue Empty?              : %s\n", cq_is_empty(&waitingQueue) ? "YES" : "NO");
    printf("    - Queue Full?               : %s\n", cq_is_full(&waitingQueue) ? "YES" : "NO");
    printf("====================================================================\n");
}

/* Feature 11: Automated FIFO Demonstration */
static void run_fifo_demonstration(void) {
    printf("\n===============================================================================\n");
    printf("            AUTOMATED FIFO DEMONSTRATION: CIRCULAR QUEUE & ALLOCATION           \n");
    printf("===============================================================================\n");
    printf("This demonstration steps through the complete FIFO lifecycle:\n");
    printf(" 1. Configure a 2-room hostel (4 beds total).\n");
    printf(" 2. Register 4 students and allocate all 4 beds (filling hostel to 100%%).\n");
    printf(" 3. Register 3 extra students requesting accommodation (filling Waiting Queue).\n");
    printf(" 4. Inspect Circular Queue pointers (FRONT, REAR, elements).\n");
    printf(" 5. Vacate 1 bed -> observe automatic DEQUEUE and allocation to FRONT student.\n");
    printf(" 6. Verify updated FRONT pointer and bed occupancy.\n");
    printf("===============================================================================\n\n");

    /* Step 1: Initialize */
    student_init();
    room_init();
    cq_init(&waitingQueue);

    printf("[STEP 1] Configuring Hostel with 2 Rooms (2 beds each = 4 beds total)...\n");
    room_add(101, 2);
    room_add(102, 2);
    room_display_all();

    /* Step 2: Register 4 students & allocate */
    printf("\n[STEP 2] Registering 4 students and requesting accommodation...\n");
    int s1 = student_register("STU001", "Alice Smith", "1MS23CS001", "CSE", 2);
    int s2 = student_register("STU002", "Bob Johnson",  "1MS23CS002", "ECE", 2);
    int s3 = student_register("STU003", "Charlie Ray",  "1MS23CS003", "ISE", 1);
    int s4 = student_register("STU004", "Diana Prince", "1MS23CS004", "MECH", 3);

    int sIdxList[4] = {s1, s2, s3, s4};
    for (int i = 0; i < 4; i++) {
        int rIdx, bIdx;
        room_find_first_vacant(&rIdx, &bIdx);
        room_allocate_bed(rIdx, bIdx, sIdxList[i]);
        Student *s = student_get_by_index(sIdxList[i]);
        s->roomNumber = room_get_by_index(rIdx)->roomNumber;
        s->bedNumber = bIdx + 1;
        s->status = STATUS_ALLOCATED;
        printf(" -> Allocated '%s' to Room %d, Bed %d\n", s->name, s->roomNumber, s->bedNumber);
    }
    printf("\nHostel Bed Status after 4 allocations:\n");
    room_display_all();

    /* Step 3: Register 3 extra students -> All beds full, so they ENQUEUE */
    printf("\n[STEP 3] Registering 3 additional students when hostel is 100%% FULL...\n");
    int s5 = student_register("STU005", "Evan Wright",  "1MS23CS005", "CSE", 1);
    int s6 = student_register("STU006", "Fiona Gallagher", "1MS23CS006", "CIVIL", 2);
    int s7 = student_register("STU007", "George Clark", "1MS23CS007", "AIML", 1);

    printf("\nAccommodation requests for STU005, STU006, STU007:\n");
    cq_enqueue(&waitingQueue, s5);
    cq_enqueue(&waitingQueue, s6);
    cq_enqueue(&waitingQueue, s7);

    /* Step 4: Display Queue */
    printf("\n[STEP 4] Examining Circular Queue state with 3 waiting students:\n");
    cq_display(&waitingQueue);
    printf("Notice: FRONT points to index %d (Evan Wright), REAR points to index %d (George Clark).\n",
           cq_get_front(&waitingQueue), cq_get_rear(&waitingQueue));

    /* Step 5: Vacate Room 101, Bed 1 (held by Alice Smith) */
    printf("\n[STEP 5] Alice Smith (STU001) vacates Room 101, Bed 1...\n");
    Student *alice = student_get_by_index(s1);
    room_update_bed_status(101, 1, 0, -1);
    alice->status = STATUS_VACATED;
    alice->roomNumber = -1;
    alice->bedNumber = -1;
    printf("[VACATE SUCCESS] Room 101, Bed 1 is freed. Student 'Alice Smith' status set to VACATED.\n");

    printf("\nTriggering FIFO Dequeue for the newly freed bed...\n");
    int nextIdx = cq_dequeue(&waitingQueue);
    Student *nextStu = student_get_by_index(nextIdx);
    room_allocate_bed(0, 0, nextIdx); /* Room 101 is idx 0, Bed 1 is idx 0 */
    nextStu->roomNumber = 101;
    nextStu->bedNumber = 1;
    nextStu->status = STATUS_ALLOCATED;

    printf("\n>>> RESULT: Bed 101-1 automatically allocated to FIFO FRONT student: '%s' (%s)!\n",
           nextStu->name, nextStu->id);

    /* Step 6: Updated Queue & Rooms */
    printf("\n[STEP 6] Inspecting Updated Circular Queue and Room Occupancy:\n");
    cq_display(&waitingQueue);
    printf("Notice: FRONT has advanced to index %d (Fiona Gallagher). Evan Wright was served first!\n",
           cq_get_front(&waitingQueue));
    room_display_all();

    printf("\n===============================================================================\n");
    printf("                        DEMONSTRATION COMPLETED SUCCESSFULLY                   \n");
    printf("===============================================================================\n\n");
}

/* Feature 12: Circular Queue Wrap-Around Demonstration */
static void run_circular_wraparound_demo(void) {
    printf("\n===============================================================================\n");
    printf("         DEDICATED DEMONSTRATION: CIRCULAR QUEUE WRAP-AROUND IN C             \n");
    printf("===============================================================================\n");
    printf("This test demonstrates the circular nature of the array-based ring buffer:\n");
    printf("  1. Uses a circular queue of capacity MAX = 6.\n");
    printf("  2. Enqueues 6 elements -> REAR reaches the last array index (5).\n");
    printf("  3. Dequeues 3 elements -> FRONT advances from 0 -> 1 -> 2 -> 3.\n");
    printf("  4. Enqueues 2 new elements -> (REAR + 1) %% MAX wraps around to index 0 and 1!\n");
    printf("  5. Shows the wrap-around state where REAR (1) < FRONT (3).\n");
    printf("  6. Dequeues all elements in exact FIFO order, showing FRONT wrap-around.\n");
    printf("===============================================================================\n\n");

    student_init();
    CircularQueue demoQ;
    cq_init(&demoQ);
    demoQ.max = 6; /* Small capacity for crystal-clear visual wrap-around */

    /* Register test students */
    int st[8];
    char idBuf[16], nameBuf[32], usnBuf[20];
    for (int i = 0; i < 8; i++) {
        snprintf(idBuf, sizeof(idBuf), "WRAP%02d", i + 1);
        snprintf(nameBuf, sizeof(nameBuf), "Student_%c", 'A' + i);
        snprintf(usnBuf, sizeof(usnBuf), "1MS23CS%03d", 10 + i);
        st[i] = student_register(idBuf, nameBuf, usnBuf, "CSE", 1);
    }

    printf("--- Phase 1: Enqueue 6 elements to fill the queue to capacity (MAX=6) ---\n");
    for (int i = 0; i < 6; i++) {
        cq_enqueue(&demoQ, st[i]);
    }
    printf("\nState after 6 enqueues:\n");
    cq_display_array_slots(&demoQ, 6);

    printf("\n--- Phase 2: Dequeue 3 elements from FRONT ---\n");
    for (int i = 0; i < 3; i++) {
        cq_dequeue(&demoQ);
    }
    printf("\nState after 3 dequeues (FRONT advanced to 3, slots 0..2 are now available):\n");
    cq_display_array_slots(&demoQ, 6);

    printf("\n--- Phase 3: Enqueue 2 new elements (Triggering REAR Wrap-Around!) ---\n");
    printf("Inserting Student_G (WRAP07) and Student_H (WRAP08)...\n");
    cq_enqueue(&demoQ, st[6]);
    cq_enqueue(&demoQ, st[7]);

    printf("\nState after circular wrap-around enqueues:\n");
    cq_display_array_slots(&demoQ, 6);
    printf("Notice: FRONT = %d, REAR = %d. REAR has wrapped around to beginning!\n",
           demoQ.front, demoQ.rear);

    printf("\n--- Phase 4: Empty the queue (Demonstrating FRONT Wrap-Around) ---\n");
    while (!cq_is_empty(&demoQ)) {
        cq_dequeue(&demoQ);
    }
    printf("\nFinal Queue State after all dequeues:\n");
    cq_display(&demoQ);
    printf("===============================================================================\n");
    printf("             CIRCULAR WRAP-AROUND DEMONSTRATION COMPLETE                      \n");
    printf("===============================================================================\n\n");
}

/* Default sample data for interactive use */
static void load_default_sample_data(void) {
    /* Add initial rooms */
    room_add(101, 3);
    room_add(102, 2);
    room_add(201, 4);

    /* Add sample students */
    int s1 = student_register("STU101", "Aarav Sharma",   "1MS23CS001", "CSE", 2);
    int s2 = student_register("STU102", "Bhavna Patel",   "1MS23CS002", "ECE", 3);
    int s3 = student_register("STU103", "Chetan Kumar",   "1MS23CS003", "ISE", 1);
    int s4 = student_register("STU104", "Deepa Nair",     "1MS23CS004", "AIML", 2);
    int s5 = student_register("STU105", "Eshwar Reddy",   "1MS23CS005", "MECH", 4);

    /* Allocate initial beds */
    int rIdx, bIdx;
    if (room_find_first_vacant(&rIdx, &bIdx)) {
        room_allocate_bed(rIdx, bIdx, s1);
        Student *s = student_get_by_index(s1);
        s->roomNumber = room_get_by_index(rIdx)->roomNumber;
        s->bedNumber = bIdx + 1;
        s->status = STATUS_ALLOCATED;
    }
    if (room_find_first_vacant(&rIdx, &bIdx)) {
        room_allocate_bed(rIdx, bIdx, s2);
        Student *s = student_get_by_index(s2);
        s->roomNumber = room_get_by_index(rIdx)->roomNumber;
        s->bedNumber = bIdx + 1;
        s->status = STATUS_ALLOCATED;
    }
    if (room_find_first_vacant(&rIdx, &bIdx)) {
        room_allocate_bed(rIdx, bIdx, s3);
        Student *s = student_get_by_index(s3);
        s->roomNumber = room_get_by_index(rIdx)->roomNumber;
        s->bedNumber = bIdx + 1;
        s->status = STATUS_ALLOCATED;
    }
    (void)s4;
    (void)s5;
}

static void print_main_menu(void) {
    printf("\n====================================================================\n");
    printf("                    HOSTEL ROOM ALLOCATION SYSTEM                   \n");
    printf("====================================================================\n");
    printf("  1. Register Student\n");
    printf("  2. Display All Students\n");
    printf("  3. Search Student (by ID or USN)\n");
    printf("  4. Add Hostel Room\n");
    printf("  5. Display All Rooms\n");
    printf("  6. Display Available Beds\n");
    printf("  7. Request Hostel Accommodation (Strict FIFO Fairness)\n");
    printf("  8. Display FIFO Waiting Queue (with Slot Map & Pointers)\n");
    printf("  9. Vacate Room\n");
    printf(" 10. Display Hostel Statistics & Report\n");
    printf(" 11. Run FIFO Demonstration Mode\n");
    printf(" 12. Run Circular Queue Wrap-Around Demonstration\n");
    printf("  0. Exit System\n");
    printf("====================================================================\n");
}

int main(int argc, char *argv[]) {
    /* Initialize subsystems */
    student_init();
    room_init();
    cq_init(&waitingQueue);

    /* Command-line automated flags */
    if (argc > 1) {
        if (strcmp(argv[1], "--demo") == 0 || strcmp(argv[1], "-d") == 0) {
            run_fifo_demonstration();
            return 0;
        }
        if (strcmp(argv[1], "--wrap-demo") == 0 || strcmp(argv[1], "-w") == 0) {
            run_circular_wraparound_demo();
            return 0;
        }
    }

    /* Load initial demo rooms and students */
    load_default_sample_data();

    printf("\n====================================================================\n");
    printf("               Welcome to Hostel Room Allocation System             \n");
    printf("         Campus Residence & Bed Allotment Management Portal         \n");
    printf("====================================================================\n");

    int running = 1;
    while (running) {
        print_main_menu();
        int choice = read_int("Enter your choice (0 - 12): ", 0, 12);

        switch (choice) {
            case 1:
                handle_register_student();
                break;
            case 2:
                handle_display_all_students();
                break;
            case 3:
                handle_search_student();
                break;
            case 4:
                handle_add_room();
                break;
            case 5:
                handle_display_all_rooms();
                break;
            case 6:
                handle_display_available_beds();
                break;
            case 7:
                handle_request_accommodation();
                break;
            case 8:
                handle_display_queue();
                break;
            case 9:
                handle_vacate_room();
                break;
            case 10:
                handle_hostel_statistics();
                break;
            case 11:
                run_fifo_demonstration();
                break;
            case 12:
                run_circular_wraparound_demo();
                break;
            case 0:
                printf("\nExiting Smart Hostel System. Thank you!\n");
                running = 0;
                break;
            default:
                printf("\n[ERROR] Invalid option selected.\n");
                break;
        }
    }

    return 0;
}
