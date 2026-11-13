#include <stdio.h>
#include <string.h>
#include "room.h"
#include "student.h"

/* Fixed-size array to store hostel rooms */
static Room room_records[MAX_ROOMS];
static int total_rooms = 0;

void room_init(void) {
    total_rooms = 0;
    for (int i = 0; i < MAX_ROOMS; i++) {
        room_records[i].roomNumber = 0;
        room_records[i].capacity = 0;
        room_records[i].occupiedCount = 0;
        for (int b = 0; b < MAX_BEDS_PER_ROOM; b++) {
            room_records[i].bedStatus[b] = 0;
            room_records[i].bedOwner[b] = -1;
        }
    }
}

int room_get_count(void) {
    return total_rooms;
}

Room* room_get_all(void) {
    return room_records;
}

Room* room_get_by_index(int idx) {
    if (idx < 0 || idx >= total_rooms) return NULL;
    return &room_records[idx];
}

int room_find_by_number(int roomNumber) {
    for (int i = 0; i < total_rooms; i++) {
        if (room_records[i].roomNumber == roomNumber) {
            return i;
        }
    }
    return -1;
}

int room_add(int roomNumber, int capacity) {
    if (total_rooms >= MAX_ROOMS) {
        printf("[ERROR] Cannot add room. Maximum room limit (%d) reached.\n", MAX_ROOMS);
        return -1;
    }

    if (roomNumber <= 0) {
        printf("[ERROR] Room number must be a positive integer.\n");
        return -2;
    }

    if (capacity < 1 || capacity > MAX_BEDS_PER_ROOM) {
        printf("[ERROR] Capacity must be between 1 and %d beds per room.\n", MAX_BEDS_PER_ROOM);
        return -3;
    }

    if (room_find_by_number(roomNumber) != -1) {
        printf("[ERROR] Room %d already exists! Duplicate room rejected.\n", roomNumber);
        return -4;
    }

    int idx = total_rooms;
    room_records[idx].roomNumber = roomNumber;
    room_records[idx].capacity = capacity;
    room_records[idx].occupiedCount = 0;
    for (int b = 0; b < MAX_BEDS_PER_ROOM; b++) {
        room_records[idx].bedStatus[b] = 0;
        room_records[idx].bedOwner[b] = -1;
    }

    total_rooms++;
    return idx;
}

void room_display_all(void) {
    if (total_rooms == 0) {
        printf("\nNo rooms currently configured in the hostel.\n");
        return;
    }

    printf("\n========================================================================================\n");
    printf("                                  ALL HOSTEL ROOMS                                      \n");
    printf("========================================================================================\n");
    printf("%-8s | %-10s | %-10s | %-8s | %-32s\n",
           "Room No", "Capacity", "Occupied", "Vacant", "Bed Layout [Bed No: Status]");
    printf("---------+------------+------------+----------+-----------------------------------------\n");

    for (int i = 0; i < total_rooms; i++) {
        Room *r = &room_records[i];
        int vacant = r->capacity - r->occupiedCount;
        printf("Room %-3d | %-10d | %-10d | %-8d | ",
               r->roomNumber, r->capacity, r->occupiedCount, vacant);

        for (int b = 0; b < r->capacity; b++) {
            if (r->bedStatus[b] == 1) {
                printf("[B%d: OCC] ", b + 1);
            } else {
                printf("[B%d: VAC] ", b + 1);
            }
        }
        printf("\n");
    }
    printf("========================================================================================\n");
    printf("Total Rooms: %d | Total Beds: %d | Occupied: %d | Available: %d\n",
           total_rooms, room_get_total_capacity(), room_get_total_occupied(), room_get_total_vacant());
}

void room_display_vacant_beds(void) {
    if (total_rooms == 0) {
        printf("\nNo rooms configured in the hostel.\n");
        return;
    }

    int totalVacant = 0;
    printf("\n====================================================================\n");
    printf("                      LIST OF AVAILABLE / VACANT BEDS               \n");
    printf("====================================================================\n");
    printf("%-10s | %-10s | %-15s | %-20s\n", "Room No", "Bed No", "Status", "Remarks");
    printf("-----------+------------+-----------------+-------------------------\n");

    for (int i = 0; i < total_rooms; i++) {
        Room *r = &room_records[i];
        for (int b = 0; b < r->capacity; b++) {
            if (r->bedStatus[b] == 0) {
                printf("Room %-5d | Bed %-6d | %-15s | Ready for allocation\n",
                       r->roomNumber, b + 1, "VACANT");
                totalVacant++;
            }
        }
    }

    if (totalVacant == 0) {
        printf(">> All beds are currently occupied! No vacant beds available.\n");
    }
    printf("====================================================================\n");
    printf("Total Available Vacant Beds: %d\n", totalVacant);
}

