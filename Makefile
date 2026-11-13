CC = gcc
CFLAGS = -Wall -Wextra -std=c11

SRCS = main.c student.c room.c queue.c
OBJS = $(SRCS:.c=.o)
TARGET = hostel.exe

TEST_SRCS = tests/test_fifo.c student.c room.c queue.c
TEST_TARGET = test_fifo.exe

all: $(TARGET) $(TEST_TARGET)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $(SRCS) -o $(TARGET)

$(TEST_TARGET): $(TEST_SRCS)
	$(CC) $(CFLAGS) -I. $(TEST_SRCS) -o $(TEST_TARGET)

test: $(TEST_TARGET)
	./$(TEST_TARGET)

clean:
	cmd /c "del /f /q $(TARGET) $(TEST_TARGET) *.o 2>nul || exit 0"

.PHONY: all test clean
