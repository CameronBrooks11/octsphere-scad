// A hemisphere, an octsphere and OpenSCAD's sphere(), side by side at one resolution.
// Left to right: octsphere(hemisphere = true), octsphere(), sphere().

use <../octsphere.scad>;

// Sides around each equator; octsphere snaps to 4, 8, 16, 32, 64 or 128
sides = 16; // [4, 8, 16, 32, 64, 128]

$fn = sides;

translate([45, 0, 0]) color("pink") sphere(20);
color("lightgreen") octsphere(20);
translate([-45, 0, 0]) color("lightblue") octsphere(20, hemisphere = true);