void room_display_occupied_beds(void) {
    if (total_rooms == 0) {
        printf("\nNo rooms configured in the hostel.\n");
        return;
    }

    int totalOcc = 0;
    printf("\n========================================================================================\n");
    printf("                               LIST OF OCCUPIED BEDS                                    \n");
    printf("========================================================================================\n");
    printf("%-10s | %-8s | %-12s | %-20s | %-15s\n",
           "Room No", "Bed No", "Student ID", "Student Name", "USN");
    printf("-----------+----------+--------------+----------------------+---------------------------\n");

    for (int i = 0; i < total_rooms; i++) {
        Room *r = &room_records[i];
        for (int b = 0; b < r->capacity; b++) {
            if (r->bedStatus[b] == 1) {
                int sIdx = r->bedOwner[b];
                Student *s = student_get_by_index(sIdx);
                if (s) {
                    printf("Room %-5d | Bed %-4d | %-12s | %-20.20s | %-15s\n",
                           r->roomNumber, b + 1, s->id, s->name, s->usn);
                } else {
                    printf("Room %-5d | Bed %-4d | %-12s | %-20s | %-15s\n",
                           r->roomNumber, b + 1, "UNKNOWN", "N/A", "N/A");
                }
                totalOcc++;
            }
        }
    }

    if (totalOcc == 0) {
        printf(">> No beds are currently occupied.\n");
    }
    printf("========================================================================================\n");
    printf("Total Occupied Beds: %d\n", totalOcc);
}

void room_search_and_display(int roomNumber) {
    int idx = room_find_by_number(roomNumber);
    if (idx == -1) {
        printf("[ERROR] Room %d was not found in the hostel.\n", roomNumber);
        return;
    }

    Room *r = &room_records[idx];
    printf("\n+--------------------------------------------------------------+\n");
    printf("| Room Details: Room %-41d |\n", r->roomNumber);
    printf("+--------------------------------------------------------------+\n");
    printf("| Capacity       : %-43d |\n", r->capacity);
    printf("| Occupied Beds  : %-43d |\n", r->occupiedCount);
    printf("| Vacant Beds    : %-43d |\n", r->capacity - r->occupiedCount);
    printf("+--------------------------------------------------------------+\n");
    printf("| Bed Breakdown:                                               |\n");
    for (int b = 0; b < r->capacity; b++) {
        if (r->bedStatus[b] == 1) {
            Student *s = student_get_by_index(r->bedOwner[b]);
            char occupant[128];
            if (s) {
                snprintf(occupant, sizeof(occupant), "OCCUPIED by %s (%s)", s->name, s->id);
            } else {
                snprintf(occupant, sizeof(occupant), "OCCUPIED (Owner idx: %d)", r->bedOwner[b]);
            }
            printf("|   Bed %d: %-51s |\n", b + 1, occupant);
        } else {
            printf("|   Bed %d: %-51s |\n", b + 1, "VACANT");
        }
    }
    printf("+--------------------------------------------------------------+\n");
}

int room_find_first_vacant(int *outRoomIdx, int *outBedIdx) {
    for (int r = 0; r < total_rooms; r++) {
        for (int b = 0; b < room_records[r].capacity; b++) {
            if (room_records[r].bedStatus[b] == 0) {
                if (outRoomIdx) *outRoomIdx = r;
                if (outBedIdx) *outBedIdx = b;
                return 1; /* Found vacant bed */
            }
        }
    }
    return 0; /* Hostel is completely full */
}

int room_allocate_bed(int roomIdx, int bedIdx, int studentIdx) {
    if (roomIdx < 0 || roomIdx >= total_rooms) return -1;
    Room *r = &room_records[roomIdx];

    if (bedIdx < 0 || bedIdx >= r->capacity) return -2;
    if (r->bedStatus[bedIdx] != 0) return -3; /* Already occupied */

    r->bedStatus[bedIdx] = 1;
    r->bedOwner[bedIdx] = studentIdx;
    r->occupiedCount++;
    return 0;
}

int room_vacate_by_student(int studentIdx, int *outRoomNumber, int *outBedNumber) {
    for (int r = 0; r < total_rooms; r++) {
        for (int b = 0; b < room_records[r].capacity; b++) {
            if (room_records[r].bedStatus[b] == 1 && room_records[r].bedOwner[b] == studentIdx) {
                room_records[r].bedStatus[b] = 0;
                room_records[r].bedOwner[b] = -1;
                room_records[r].occupiedCount--;
                if (outRoomNumber) *outRoomNumber = room_records[r].roomNumber;
                if (outBedNumber) *outBedNumber = b + 1; /* 1-based bed number */
                return 0; /* Successfully vacated */
            }
        }
    }
    return -1; /* Student was not occupying any bed */
}

int room_update_bed_status(int roomNumber, int bedNumber, int newStatus, int studentIdx) {
    int rIdx = room_find_by_number(roomNumber);
    if (rIdx == -1) return -1;

    Room *r = &room_records[rIdx];
    int bIdx = bedNumber - 1; /* Convert 1-based to 0-based */
    if (bIdx < 0 || bIdx >= r->capacity) return -2;

    if (newStatus == 0) { /* Vacate */
        if (r->bedStatus[bIdx] == 1) {
            r->bedStatus[bIdx] = 0;
            r->bedOwner[bIdx] = -1;
            r->occupiedCount--;
        }
    } else { /* Occupy */
        if (r->bedStatus[bIdx] == 0) {
            r->bedStatus[bIdx] = 1;
            r->bedOwner[bIdx] = studentIdx;
            r->occupiedCount++;
        }
    }
    return 0;
}

int room_get_total_capacity(void) {
    int cap = 0;
    for (int i = 0; i < total_rooms; i++) {
        cap += room_records[i].capacity;
    }
    return cap;
}

int room_get_total_occupied(void) {
    int occ = 0;
    for (int i = 0; i < total_rooms; i++) {
        occ += room_records[i].occupiedCount;
    }
    return occ;
}

int room_get_total_vacant(void) {
    return room_get_total_capacity() - room_get_total_occupied();
}
