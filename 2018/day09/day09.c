#include <stdio.h>

#define NUM_PLAYERS 423
#define MAX_MARBLE 7194400

struct sMarble
{
  int id;
  struct sMarble* prev;
  struct sMarble* next;
};

struct sMarble* current_pos;
int circle_size = 1;
unsigned int scores[NUM_PLAYERS];
struct sMarble circle[MAX_MARBLE + 1];

void circle_insert(int marble)
{
  struct sMarble* insert_pos = current_pos->next;

  circle[marble].id = marble;
  circle[marble].prev = insert_pos;
  circle[marble].next = insert_pos->next;
  insert_pos->next->prev = &circle[marble];
  insert_pos->next = &circle[marble];
  current_pos = &circle[marble];
  circle_size++;
}

int circle_remove()
{
  struct sMarble* remove_pos = current_pos->prev->prev->prev->prev->prev->prev->prev; // lol

  current_pos = remove_pos->next;
  remove_pos->prev->next = remove_pos->next;
  remove_pos->next->prev = remove_pos->prev;
  circle_size--;
  return remove_pos->id;
}

int main(int argc, char* argv[])
{
  current_pos = &circle[0];
  current_pos->id = 0;
  current_pos->prev = current_pos;
  current_pos->next = current_pos;

  for (int marble = 1; marble <= MAX_MARBLE; marble++) {
  if (0 == (marble % 23)) {
      scores[marble % NUM_PLAYERS] += marble;
      scores[marble % NUM_PLAYERS] += circle_remove();
    }
    else {
      circle_insert(marble);
    }
  }

  int max_score = 0;
  int max_player = 0;
  for (int player = 0; player < NUM_PLAYERS; player++) {
    if (scores[player] > max_score) {
      max_score = scores[player];
      max_player = player;
    }
  }
  printf("Player %d: %u\r\n", max_player + 1, max_score);


  return 0;
}
