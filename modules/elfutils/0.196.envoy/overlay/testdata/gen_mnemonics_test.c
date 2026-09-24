#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#ifdef main
#undef main
#endif

int gen_mnemonics_tool_main(int argc, char **argv);

static const char kInput[] =
    "%%\n"
    "# duplicate mnemonics should collapse to one output line\n"
    "FIRST:FOO\n"
    "SECOND:FOO\n"
    "\n"
    "# INVALID entries are dropped\n"
    "THIRD:INVALID\n"
    "\n"
    "# brace-only expansions should be ignored without crashing\n"
    "FOURTH:{COND}\n"
    "\n"
    "FIFTH:BAR\n";

static const char kExpected[] =
    "MNE(BAR)\n"
    "MNE(FOO)\n";

static char *create_temp_path(void)
{
  const char *tmpdir = getenv("TEST_TMPDIR");
  if (tmpdir == NULL || tmpdir[0] == '\0')
    tmpdir = "/tmp";

  size_t len = strlen(tmpdir) + strlen("/gen_mnemonics_XXXXXX") + 1;
  char *path = malloc(len);
  if (path == NULL)
    {
      perror("malloc");
      exit(1);
    }

  snprintf(path, len, "%s/gen_mnemonics_XXXXXX", tmpdir);
  int fd = mkstemp(path);
  if (fd < 0)
    {
      perror("mkstemp");
      exit(1);
    }
  close(fd);
  unlink(path);
  return path;
}

static void write_file_or_die(const char *path, const char *contents)
{
  FILE *f = fopen(path, "wb");
  if (f == NULL)
    {
      perror("fopen");
      exit(1);
    }

  size_t len = strlen(contents);
  if (fwrite(contents, 1, len, f) != len)
    {
      fclose(f);
      perror("fwrite");
      exit(1);
    }

  if (fclose(f) != 0)
    {
      perror("fclose");
      exit(1);
    }
}

static char *read_file_or_die(const char *path)
{
  FILE *f = fopen(path, "rb");
  char *contents = NULL;
  if (f == NULL)
    {
      perror("fopen");
      exit(1);
    }

  if (fseek(f, 0, SEEK_END) != 0)
    {
      fclose(f);
      perror("fseek");
      exit(1);
    }

  long len = ftell(f);
  if (len < 0)
    {
      fclose(f);
      perror("ftell");
      exit(1);
    }

  if (fseek(f, 0, SEEK_SET) != 0)
    {
      fclose(f);
      perror("fseek");
      exit(1);
    }

  contents = malloc((size_t) len + 1);
  if (contents == NULL)
    {
      fclose(f);
      perror("malloc");
      exit(1);
    }

  if (fread(contents, 1, (size_t) len, f) != (size_t) len)
    {
      free(contents);
      fclose(f);
      perror("fread");
      exit(1);
    }
  contents[len] = '\0';

  if (fclose(f) != 0)
    {
      free(contents);
      perror("fclose");
      exit(1);
    }

  return contents;
}

int main(void)
{
  char *input_path = create_temp_path();
  char *output_path = create_temp_path();
  write_file_or_die(input_path, kInput);

  char *argv[] = {
      "gen_mnemonics_test",
      input_path,
      output_path,
      NULL,
  };
  if (gen_mnemonics_tool_main(3, argv) != 0)
    return 1;

  char *output = read_file_or_die(output_path);
  int ok = strcmp(output, kExpected) == 0;
  if (!ok)
    fprintf(stderr, "unexpected output:\n%s", output);

  free(output);
  unlink(input_path);
  unlink(output_path);
  free(input_path);
  free(output_path);
  return ok ? 0 : 1;
}
