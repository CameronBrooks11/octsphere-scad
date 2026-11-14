default:
    @just --list

# Render octsphere() at several resolutions and check size, closure and vertices
test:
    python3 tests/test_octsphere.py

# Render the README picture into assets/
images:
    @mkdir -p assets
    openscad --render --view=edges --colorscheme=Tomorrow --imgsize=900,380 --camera=0,0,0,70,0,10,150 -o assets/compare.png examples/compare.scad
