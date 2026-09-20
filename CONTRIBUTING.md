# Contributing

`xirr` calculates the irregular internal rate of return (xirr) and net present value (xnpv). It is published to PyPI.
User documentation is in `docs/` (built with Sphinx, hosted on Read the Docs).

## Layout

| Path | Content |
|---|---|
| `src/xirr/` | the package, the calculations are in `math.py` |
| `tests/xirr/` | tests, mirroring the layout of `src` |
| `docs/` | user documentation, `docs/api` is generated at build time and git-ignored |

The examples in the docstrings are doctests and run with the tests.

## Setup

```bash
uv sync --locked --dev
```

Python 3.11 to 3.14 are supported and tested.

## Checks

CI runs the same commands, all of them have to pass:

```bash
uv run pre-commit run --all-files   # ruff, ruff format, mypy, uv-lock, zizmor, rst lint
uv run deptry src                   # imports vs declared dependencies
uv run pytest
uv run --group docs sphinx-build -W --keep-going -b html docs docs/_build   # documentation without warnings
uv build
```

Things that catch people out:

- `pre-commit run --all-files` only looks at files tracked by git. `git add` new files before running it, otherwise
  they are not checked (and CI then fails on them).
- mypy runs in the project environment (a local pre-commit hook calling `uv run mypy`), so it checks against the types of
  the installed packages. Stub packages (`types-*`) belong into the `dev` dependency group.
- deptry fails for an import that is only available transitively and for a declared dependency that is not used.
  Declare what you import in `pyproject.toml`, remove what you stop using.

## Code

- Type hints are required in `src` (mypy `disallow_untyped_defs`, tests are exempt).
- ruff selects `E4, E7, E9, F, B, I, S113, T20, UP` (see `pyproject.toml`), `ruff format` decides the formatting.
- The function names (`cleanXirr`, `listsXirr`, ...) and the `valuesPerDate` parameters are public API, do not rename them.

## Dependencies

- `uv.lock` is committed. Regenerate it with the uv version of the `uv-lock` pre-commit hook (`rev` in
  `.pre-commit-config.yaml`), a different uv version rewrites unrelated parts of the file:
  `uvx --from uv==<rev> uv lock`.
- Dependabot (`.github/dependabot.yml`) opens grouped PRs for minor and patch updates of Python packages weekly and for
  GitHub Actions monthly. Major updates come as separate PRs. New releases wait 7 days (cooldown), security updates do not.

## Git and pull requests

- Branch off `master`, named `feature/…`, `bugfix/…` or `chore/…` (snake_case after the prefix). The prefix labels the PR
  (`.github/pr-labeler.yml`), and the label decides the category in the release notes (`.github/release-drafter.yml`).
- Commit subjects are imperative and start with a capital letter ("Fix xirr for a single negative cash flow"),
  the body explains why.
- Changes go through pull requests into `master`.

## CI and releases

`.github/workflows/build-publish.yml` runs `lint`, `test` (matrix), `build`, and on pushes to `master` and version tags
the publish jobs. Workflows use the least permissions they need, and every action is pinned to a commit SHA
(Dependabot keeps the pins current, zizmor fails for unpinned actions or broad permissions).

- Every push to `master` publishes a development version to TestPyPI.
- Release notes are drafted by release-drafter. Publishing the draft creates the tag `vX.Y.Z`, which publishes to PyPI.
- Publishing uses PyPI trusted publishing (OIDC) from the GitHub environments `testpypi` and `pypi`, there are no
  stored tokens.
- The version is derived from the git tags (uv-dynamic-versioning), so CI checks out the full history (`fetch-depth: 0`).
