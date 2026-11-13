// octsphere() beside OpenSCAD's sphere() at the same resolution, and an
// octsphere hemisphere.
use <../octsphere.scad>;

$fn = 64;

translate([45, 0, 0]) color("pink") sphere(20);
color("lightgreen") octsphere(20);
translate([-45, 0, 0]) color("lightblue") octsphere(20, hemisphere = true);
