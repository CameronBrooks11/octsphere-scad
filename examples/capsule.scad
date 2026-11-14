// Capsules capped with octsphere() and with sphere(), side by side.
// The octsphere's equator has the cylinder's vertices, so the caps meet the cylinder edge to
// edge. sphere() has no ring on its equator, so its caps leave a step at each end.

use <../octsphere.scad>;

// Sides around the cylinder and each equator; octsphere snaps to 4, 8, 16, 32, 64 or 128
sides = 16; // [4, 8, 16, 32, 64, 128]
// Radius of the capsule (mm)
radius = 10; // [2:1:50]
// Length of the straight part (mm)
length = 30; // [0:1:200]

$fn = sides;

// Left: octsphere caps.
translate([-radius * 1.5, 0, 0]) color("lightgreen") {
  cylinder(r = radius, h = length);
  translate([0, 0, length]) octsphere(radius, hemisphere = true);
  mirror([0, 0, 1]) octsphere(radius, hemisphere = true);
}

// Right: sphere() caps.
translate([radius * 1.5, 0, 0]) color("pink") {
  cylinder(r = radius, h = length);
  translate([0, 0, length]) sphere(radius);
  sphere(radius);
}
