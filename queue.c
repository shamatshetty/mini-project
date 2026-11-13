#include <stdio.h>
#include "queue.h"
#include "student.h"

/*
 * Initialize the circular queue to an empty state.
 * Both FRONT and REAR are set to -1.
 */
void cq_init(CircularQueue *q) {
    if (!q) return;
    q->front = -1;
    q->rear = -1;
    q->max = MAX_QUEUE;
    q->count = 0;
    for (int i = 0; i < MAX_QUEUE; i++) {
        q->items[i] = -1;
    }
}

/*
 * Returns 1 if circular queue is empty, 0 otherwise.
 */
int cq_is_empty(const CircularQueue *q) {
    if (!q) return 1;
    return (q->front == -1);
}

/*
 * Returns 1 if circular queue is full, 0 otherwise.
 * Full condition: (REAR + 1) % MAX == FRONT
 */
int cq_is_full(const CircularQueue *q) {
    if (!q) return 0;
    return ((q->rear + 1) % q->max == q->front);
}

int cq_get_count(const CircularQueue *q) {
    if (!q) return 0;
    return q->count;
}

int cq_get_front(const CircularQueue *q) {
    if (!q) return -1;
    return q->front;
}

int cq_get_rear(const CircularQueue *q) {
    if (!q) return -1;
    return q->rear;
}

/*
 * Returns 1 if REAR has circularly wrapped around past the end of the array (REAR < FRONT).
 */
int cq_is_wrapped(const CircularQueue *q) {
    if (!q || q->count == 0) return 0;
    return (q->rear < q->front);
}

/*
 * Insert a student array index into the circular queue.
 * FIFO Rule: Element is placed at (rear + 1) % MAX.
 * Tracks and reports previous and updated pointer positions.
 */
int cq_enqueue(CircularQueue *q, int studentIdx) {
    if (!q) return -1;

    if (cq_is_full(q)) {
        printf("[QUEUE ERROR] Waiting Queue is FULL! Cannot enqueue student index %d.\n", studentIdx);
        printf("              (FRONT=%d, REAR=%d, Current Count=%d, MAX=%d)\n",
               q->front, q->rear, q->count, q->max);
        return -1;
    }

    int oldFront = q->front;
    int oldRear = q->rear;
    int isWrapAround = 0;

    if (cq_is_empty(q)) {
        /* Queue was empty: first element placed at index 0 */
        q->front = 0;
        q->rear = 0;
    } else {
        /* Check if REAR wraps from end of array back to 0 */
        if (q->rear == q->max - 1) {
            isWrapAround = 1;
        }
        /* Circular increment */
        q->rear = (q->rear + 1) % q->max;
    }

    q->items[q->rear] = studentIdx;
    q->count++;

    Student *s = student_get_by_index(studentIdx);
    printf("--------------------------------------------------------------------\n");
    printf("[ENQUEUE OPERATION] Enqueued Student '%s' (%s)\n",
           s ? s->name : "N/A", s ? s->id : "N/A");
    printf("  Previous Pointers: FRONT = %-3d | REAR = %-3d\n", oldFront, oldRear);
    if (isWrapAround) {
        printf("  >>> [CIRCULAR WRAP-AROUND] REAR wrapped circularly from index %d -> 0! <<<\n", oldRear);
    }
    printf("  Updated Pointers : FRONT = %-3d | REAR = %-3d | Stored at items[%d]\n",
           q->front, q->rear, q->rear);
    printf("  Queue Total Size : %d / %d\n", q->count, q->max);
    printf("--------------------------------------------------------------------\n");

    if (s) {
        s->status = STATUS_WAITING;
    }

    return 0;
}

/*
 * Remove and return the student array index from the FRONT of the circular queue.
 * FIFO Rule: The element at FRONT is dequeued first.
 * Tracks and reports previous and updated pointer positions.
 */
int cq_dequeue(CircularQueue *q) {
    if (!q || cq_is_empty(q)) {
        printf("[QUEUE ERROR] Waiting Queue is EMPTY! Cannot dequeue.\n");
        return -1;
    }

    int studentIdx = q->items[q->front];
    int oldFront = q->front;
    int oldRear = q->rear;
    int isWrapAround = 0;

    /* Clear the slot */
    q->items[oldFront] = -1;

    if (q->front == q->rear) {
        /* Only one element was in the queue; reset to empty state */
        q->front = -1;
        q->rear = -1;
    } else {
        /* Check if FRONT wraps from end of array back to 0 */
        if (q->front == q->max - 1) {
            isWrapAround = 1;
        }
        /* Circular increment */
        q->front = (q->front + 1) % q->max;
    }

    q->count--;

    Student *s = student_get_by_index(studentIdx);
    printf("--------------------------------------------------------------------\n");
    printf("[DEQUEUE OPERATION] Dequeued Student '%s' (%s)\n",
           s ? s->name : "N/A", s ? s->id : "N/A");
    printf("  Previous Pointers: FRONT = %-3d | REAR = %-3d | Popped from items[%d]\n",
           oldFront, oldRear, oldFront);
    if (isWrapAround) {
        printf("  >>> [CIRCULAR WRAP-AROUND] FRONT wrapped circularly from index %d -> 0! <<<\n", oldFront);
    }
    printf("  Updated Pointers : FRONT = %-3d | REAR = %-3d\n", q->front, q->rear);
    printf("  Queue Total Size : %d / %d\n", q->count, q->max);
    printf("--------------------------------------------------------------------\n");

    return studentIdx;
}

