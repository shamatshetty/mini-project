#ifndef STUDENT_H
#define STUDENT_H

#define MAX_STUDENTS 100
#define ID_LEN 16
#define NAME_LEN 64
#define USN_LEN 20
#define DEPT_LEN 32

/*
 * Allocation Status of a Student in the Hostel
 */
typedef enum {
    STATUS_UNALLOCATED = 0,  /* Registered, accommodation not yet requested */
    STATUS_WAITING,          /* Waiting in the Circular FIFO Queue */
    STATUS_ALLOCATED,        /* Room & Bed assigned */
    STATUS_VACATED           /* Vacated the hostel */
} AllocationStatus;

/*
 * Student Structure
 * Stores individual student details, academic info, and room allotment status.
 */
typedef struct {
    char id[ID_LEN];                 /* Unique Student ID e.g., "STU101" */
    char name[NAME_LEN];             /* Full Name */
    char usn[USN_LEN];               /* University Seat Number (Strictly Unique) */
    char department[DEPT_LEN];       /* Academic Department e.g., "CSE", "ECE" */
    int year;                        /* Academic Year (1, 2, 3, 4) */
    int roomNumber;                  /* Allocated Room Number (-1 if none) */
    int bedNumber;                   /* Allocated Bed Number 1..4 (-1 if none) */
    AllocationStatus status;         /* Current Allocation Status */
} Student;

/* Module Lifecycle */
void student_init(void);
int student_get_count(void);
Student* student_get_all(void);
Student* student_get_by_index(int idx);

/* Operations */
int student_find_by_id(const char *id);
int student_find_by_usn(const char *usn);
int student_register(const char *id, const char *name, const char *usn, const char *dept, int year);
void student_display_all(void);
void student_display_single(int idx);
const char* student_status_to_string(AllocationStatus status);

#endif /* STUDENT_H */
