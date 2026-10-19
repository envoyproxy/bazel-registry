#include <wasmtime.h>

#if !defined(WASMTIME_FEATURE_CRANELIFT) || !defined(WASMTIME_FEATURE_COMPILER) || \
    !defined(WASMTIME_FEATURE_GC)
#error Missing enabled C API features
#endif

#if defined(WASMTIME_FEATURE_GC_DRC) || defined(WASMTIME_FEATURE_GC_NULL) || \
    defined(WASMTIME_FEATURE_WASI) || defined(WASMTIME_FEATURE_WAT)
#error Unexpected optional C API features
#endif

int main() {
  wasm_config_t *config = wasm_config_new();
  wasmtime_config_strategy_set(config, WASMTIME_STRATEGY_CRANELIFT);
  wasmtime_config_wasm_gc_set(config, false);
  wasm_config_delete(config);
  return 0;
}
