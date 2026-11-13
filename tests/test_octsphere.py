"""Render octsphere() in a set of cases and check each result.

usage: python3 tests/test_octsphere.py [OPENSCAD]

Each case renders a call to octsphere() with --hardwarnings and checks the
STL's separate solids (triangles sharing a vertex belong to the same solid),
its size to within 0.01 mm, its triangle count, and that every vertex lies on
the sphere: within 0.01 mm of the radius, or on the flat base of a hemisphere.
"""

import math
import os
import struct
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, "octsphere.scad")


def load(path):
    data = open(path, "rb").read()
    (n,) = struct.unpack_from("<I", data, 80)
    tris = [struct.unpack_from("<9f", data, 84 + i * 50 + 12) for i in range(n)]
    return [[t[0:3], t[3:6], t[6:9]] for t in tris]


def solids(tris):
    parent = {}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for corners in tris:
        for c in corners:
            parent.setdefault(c, c)
        root = find(corners[0])
        for c in corners[1:]:
            parent[find(c)] = root
    return len({find(v) for v in parent})


# (label, OpenSCAD source, radius, hemisphere, triangles)
# The equator has the nearest 4 x 2^n sides to the fragment count, and a
# sphere of 2^n-sided levels has 8 x 4^n triangles; a hemisphere has half of
# those plus its base, which OpenSCAD triangulates.
CASES = [
    ("defaults: $fa 12, $fs 2 give 30 fragments, so 32 sides", "octsphere(r = 20);", 20, False, 512),
    ("$fn = 3 rounds up to the octahedron", "$fn = 3; octsphere(r = 20);", 20, False, 8),
    ("$fn = 4 is the octahedron", "$fn = 4; octsphere(r = 20);", 20, False, 8),
    ("$fn = 50 snaps to 64 sides", "$fn = 50; octsphere(d = 30);", 15, False, 2048),
    ("$fa 2, $fs 0.5 give 180 fragments, so 128 sides", "$fa = 2; $fs = 0.5; octsphere(r = 20);", 20, False, 8192),
    ("hemisphere, $fn = 64", "$fn = 64; octsphere(r = 20, hemisphere = true);", 20, True, 1086),
    ("no size: radius 1", "$fn = 16; octsphere();", 1, False, 128),
]


def main():
    openscad = sys.argv[1] if len(sys.argv) > 1 else "openscad"
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        scad, stl = os.path.join(tmp, "case.scad"), os.path.join(tmp, "case.stl")
        for label, body, r, hemi, want_tris in CASES:
            with open(scad, "w") as f:
                f.write(f"use <{LIB}>;\n{body}\n")
            result = subprocess.run([openscad, "--hardwarnings", "--export-format", "binstl", "-o", stl, scad],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                errors = [l for l in result.stderr.splitlines() if "WARNING" in l or "ERROR" in l]
                failures.append(label)
                print(f"FAIL {label}: openscad exited {result.returncode}: {'; '.join(errors)}")
                continue
            tris = load(stl)
            pts = {p for t in tris for p in t}
            size = [max(p[i] for p in pts) - min(p[i] for p in pts) for i in range(3)]
            want_size = [2 * r, 2 * r, r if hemi else 2 * r]
            off = [p for p in pts if abs(math.dist(p, (0, 0, 0)) - r) > 0.01 and not (hemi and abs(p[2]) < 1e-6)]
            n = solids(tris)
            problems = []
            if n != 1:
                problems.append(f"{n} solids")
            if any(abs(a - b) > 0.01 for a, b in zip(size, want_size)):
                problems.append("size " + " x ".join(f"{s:.2f}" for s in size))
            if len(tris) != want_tris:
                problems.append(f"{len(tris)} triangles, expected {want_tris}")
            if off:
                problems.append(f"{len(off)} vertices off the sphere")
            got = f"{len(tris)} triangles, " + " x ".join(f"{s:.2f}" for s in size) + " mm"
            if problems:
                failures.append(label)
                print(f"FAIL {label}: " + "; ".join(problems))
            else:
                print(f"ok   {label}: {got}")
    print("all checks passed" if not failures else f"{len(failures)} failed")
    sys.exit(1 if failures else 0)


main()
