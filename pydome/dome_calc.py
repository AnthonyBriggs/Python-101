#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Calculate the strut lengths for a geodesic dome.

Uses euclid for vectors (http://partiallydisassembled.net/euclid.html).

TODO: Switch to https://github.com/ezag/pyeuclid/ ?
"""

from collections import Counter
import math
import sys

from euclid import Vector3

DEBUG = False
def debug(*debug_strings):
    if DEBUG:
        print(' '.join(debug_strings))

# parse input
frequency = 2
radius = 1
for item in sys.argv[1:]:
    if item.endswith('v'):
        frequency = int(item[:-1])
    elif item.isdigit():
        radius = int(item)

# From http://en.wikipedia.org/wiki/Icosahedron#Cartesian_coordinates
# An icosahedron is defined by the following coordinates:
#    (0, ±1, ±φ)
#    (±1, ±φ, 0)
#    (±φ, 0, ±1) 
phi = (1.0 + math.sqrt(5)) / 2.0
debug("Phi is:", phi)

# We only need one face to calculate strut lengths
# I picked these coordinates by looking carefully at http://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Icosahedron-golden-rectangles.svg/200px-Icosahedron-golden-rectangles.svg.png
# and choosing the closest face 
#       (lt grn: y=0, purple: x=0, dk grn: z=0)
center = (0.0, 0.0, 0.0)
points = [(phi, 1.0, 0.0), (1.0, 0.0, phi), (0.0, phi, 1.0)]

# interpolate points in the triangle - 
#   2v == split each side into 2, 3v == 3, etc.
#       1               1
#      2 3             2 3
#     4 5 6           4 5 6
#                    7 8 9 10
#
#  0 + 1 + 2 + 3   0 + 1 + 2 + 3 + 4
num_nodes = sum(range(frequency+2))

# pick two vectors, one going 'left' and another 'right' from start,
# and generate all of the remaining points from combinations of them.
start = Vector3(*points[0])
left = Vector3(*points[1]) - start
right = Vector3(*points[2]) - start
vec_left = left / frequency
vec_right = right / frequency
debug( "L:", vec_left, abs(vec_left) )
debug( "R:", vec_right, abs(vec_right) )
debug( "R-L:", vec_right - vec_left, abs(vec_right - vec_left) )

# In theory right, but alas, floating point!
#assert abs(vec_left) == abs(vec_right) == abs(vec_right - vec_left)

# generate combinations - start with all left, then sub the 
# end left ones for right:  LLL, LLR, LRR, RRR
output_points = [Vector3(*points[0])]
for i in range(1, frequency + 1):
    debug(i)
    for j in range(i+1):
        debug("   " + "L" * (i-j) + "R" * j)
        point = start + vec_left * (i-j) + vec_right * j
        output_points.append(point)
debug(output_points)
debug(frequency, num_nodes)
debug()

# normalise points to the outside of a unit sphere
output_points = [p.normalized() for p in output_points]


# calc strut lengths ( to how many dp?)
# need to neighborify?
# 1v == 1,2 1,3 2,3
# 2v == 1,2 1,3 2,3 2,4 2,5 3,5 3,6 4,5 5,6
# 3v == 2v + 4,7 4,8 5,8 5,9 6,9 6,10 7,8 8,9 9,10
def triangulate(the_list):
    to_triangulate = the_list[:]
    output = []
    count = 1
    while to_triangulate != []:
        try:
            output.append([to_triangulate.pop(0) for i in range(count)])
        except IndexError:
            raise ValueError(("The list %s does not have a triangular "
                              "number of items!") % the_list)
        count += 1
    return output


def join_nodes(node_list):
    return [(node_list[index], node_list[index+1])
        for index, node in enumerate(node_list[:-1])]

def link_rows(first_row, second_row, internal=False, last=False):
    """Link two rows of nodes and return them as tuples.
    If internal is set, return just the internal nodes.
    If last and internal are set, don't join the bottom row of nodes
        (it'll be an edge)."""
    output = []
    debug( first_row, second_row)
    for index, node in enumerate(first_row):
        # link each first row node to two neighbors in 2nd row
        output.append((node, second_row[index]))
        output.append((node, second_row[index+1]))
    
    if internal:
        # first and last nodes will be external
        output = output[1:-1]

    # link nodes in second row together
    if not(internal and last):
        output += join_nodes(second_row)
    
    return output

#       0               0
#      1 2             1 2
#     3 4 5           3 4 5
#                    6 7 8 9

def link_edge(tri_list):
    """Return one edge of a triangulated list"""
    return join_nodes([line[0] for line in tri_list])

def link_nodes(tri_list, internal=False):
    """Given a triangulated list of points, return all of the links/edges.
    If internal is True, don't return outside edges."""
    output = []
    for i, node_list in enumerate(tri_list[:-1]):
        # link to each row in turn, eg. (1, (2,3)) then ((2,3), (4,5,6))
        output += link_rows(tri_list[i], tri_list[i+1], 
                            internal=internal, 
                            last=(i+2==len(tri_list)))
    return output

tri_points = triangulate(output_points)

triangulated = link_nodes(tri_points)
for t in triangulated:
    debug(t)

internal = link_nodes(tri_points, internal=True)
for i in internal:
    debug(t)

edges = link_edge(tri_points)
for e in edges:
    debug(e)

strut_lengths = [abs(v1 - v2) for v1, v2 in triangulated]
int_strut_lengths = [abs(v1 - v2) for v1, v2 in internal]
edge_lengths = [abs(v1 - v2) for v1, v2 in edges]

# strut lengths + nodes
node_numbers = link_nodes(triangulate(list(range(num_nodes))))
struts_and_numbers = ["%s: %.05f" % (node, sl) 
                        for node, sl in zip(node_numbers, strut_lengths)]


print("All strut lengths:\n   ", end=' ')
print('\n    '.join(struts_and_numbers))
print()
print("Strut counts (per triangle):")
#print set(["%.05f" % sl for sl in strut_lengths])
counts = Counter(["%.05f" % sl for sl in strut_lengths])
for length, count in sorted(counts.items()):
    print("    %s\t%d" % (length, count))

if 0:
    # TODO: counts for a whole dome?
    print()
    print(triangulate(list(range(num_nodes))))
    print(link_edge(triangulate(list(range(num_nodes)))))
    print(link_edge(triangulate(output_points)))
    print()
    print(link_nodes(triangulate(list(range(num_nodes))), internal=True))
    print(link_nodes(triangulate(output_points), internal=True))


