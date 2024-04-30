import Lake
open Lake DSL

package REPL {
  -- add package configuration options here
}

lean_lib REPL {
  -- add library configuration options here
}

@[default_target]
lean_exe repl where
  root := `REPL.Main
  supportInterpreter := true

require mathlib from git "https://github.com/leanprover-community/mathlib4"@"3cecb823a74ed737c6ebc115e515eba649ec7715"
