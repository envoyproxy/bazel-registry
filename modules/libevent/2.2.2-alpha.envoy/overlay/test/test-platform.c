#include <event2/event.h>
#include <event2/thread.h>
#include <event2/util.h>

#include <stdio.h>
#include <string.h>

static void on_event(evutil_socket_t fd, short events, void *arg) {
  (void)fd;
  (void)events;
  ++*(int *)arg;
}

static int test_backend(void) {
  struct event_config *config = event_config_new();
  struct event_base *base = NULL;
  struct event *event = NULL;
  const char *expected_method = NULL;
  int calls = 0;
  int pass = 0;

  if (config == NULL) {
    fprintf(stderr, "FAIL: event_config_new\n");
    return 0;
  }
  if (event_config_set_flag(config, EVENT_BASE_FLAG_IGNORE_ENV) != 0) {
    goto done;
  }
#ifdef _WIN32
  // Envoy excludes win32 to select wepoll. The default alone can hide a missing
  // backend.
  if (event_config_avoid_method(config, "win32") != 0) {
    goto done;
  }
  expected_method = "wepoll";
#elif defined(__APPLE__)
  expected_method = "kqueue";
#elif defined(__linux__)
  expected_method = "epoll";
#endif

  base = event_base_new_with_config(config);
  if (base == NULL) {
    fprintf(stderr, "FAIL: event_base_new_with_config\n");
    goto done;
  }
  if (expected_method != NULL &&
      strcmp(event_base_get_method(base), expected_method) != 0) {
    fprintf(stderr, "FAIL: expected %s backend, got %s\n", expected_method,
            event_base_get_method(base));
    goto done;
  }
  event = event_new(base, -1, 0, on_event, &calls);
  if (event == NULL) {
    goto done;
  }
  event_active(event, EV_TIMEOUT, 1);
  pass = event_base_loop(base, EVLOOP_NONBLOCK) >= 0 && calls == 1;
  if (!pass) {
    fprintf(stderr, "FAIL: backend did not dispatch the active event\n");
  }

done:
  if (event != NULL) {
    event_free(event);
  }
  if (base != NULL) {
    event_base_free(base);
  }
  event_config_free(config);
  return pass;
}

#ifdef __APPLE__
static int test_socketpair(void) {
  evutil_socket_t sockets[2];
  struct sockaddr_storage address;
  ev_socklen_t length = sizeof(address);
  int pass;

  if (evutil_socketpair(AF_UNIX, SOCK_STREAM, 0, sockets) != 0) {
    fprintf(stderr, "FAIL: evutil_socketpair\n");
    return 0;
  }
  // Missing HAVE_SOCKETPAIR silently substitutes a TCP pair for a native Unix
  // pair.
  pass = getsockname(sockets[0], (struct sockaddr *)&address, &length) == 0 &&
         address.ss_family == AF_UNIX;
  evutil_closesocket(sockets[0]);
  evutil_closesocket(sockets[1]);
  if (!pass) {
    fprintf(stderr, "FAIL: evutil_socketpair did not create Unix sockets\n");
  }
  return pass;
}
#endif

int main(void) {
  int pass;
#ifdef _WIN32
  WSADATA data;
  if (WSAStartup(MAKEWORD(2, 2), &data) != 0) {
    return 1;
  }
  if (evthread_use_windows_threads() != 0) {
    WSACleanup();
    return 1;
  }
#else
  if (evthread_use_pthreads() != 0) {
    return 1;
  }
#endif

  pass = test_backend();
#ifdef __APPLE__
  if (!test_socketpair()) {
    pass = 0;
  }
#endif
  libevent_global_shutdown();
#ifdef _WIN32
  WSACleanup();
#endif
  return pass ? 0 : 1;
}