/*
 * Inspect the FRONT element without removing it.
 */
int cq_peek(const CircularQueue *q) {
    if (!q || cq_is_empty(q)) {
        return -1;
    }
    return q->items[q->front];
}

/*
 * Displays a detailed map of all queue array slots to visualize the circular buffer.
 */
void cq_display_array_slots(const CircularQueue *q, int maxSlotsToShow) {
    if (!q) return;
    int limit = (maxSlotsToShow > 0 && maxSlotsToShow <= q->max) ? maxSlotsToShow : q->max;

    printf("\n--- Circular Queue Array Slot Map (Indexes 0 to %d) ---\n", limit - 1);
    printf("Idx  | Status   | Student ID   | Occupant Name        | Pointer Markers\n");
    printf("-----+----------+--------------+----------------------+---------------------\n");

    for (int i = 0; i < limit; i++) {
        int sIdx = q->items[i];
        int isOccupied = (sIdx != -1);
        Student *s = isOccupied ? student_get_by_index(sIdx) : NULL;

        char marker[32] = "";
        int isF = (i == q->front);
        int isR = (i == q->rear);

        if (isF && isR && q->count > 0) {
            snprintf(marker, sizeof(marker), "<== FRONT & REAR");
        } else if (isF && q->count > 0) {
            snprintf(marker, sizeof(marker), "<== FRONT");
        } else if (isR && q->count > 0) {
            snprintf(marker, sizeof(marker), "<== REAR");
        }

        if (isOccupied && s) {
            printf("[%02d] | OCCUPIED | %-12s | %-20.20s | %s\n",
                   i, s->id, s->name, marker);
        } else {
            printf("[%02d] | EMPTY    | %-12s | %-20s | %s\n",
                   i, "--", "--", marker);
        }
    }
    printf("----------------------------------------------------------------------------\n");
}

/*
 * Displays the entire circular FIFO queue with its internal array indices,
 * FRONT and REAR pointers, circular wrap-around indicator, and waiting students.
 */
void cq_display(const CircularQueue *q) {
    if (!q || cq_is_empty(q)) {
        printf("\n====================================================================\n");
        printf("                       FIFO WAITING QUEUE                           \n");
        printf("====================================================================\n");
        printf("Queue Status : EMPTY\n");
        printf("FRONT Pointer: %d | REAR Pointer: %d | MAX Capacity: %d | Waiting: 0\n",
               q ? q->front : -1, q ? q->rear : -1, q ? q->max : MAX_QUEUE);
        printf("====================================================================\n");
        return;
    }

    printf("\n========================================================================================\n");
    printf("                                   FIFO WAITING QUEUE                                   \n");
    printf("========================================================================================\n");
    printf("Queue Pointers -> FRONT: %d | REAR: %d | Total Waiting: %d | MAX Capacity: %d\n",
           q->front, q->rear, q->count, q->max);

    if (cq_is_wrapped(q)) {
        printf(">>> [CIRCULAR WRAP-AROUND ACTIVE]: REAR (%d) < FRONT (%d) - Array has looped back! <<<\n",
               q->rear, q->front);
    }

    printf("----------------------------------------------------------------------------------------\n");
    printf("%-5s | %-10s | %-12s | %-20s | %-15s | %-6s\n",
           "Pos", "Queue Idx", "Student ID", "Name", "USN", "Dept");
    printf("------+------------+--------------+----------------------+-----------------+--------\n");

    int pos = 1;
    int idx = q->front;
    while (1) {
        int studentIdx = q->items[idx];
        Student *s = student_get_by_index(studentIdx);

        char posMarker[16];
        if (idx == q->front && idx == q->rear) {
            snprintf(posMarker, sizeof(posMarker), "F & R");
        } else if (idx == q->front) {
            snprintf(posMarker, sizeof(posMarker), "FRONT");
        } else if (idx == q->rear) {
            snprintf(posMarker, sizeof(posMarker), "REAR");
        } else {
            snprintf(posMarker, sizeof(posMarker), "#%d", pos);
        }

        if (s) {
            printf("%-5s | [%2d]       | %-12s | %-20.20s | %-15s | %-6s\n",
                   posMarker, idx, s->id, s->name, s->usn, s->department);
        } else {
            printf("%-5s | [%2d]       | %-12s | %-20s | %-15s | %-6s\n",
                   posMarker, idx, "ERR_UNKNOWN", "Unknown", "N/A", "N/A");
        }

        if (idx == q->rear) {
            break; /* Reached end of circular queue */
        }
        idx = (idx + 1) % q->max;
        pos++;
    }
    printf("========================================================================================\n");
    printf("FIFO Principle: The student at FRONT will get the very next vacant bed.\n");

    /* Show array slot map for the first 16 slots or active range */
    int slotsToShow = (q->count > 0 && q->rear >= q->front) ? (q->rear + 3) : (q->max);
    if (slotsToShow < 8) slotsToShow = 8;
    if (slotsToShow > q->max) slotsToShow = q->max;
    cq_display_array_slots(q, slotsToShow);
}
