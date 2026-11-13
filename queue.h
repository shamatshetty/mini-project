#ifndef QUEUE_H
#define QUEUE_H

#define MAX_QUEUE 50

/*
 * Circular FIFO Queue Structure
 * Implemented using a fixed-size integer array storing student indices.
 * Maintains FRONT, REAR, MAX capacity, and active count.
 */
typedef struct {
    int items[MAX_QUEUE];  /* Fixed-size integer array storing student array indices */
    int front;             /* Index of the front element (-1 when empty) */
    int rear;              /* Index of the rear element (-1 when empty) */
    int max;               /* Maximum capacity of the circular queue */
    int count;             /* Number of students currently in the queue */
} CircularQueue;

/* Queue Lifecycle */
void cq_init(CircularQueue *q);

/* Status Checking */
int cq_is_empty(const CircularQueue *q);
int cq_is_full(const CircularQueue *q);
int cq_get_count(const CircularQueue *q);
int cq_get_front(const CircularQueue *q);
int cq_get_rear(const CircularQueue *q);
int cq_is_wrapped(const CircularQueue *q);

/* Core Circular FIFO Operations with Pointer Tracking */
int cq_enqueue(CircularQueue *q, int studentIdx);
int cq_dequeue(CircularQueue *q);
int cq_peek(const CircularQueue *q);

/* Visualization & Display */
void cq_display(const CircularQueue *q);
void cq_display_array_slots(const CircularQueue *q, int maxSlotsToShow);

#endif /* QUEUE_H */
