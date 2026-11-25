# DSA in Python

LeetCode practice in Python, next to the Java track in `../unhomie/`.

## Setup

```sh
cd python && uv sync
```

## Run

```sh
uv run pytest                                  # all solutions
uv run pytest leetcode/easy/*_217_*            # one problem
```

## Add a solution

1. Name the file `__{n}_{id}_{snake_name}.py`. `n` is the next number in the difficulty folder.
2. Put it in `leetcode/{easy,medium,hard}/`.
3. Keep the LeetCode `Solution` class and method signature.
4. Add a parametrized `test_` function in the same file.

See `leetcode/easy/__1_217_contains_duplicate.py`.
