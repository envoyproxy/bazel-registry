# libevent module maintainer notes

## Android config header regeneration

`/home/runner/work/bazel-registry/bazel-registry/modules/libevent/2.2.2-alpha.envoy/overlay/event2-config_android.h`
was generated from libevent `release-2.2.2-alpha` using:

- Android NDK: `r26d`
- Android API level: `23` (Envoy Mobile minimum SDK at time of generation)

Regenerate when libevent changes or when Envoy Mobile raises min SDK:

```bash
NDK=/path/to/android-ndk-r26d
cmake /path/to/libevent-release-2.2.2-alpha \
  -DCMAKE_TOOLCHAIN_FILE="$NDK/build/cmake/android.toolchain.cmake" \
  -DANDROID_ABI=x86_64 \
  -DANDROID_PLATFORM=android-23 \
  -DEVENT__DISABLE_TESTS=ON \
  -DEVENT__DISABLE_SAMPLES=ON \
  -DEVENT__DISABLE_BENCHMARK=ON
```

Then copy generated `include/event2/event-config.h` values into the Bazel overlay header in the same style as other platform config headers.

Preserve the handwritten byte-order block in
`event2-config_android.h` when regenerating it. That block is not
part of the cmake-generated output; it exists so libevent's `sha1.c`
has exactly one of `LITTLE_ENDIAN` / `BIG_ENDIAN` in scope on Android.

`evconfig-private_android.h` should be kept aligned with generated
`include/evconfig-private.h`; for Android API 23 it currently matches
the linux private config.

## Windows configuration

Keep `EVENT__HAVE_WEPOLL` and `EVENT__HAVE_BCRYPTGENRANDOM` enabled in
`event2-config_msvc.h`, matching libevent's CMake configuration for Windows.
The core library must also link `bcrypt.lib` for the latter. Listing `wepoll.c`
in `srcs` alone does not enable the backend: `epoll.c` and `event.c` both use
`EVENT__HAVE_WEPOLL` to compile and register it.

`test-platform` initializes threading, excludes the `win32` backend as Envoy does,
and verifies that `wepoll` initializes and dispatches an event. It runs in the
existing Windows presubmit without requiring OpenSSL.

## macOS configuration

Preserve the CMake-detected `arc4random_stir`, `pread`,
`pthread_mutexattr_setprotocol`, `socketpair`, and `strsignal` capabilities when
updating `event2-config_apple.h`. Omitting `socketpair` silently selects libevent's
TCP emulation; `test-platform` verifies that Unix socket pairs remain native.

The native Bazel libraries retain CMake's `-fno-strict-aliasing` on non-Windows
platforms. MSVC and clang-cl already use that aliasing behavior by default.
