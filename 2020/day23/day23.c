#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define CUPS_TEST 389125467
#define CUPS_INPUT 167248359
#define CUPS_LEN 1000000

char* print_list(int *l, int len)
{
	char *buf = malloc(len * 3 + 3);
	int offset = 0;
	offset += sprintf(buf+offset, "[");
	for (int i = 0; i < len; i++)
	{
		offset += sprintf(buf+offset, "%d, ", l[i]);
	}
	offset += sprintf(buf+offset - 2, "]\n");
	return buf;
}

int find_index(int *l, int target, int len)
{
	int i = 0;
	while (l[i] != target && i < len) i++;

	if (i == len)
	{
		return -1;
	}
	else
	{
		return i;
	}
}

static int cup_buffer[2][CUPS_LEN];
int main(void)
{
	int seed = CUPS_INPUT;
	int cup_buffer_idx = 0;
	int *cups = cup_buffer[cup_buffer_idx];
	int idx = 0;

	for (int i = 0; i < CUPS_LEN; i++)
	{
		cups[i] = i + 1;
	}

	while (seed > 0)
	{
	    cups[9 - ++idx] = seed % 10;
	    seed /= 10;
	}

	int current_cup = cups[0];
	for (int i = 0; i < 10000000; i++)
	{
		if ((i % 10000) == 0)
		{
			printf("%d\n", i);
		}
		//printf("cups: %s", print_list(cups, CUPS_LEN));
		//printf("current cup: %d\n", current_cup);

		int current_cup_idx = find_index(cups, current_cup, CUPS_LEN);
		int picked_up_cups[3];
		for (int x = 0; x < 3; x++)
		{
			int pick_up_cup_idx = (current_cup_idx + 1) % CUPS_LEN;
			picked_up_cups[x] = cups[(pick_up_cup_idx + x) % CUPS_LEN];
		}
		//printf("okay i picked up: %s", print_list(picked_up_cups, 3));

		int destination_cup = (current_cup - 1) % CUPS_LEN;
		if (destination_cup == 0) destination_cup = CUPS_LEN;
		while (find_index(picked_up_cups, destination_cup, 3) >= 0)
		{
			destination_cup = (destination_cup - 1) % CUPS_LEN;
			if (destination_cup == 0) destination_cup = CUPS_LEN;
		}
		//printf("destination cup: %d\n", destination_cup);
		int destination_cup_idx = find_index(cups, destination_cup, CUPS_LEN);

		int cup_buffer_idx_next = cup_buffer_idx ^ 1;
			idx = 0;
			int *cups_next = cup_buffer[cup_buffer_idx_next];
/*
		printf("okay, fill part 1: from current_cup_idx (%d), skipping %d-%d, to destination_cup_idx (%d).\n",
				current_cup_idx,
				(current_cup_idx + 1) % CUPS_LEN,
				(current_cup_idx + 3) % CUPS_LEN,
				destination_cup_idx);
*/
		cups_next[idx++] = cups[current_cup_idx];
		for (int j = (current_cup_idx + 4) % CUPS_LEN; j != destination_cup_idx; j = (j + 1) % CUPS_LEN)
		{
			cups_next[idx++] = cups[j];
		}
		cups_next[idx++] = cups[destination_cup_idx];
		//printf("okay after stage one, cups_next: %s", print_list(cups_next, 5));

		for (int j = 0; j < 3; j++)
		{
			cups_next[idx++] = picked_up_cups[j];
		}
		//printf("okay after stage two, cups_next: %s", print_list(cups_next, 5));

		int wrapup_copy_idx = (destination_cup_idx + 1) % CUPS_LEN;
		while (wrapup_copy_idx != current_cup_idx)
		{
			cups_next[idx++] = cups[wrapup_copy_idx];
			wrapup_copy_idx = (wrapup_copy_idx + 1) % CUPS_LEN;
		}
		//printf("okay after stage three, cups_next: %s\n", print_list(cups_next, CUPS_LEN));

		cup_buffer_idx = cup_buffer_idx_next;
		cups = cup_buffer[cup_buffer_idx];
		current_cup = cups[1];
	}
	//printf("okay cups: %s\n", print_list(cups, CUPS_LEN));
	int cup_1_index = find_index(cups, 1, CUPS_LEN);
	int64_t answer1 = cups[(cup_1_index + 1) % CUPS_LEN];
	int64_t answer2 = cups[(cup_1_index + 2) % CUPS_LEN];
	int64_t answer = answer1 * answer2;
	printf("answer = %lld * %lld = %lld\n", answer1, answer2, answer);

	return 0;
}
