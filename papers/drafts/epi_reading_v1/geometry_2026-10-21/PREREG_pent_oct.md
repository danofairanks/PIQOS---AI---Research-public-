# PREREG (2026-10-21): pentagon + octagon re-check. Written after reading records.json fields and the paper's pentagon/octagon text, BEFORE running any geometry.
Conventions (stated up front): pentagon vertex k = centre + R(cos(a+pi/10+2pi k/5), sin(...)), R=1/(2 sin(pi/5)), a = piece angle (radians), piece = [x, y, a]. Enclosing shape = equilateral triangle, either orientation, minimal side by support functions. Octagon = regular, circumradius 1, centre at origin, both orientations tried; the one that fits the data is reported, and that choice is itself reported as a convention found from the data, not verified.
- Q1: octagon: one orientation gives implied radius equal to claimed 0.14729738042484086 within 1e-14.
- Q2: pentagons: 9/9 have max pairwise penetration <= 1e-12, and the implied minimal triangle side equals the claimed value within 1e-9.
- Q3: the 'current_reference' values equal the claimed values to the displayed digits for all 9 (already visible in the data: 'listed' = matching, not exceeding, the current listing at displayed precision).
- Q4: no pentagon record shows penetration or side error that would change the comparison to the previous listing.
