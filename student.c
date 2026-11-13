#include <stdio.h>
#include <string.h>
#include "student.h"

/* Fixed-size array to store student records */
static Student student_records[MAX_STUDENTS];
static int total_students = 0;

void student_init(void) {
    total_students = 0;
    for (int i = 0; i < MAX_STUDENTS; i++) {
        student_records[i].id[0] = '\0';
        student_records[i].name[0] = '\0';
        student_records[i].usn[0] = '\0';
        student_records[i].department[0] = '\0';
        student_records[i].year = 0;
        student_records[i].roomNumber = -1;
        student_records[i].bedNumber = -1;
        student_records[i].status = STATUS_UNALLOCATED;
    }
}

int student_get_count(void) {
    return total_students;
}

Student* student_get_all(void) {
    return student_records;
}

Student* student_get_by_index(int idx) {
    if (idx < 0 || idx >= total_students) {
        return NULL;
    }
    return &student_records[idx];
}

int student_find_by_id(const char *id) {
    if (!id || id[0] == '\0') return -1;
    for (int i = 0; i < total_students; i++) {
        if (strcmp(student_records[i].id, id) == 0) {
            return i;
        }
    }
    return -1;
}

int student_find_by_usn(const char *usn) {
    if (!usn || usn[0] == '\0') return -1;
    for (int i = 0; i < total_students; i++) {
        if (strcmp(student_records[i].usn, usn) == 0) {
            return i;
        }
    }
    return -1;
}

int student_register(const char *id, const char *name, const char *usn, const char *dept, int year) {
    if (total_students >= MAX_STUDENTS) {
        printf("[ERROR] Student database is full! Maximum limit (%d) reached.\n", MAX_STUDENTS);
        return -1;
    }

    if (!id || id[0] == '\0' || !name || name[0] == '\0' || !usn || usn[0] == '\0') {
        printf("[ERROR] Student ID, Name, and USN cannot be empty.\n");
        return -1;
    }

    /* Check duplicate ID */
    if (student_find_by_id(id) != -1) {
        printf("[ERROR] Duplicate Student ID '%s'! Registration rejected.\n", id);
        return -2;
    }

    /* Check duplicate USN */
    if (student_find_by_usn(usn) != -1) {
        printf("[ERROR] Duplicate USN '%s'! Registration rejected.\n", usn);
        return -3;
    }

    /* Store record at the next available array index */
    int idx = total_students;
    strncpy(student_records[idx].id, id, ID_LEN - 1);
    student_records[idx].id[ID_LEN - 1] = '\0';

    strncpy(student_records[idx].name, name, NAME_LEN - 1);
    student_records[idx].name[NAME_LEN - 1] = '\0';

    strncpy(student_records[idx].usn, usn, USN_LEN - 1);
    student_records[idx].usn[USN_LEN - 1] = '\0';

    strncpy(student_records[idx].department, dept ? dept : "N/A", DEPT_LEN - 1);
    student_records[idx].department[DEPT_LEN - 1] = '\0';

    student_records[idx].year = year;
    student_records[idx].roomNumber = -1;
    student_records[idx].bedNumber = -1;
    student_records[idx].status = STATUS_UNALLOCATED;

    total_students++;
    return idx;
}

const char* student_status_to_string(AllocationStatus status) {
    switch (status) {
        case STATUS_UNALLOCATED: return "Unallocated";
        case STATUS_WAITING:     return "Waiting in FIFO Queue";
        case STATUS_ALLOCATED:   return "Allocated";
        case STATUS_VACATED:     return "Vacated";
        default:                 return "Unknown";
    }
}

void student_display_single(int idx) {
    if (idx < 0 || idx >= total_students) {
        printf("[ERROR] Invalid student index %d.\n", idx);
        return;
    }
    Student *s = &student_records[idx];
    printf("+--------------------------------------------------------------------------+\n");
    printf("| Student ID   : %-58s |\n", s->id);
    printf("| Student Name : %-58s |\n", s->name);
    printf("| USN          : %-58s |\n", s->usn);
    printf("| Department   : %-58s |\n", s->department);
    printf("| Year         : Year %-53d |\n", s->year);
    printf("| Status       : %-58s |\n", student_status_to_string(s->status));
    if (s->status == STATUS_ALLOCATED) {
        printf("| Room Number  : Room %-53d |\n", s->roomNumber);
        printf("| Bed Number   : Bed %-54d |\n", s->bedNumber);
    } else {
        printf("| Room Number  : %-58s |\n", "Not Allocated");
        printf("| Bed Number   : %-58s |\n", "Not Allocated");
    }
    printf("+--------------------------------------------------------------------------+\n");
}

void student_display_all(void) {
    if (total_students == 0) {
        printf("\nNo student records found in the system.\n");
        return;
    }

    printf("\n====================================================================================================\n");
    printf("                                       ALL REGISTERED STUDENTS                                      \n");
    printf("====================================================================================================\n");
    printf("%-4s | %-12s | %-20s | %-15s | %-6s | %-4s | %-16s | %-10s\n",
           "Idx", "Student ID", "Name", "USN", "Dept", "Year", "Status", "Room/Bed");
    printf("-----+--------------+----------------------+-----------------+--------+------+------------------+-----------\n");

    for (int i = 0; i < total_students; i++) {
        Student *s = &student_records[i];
        char roomBed[16];
        if (s->status == STATUS_ALLOCATED) {
            snprintf(roomBed, sizeof(roomBed), "R%d-B%d", s->roomNumber, s->bedNumber);
        } else {
            snprintf(roomBed, sizeof(roomBed), "--");
        }

        printf("%-4d | %-12s | %-20.20s | %-15s | %-6.6s | %-4d | %-16.16s | %-10s\n",
               i, s->id, s->name, s->usn, s->department, s->year,
               student_status_to_string(s->status), roomBed);
    }
    printf("====================================================================================================\n");
    printf("Total registered students: %d / %d\n", total_students, MAX_STUDENTS);
}
