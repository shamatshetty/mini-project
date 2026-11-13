#ifndef ROOM_H
#define ROOM_H

#define MAX_ROOMS 50
#define MAX_BEDS_PER_ROOM 4

/*
 * Room Structure
 * Manages room capacity and per-bed occupancy status.
 * Max 4 beds per room.
 */
typedef struct {
    int roomNumber;                           /* e.g., 101, 102 */
    int capacity;                             /* Bed capacity: 1 to MAX_BEDS_PER_ROOM */
    int occupiedCount;                        /* Number of beds currently occupied */
    int bedStatus[MAX_BEDS_PER_ROOM];         /* 0 = Vacant, 1 = Occupied */
    int bedOwner[MAX_BEDS_PER_ROOM];          /* Index into students[] array, -1 if vacant */
} Room;

/* Lifecycle */
void room_init(void);
int room_get_count(void);
Room* room_get_all(void);
Room* room_get_by_index(int idx);

/* Operations */
int room_add(int roomNumber, int capacity);
int room_find_by_number(int roomNumber);
void room_display_all(void);
void room_display_vacant_beds(void);
void room_display_occupied_beds(void);
void room_search_and_display(int roomNumber);

/* Bed Allocation / Deallocation */
int room_find_first_vacant(int *outRoomIdx, int *outBedIdx);
int room_allocate_bed(int roomIdx, int bedIdx, int studentIdx);
int room_vacate_by_student(int studentIdx, int *outRoomNumber, int *outBedNumber);
int room_update_bed_status(int roomNumber, int bedNumber, int newStatus, int studentIdx);

/* Aggregate Statistics */
int room_get_total_capacity(void);
int room_get_total_occupied(void);
int room_get_total_vacant(void);

#endif /* ROOM_H */
