default:
    @just --list

# Render octsphere() at several resolutions and check size, closure and vertices
test:
    python3 tests/test_octsphere.py

# Everything CI runs, bar the tests
check: fmt-check

# Format the .scad sources with topiary (.topiary/languages.ncl)
fmt:
    git ls-files -z '*.scad' | xargs -0 -r topiary format

# Check the .scad sources are formatted, without changing them
fmt-check:
    git ls-files -z '*.scad' | xargs -0 -r -n1 topiary format --check

# Render the README picture into assets/
images:
    @mkdir -p assets
    openscad --render --view=edges --colorscheme=Tomorrow --imgsize=900,380 --camera=0,0,0,70,0,10,150 -o assets/compare.png examples/compare.scad
