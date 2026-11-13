#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "student.h"
#include "room.h"
#include "queue.h"

static int tests_passed = 0;
static int tests_total = 0;

#define TEST_ASSERT(cond, msg) do { \
    tests_total++; \
    if (cond) { \
        tests_passed++; \
        printf("  [PASS] %s\n", msg); \
    } else { \
        printf("  [FAIL] %s (Line %d)\n", msg, __LINE__); \
    } \
} while (0)

static void test_student_management(void) {
    printf("\n=== TEST SUITE 1: STUDENT MANAGEMENT & VALIDATION ===\n");
    student_init();

    int idx1 = student_register("STU001", "Alice Smith", "1MS23CS001", "CSE", 2);
    TEST_ASSERT(idx1 == 0, "First student registered at index 0");
    TEST_ASSERT(student_get_count() == 1, "Student count is 1");

    /* Duplicate ID check */
    int dupId = student_register("STU001", "Fake Alice", "1MS23CS999", "CSE", 2);
    TEST_ASSERT(dupId == -2, "Duplicate Student ID 'STU001' correctly rejected");

    /* Duplicate USN check */
    int dupUsn = student_register("STU002", "Bob Johnson", "1MS23CS001", "ECE", 1);
    TEST_ASSERT(dupUsn == -3, "Duplicate USN '1MS23CS001' correctly rejected");

    /* Valid second student */
    int idx2 = student_register("STU002", "Bob Johnson", "1MS23CS002", "ECE", 1);
    TEST_ASSERT(idx2 == 1, "Second student registered at index 1");
    TEST_ASSERT(student_get_count() == 2, "Student count is 2");

    /* Search by ID and USN */
    TEST_ASSERT(student_find_by_id("STU001") == 0, "Found student by ID STU001");
    TEST_ASSERT(student_find_by_usn("1MS23CS002") == 1, "Found student by USN 1MS23CS002");
    TEST_ASSERT(student_find_by_id("NONEXISTENT") == -1, "Search for non-existent ID returns -1");
}

static void test_room_management(void) {
    printf("\n=== TEST SUITE 2: ROOM MANAGEMENT & CAPACITY RULES ===\n");
    room_init();

    /* Add room with valid capacity (1..4) */
    int r1 = room_add(101, 2);
    int r2 = room_add(102, 4);
    TEST_ASSERT(r1 >= 0 && r2 >= 0, "Rooms 101 (cap 2) and 102 (cap 4) added");
    TEST_ASSERT(room_get_count() == 2, "Total rooms is 2");
    TEST_ASSERT(room_get_total_capacity() == 6, "Total bed capacity is 6");
    TEST_ASSERT(room_get_total_vacant() == 6, "All 6 beds initially vacant");

    /* Reject invalid capacity (> 4 or < 1) */
    int invalidCapHigh = room_add(103, 5);
    int invalidCapZero = room_add(104, 0);
    TEST_ASSERT(invalidCapHigh == -3, "Capacity > 4 rejected");
    TEST_ASSERT(invalidCapZero == -3, "Capacity < 1 rejected");

    /* Reject duplicate room */
    int dupRoom = room_add(101, 3);
    TEST_ASSERT(dupRoom == -4, "Duplicate room 101 rejected");
}

static void test_circular_queue(void) {
    printf("\n=== TEST SUITE 3: CIRCULAR FIFO QUEUE OPERATIONS ===\n");
    CircularQueue q;
    cq_init(&q);

    TEST_ASSERT(cq_is_empty(&q) == 1, "Queue initialized to empty");
    TEST_ASSERT(cq_is_full(&q) == 0, "Queue is not full");
    TEST_ASSERT(cq_get_front(&q) == -1 && cq_get_rear(&q) == -1, "FRONT and REAR are -1");

    /* Enqueue first element */
    cq_enqueue(&q, 10);
    TEST_ASSERT(cq_get_front(&q) == 0 && cq_get_rear(&q) == 0, "After 1st enqueue: FRONT=0, REAR=0");
    TEST_ASSERT(cq_peek(&q) == 10, "cq_peek() returns 10");
    TEST_ASSERT(cq_get_count(&q) == 1, "Queue count is 1");

    /* Enqueue more elements */
    cq_enqueue(&q, 20);
    cq_enqueue(&q, 30);
    TEST_ASSERT(cq_get_front(&q) == 0 && cq_get_rear(&q) == 2, "After 3 enqueues: FRONT=0, REAR=2");
    TEST_ASSERT(cq_get_count(&q) == 3, "Queue count is 3");

    /* Dequeue maintains strict FIFO order */
    int item1 = cq_dequeue(&q);
    TEST_ASSERT(item1 == 10, "First dequeued item is 10 (FIFO)");
    TEST_ASSERT(cq_get_front(&q) == 1, "FRONT advanced to 1");

    int item2 = cq_dequeue(&q);
    TEST_ASSERT(item2 == 20, "Second dequeued item is 20 (FIFO)");
    TEST_ASSERT(cq_get_front(&q) == 2, "FRONT advanced to 2");

    int item3 = cq_dequeue(&q);
    TEST_ASSERT(item3 == 30, "Third dequeued item is 30 (FIFO)");
    TEST_ASSERT(cq_is_empty(&q) == 1, "Queue is now empty");
    TEST_ASSERT(cq_get_front(&q) == -1 && cq_get_rear(&q) == -1, "FRONT and REAR reset to -1");

    /* Underflow test */
    int underflow = cq_dequeue(&q);
    TEST_ASSERT(underflow == -1, "Dequeue from empty queue safely returns -1");
}

static void test_circular_wrap_around(void) {
    printf("\n=== TEST SUITE 4: CIRCULAR QUEUE WRAP-AROUND ===\n");
    CircularQueue q;
    cq_init(&q);

    /* Fill up to MAX_QUEUE */
    for (int i = 0; i < MAX_QUEUE; i++) {
        cq_enqueue(&q, i);
    }
    TEST_ASSERT(cq_is_full(&q) == 1, "Queue is full after MAX_QUEUE enqueues");
    TEST_ASSERT(cq_enqueue(&q, 999) == -1, "Enqueue on full queue safely returns -1");

    /* Dequeue 5 elements to move FRONT forward */
    for (int i = 0; i < 5; i++) {
        int val = cq_dequeue(&q);
        assert(val == i);
    }
    TEST_ASSERT(cq_get_front(&q) == 5, "FRONT moved to index 5");
    TEST_ASSERT(cq_is_full(&q) == 0, "Queue is no longer full");

    /* Enqueue 5 more elements to trigger circular wrap-around to index 0..4 */
    for (int i = 0; i < 5; i++) {
        int res = cq_enqueue(&q, 100 + i);
        assert(res == 0);
    }
    TEST_ASSERT(cq_get_rear(&q) == 4, "REAR successfully wrapped around circularly to index 4");
    TEST_ASSERT(cq_is_wrapped(&q) == 1, "cq_is_wrapped() returns 1 (REAR < FRONT)");
    TEST_ASSERT(cq_is_full(&q) == 1, "Queue is full again with wrap-around");
}

static void test_fifo_hostel_allocation_and_vacate(void) {
    printf("\n=== TEST SUITE 5: END-TO-END FIFO ALLOCATION & VACATE ===\n");
    student_init();
    room_init();
    CircularQueue q;
    cq_init(&q);

    /* Setup 1 room with 2 beds */
    room_add(101, 2);

    /* Register 4 students */
    int s1 = student_register("S1", "Student One",   "USN01", "CSE", 1);
    int s2 = student_register("S2", "Student Two",   "USN02", "CSE", 1);
    int s3 = student_register("S3", "Student Three", "USN03", "CSE", 1);
    int s4 = student_register("S4", "Student Four",  "USN04", "CSE", 1);

    /* S1 requests: gets Bed 1 */
    int rIdx, bIdx;
    TEST_ASSERT(room_find_first_vacant(&rIdx, &bIdx) == 1, "Bed 1 found for S1");
    room_allocate_bed(rIdx, bIdx, s1);
    student_get_by_index(s1)->roomNumber = 101;
    student_get_by_index(s1)->bedNumber = bIdx + 1;
    student_get_by_index(s1)->status = STATUS_ALLOCATED;

    /* S2 requests: gets Bed 2 */
    TEST_ASSERT(room_find_first_vacant(&rIdx, &bIdx) == 1, "Bed 2 found for S2");
    room_allocate_bed(rIdx, bIdx, s2);
    student_get_by_index(s2)->roomNumber = 101;
    student_get_by_index(s2)->bedNumber = bIdx + 1;
    student_get_by_index(s2)->status = STATUS_ALLOCATED;

    /* Hostel is now completely full */
    TEST_ASSERT(room_find_first_vacant(&rIdx, &bIdx) == 0, "No vacant beds remaining in hostel");

    /* S3 requests: must be inserted into waiting queue */
    cq_enqueue(&q, s3);
    TEST_ASSERT(student_get_by_index(s3)->status == STATUS_WAITING, "S3 is WAITING in queue");
    TEST_ASSERT(cq_peek(&q) == s3, "S3 is at FRONT of waiting queue");

    /* S4 requests: must be inserted into waiting queue */
    cq_enqueue(&q, s4);
    TEST_ASSERT(student_get_by_index(s4)->status == STATUS_WAITING, "S4 is WAITING in queue");
    TEST_ASSERT(cq_get_count(&q) == 2, "Waiting queue has 2 students");

    /* Vacate Bed 1 (held by S1) */
    room_update_bed_status(101, 1, 0, -1);
    student_get_by_index(s1)->status = STATUS_VACATED;
    student_get_by_index(s1)->roomNumber = -1;
    student_get_by_index(s1)->bedNumber = -1;

    /* FIFO check: S3 (who entered queue first) must receive the freed bed */
    int nextIdx = cq_dequeue(&q);
    TEST_ASSERT(nextIdx == s3, "S3 dequeued first due to FIFO order");

    /* Allocate freed bed to S3 */
    room_allocate_bed(0, 0, nextIdx);
    student_get_by_index(nextIdx)->roomNumber = 101;
    student_get_by_index(nextIdx)->bedNumber = 1;
    student_get_by_index(nextIdx)->status = STATUS_ALLOCATED;

    TEST_ASSERT(student_get_by_index(s3)->status == STATUS_ALLOCATED, "S3 is now ALLOCATED");
    TEST_ASSERT(student_get_by_index(s3)->roomNumber == 101, "S3 received Room 101");
    TEST_ASSERT(student_get_by_index(s3)->bedNumber == 1, "S3 received Bed 1");

    /* S4 must now be at FRONT of queue */
    TEST_ASSERT(cq_peek(&q) == s4, "S4 is now FRONT of waiting queue");
    TEST_ASSERT(cq_get_count(&q) == 1, "Waiting queue count is 1");
}

static void test_fifo_fairness_no_bypass(void) {
    printf("\n=== TEST SUITE 6: STRICT FIFO FAIRNESS (NO BYPASSING) ===\n");
    student_init();
    room_init();
    CircularQueue q;
    cq_init(&q);

    /* Fill a room */
    room_add(101, 1);
    int s1 = student_register("STU1", "Student One", "USN01", "CSE", 1);
    room_allocate_bed(0, 0, s1);
    student_get_by_index(s1)->status = STATUS_ALLOCATED;

    /* S2 waits */
    int s2 = student_register("STU2", "Student Two", "USN02", "CSE", 1);
    cq_enqueue(&q, s2);
    TEST_ASSERT(cq_get_count(&q) == 1, "S2 is in waiting queue");

    /* Now a new student S3 requests accommodation while S2 is already waiting */
    int s3 = student_register("STU3", "Student Three", "USN03", "CSE", 1);

    /* FIFO Rule: Even if a bed were somehow free, S3 MUST enter REAR of queue */
    cq_enqueue(&q, s3);
    TEST_ASSERT(cq_get_count(&q) == 2, "S3 enqueued at REAR");
    TEST_ASSERT(cq_peek(&q) == s2, "S2 remains at FRONT and is NOT bypassed by S3");

    /* When bed is vacated, FRONT student (S2) receives it, NOT S3 */
    room_update_bed_status(101, 1, 0, -1);
    int allocatedStudent = cq_dequeue(&q);
    TEST_ASSERT(allocatedStudent == s2, "S2 received bed first; FIFO fairness preserved");
    TEST_ASSERT(cq_peek(&q) == s3, "S3 is now next in line (FRONT)");
}

static void test_auto_allocation_after_adding_room(void) {
    printf("\n=== TEST SUITE 7: AUTO ALLOCATION AFTER ADDING A ROOM ===\n");
    student_init();
    room_init();
    CircularQueue q;
    cq_init(&q);

    /* 2 students are waiting in queue */
    int s1 = student_register("WAIT1", "Waiting One", "USN_W1", "CSE", 1);
    int s2 = student_register("WAIT2", "Waiting Two", "USN_W2", "CSE", 1);
    cq_enqueue(&q, s1);
    cq_enqueue(&q, s2);
    TEST_ASSERT(cq_get_count(&q) == 2, "2 students currently waiting");

    /* Administrator adds a new room 201 with 2 beds */
    int newRoomIdx = room_add(201, 2);
    TEST_ASSERT(newRoomIdx >= 0, "Room 201 added");

    /* Automatic Allocation logic: allocate available beds to waiting students in FIFO order */
    Room *r = room_get_by_index(newRoomIdx);
    for (int b = 0; b < r->capacity && !cq_is_empty(&q); b++) {
        if (r->bedStatus[b] == 0) {
            int stuIdx = cq_dequeue(&q);
            room_allocate_bed(newRoomIdx, b, stuIdx);
            Student *st = student_get_by_index(stuIdx);
            st->roomNumber = r->roomNumber;
            st->bedNumber = b + 1;
            st->status = STATUS_ALLOCATED;
        }
    }

    TEST_ASSERT(cq_is_empty(&q) == 1, "Waiting queue is now empty after auto-allocation");
    TEST_ASSERT(student_get_by_index(s1)->roomNumber == 201 && student_get_by_index(s1)->bedNumber == 1,
                "S1 automatically got Room 201 Bed 1");
    TEST_ASSERT(student_get_by_index(s2)->roomNumber == 201 && student_get_by_index(s2)->bedNumber == 2,
                "S2 automatically got Room 201 Bed 2");
    TEST_ASSERT(r->occupiedCount == 2, "Room 201 is now fully occupied");
}

int main(void) {
    printf("===============================================================\n");
    printf("     RUNNING UNIT & INTEGRATION TESTS FOR SMART HOSTEL C       \n");
    printf("===============================================================\n");

    test_student_management();
    test_room_management();
    test_circular_queue();
    test_circular_wrap_around();
    test_fifo_hostel_allocation_and_vacate();
    test_fifo_fairness_no_bypass();
    test_auto_allocation_after_adding_room();

    printf("\n===============================================================\n");
    printf("TEST RESULTS: %d / %d TESTS PASSED\n", tests_passed, tests_total);
    printf("===============================================================\n");

    return (tests_passed == tests_total) ? 0 : 1;
}
