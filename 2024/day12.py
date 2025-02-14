"""
Day 12
https://adventofcode.com/2024/day/12

For a grid of letters (garden of plant types), find the individual regions for each grouping of plants.
For part 1:
Calculate the region's area and perimeter (number of fence segments)
Calculate the costs of fences (for a region, area * parameter)
For part 2: use number of sides instead of perimeter

Return the final cost of all fences in the garden.
"""

from aoc_libs.grid import Position
from aoc_libs.grid import Grid
from aoc_libs.grid import Dir
from aoc_libs.grid import DIR_ORTHOG
import dataclasses


# A region tracks the plant type (unused in logic, but useful for debugging),
# along with a dictionary mapping a given plot position with a set of sides 
# containing a segment of fence for that plot.  (The fences will get added later,)
# so do not initialize them when creating a new region)
@dataclasses.dataclass
class Region:
    plant_type: str
    plots_fences: dict[Position, set[Dir]] = dataclasses.field(
        default_factory=dict, init=False
    )

    # Get just the plots/positions inside the region
    @property
    def plots(self):
        return self.plots_fences.keys()

    # Add a plot and the sides that contain a fence segment to the region
    def add_plot(self, plot, fence_dirs):
        self.plots_fences[plot] = fence_dirs

    # The area is the number of plots contained in the region.
    def get_area(self):
        return len(self.plots)

    # Since each plot knows how many fence segments it has, count up the
    # total fence segments for all the plots.
    def get_fences(self):
        fences = 0
        for f_dirs in self.plots_fences.values():
            fences += len(f_dirs)
        return fences

    # Calculate the number of sides in a region.  This is done by creating slices through the grid
    # of 
    def get_sides(self):
        ############## Helper functions to add the correct side info to the map ##############
        def _update_slice(plot, f_dir, slice_dict):
            match f_dir:
                case Dir.N:
                    slice_dict.setdefault(Slice(True, plot.row, plot.row - 1), []).append(plot.col)
                case Dir.S:
                    slice_dict.setdefault(Slice(True, plot.row, plot.row + 1), []).append(plot.col)
                case Dir.E:
                    slice_dict.setdefault(Slice(False, plot.col, plot.col + 1), []).append(plot.row)
                case Dir.W:
                    slice_dict.setdefault(Slice(False, plot.col, plot.col - 1), []).append(plot.row)
        
        # Count the segments in each list of slices - for all values in a slice, if the values
        # are adjacent, they are part of the same side.
        def _count_sides(slices):
            # Sort values for the slice.  If there is any spot where the following value isn't one more
            # then the previous value, that indicates a break in the set of slices and therefore the
            # end of a side.
            slices.sort()
            sides = 1
            for i in range(len(slices) - 1):
                if slices[i] + 1 != slices[i + 1]:
                    sides += 1
            return sides

        ######################################################################################
        # Create a dictionary that maps a slice to the corresponding perpendicular row or column
        slice_dict = {}

        #print(f"\n\n-------------------------\nGetting sides for region {self.plant_type}")
        for plot, fences in self.plots_fences.items():
            #print(f"\nChecking plot {plot=} with {len(fences)} fences ({fences})")
            # For every plot and fence, create a slice between the plot and the next position
            # based on its direction.  Add it to the slice_dictionary with the matching
            # perpendicular row or col value.
            for f_dir in fences:
                _update_slice(plot, f_dir, slice_dict)

            
            # print(f"Total so far: {len(sides)=}")
            # print("\t", end="")
            # print(*sides, sep="\n\t")

        sides = 0
        # Count the segments in each slice - for all values in a slice, if they are
        for slices in slice_dict.values():
            sides += _count_sides(slices)

        #print(f"Total sides for the region: {len(sides)}")
        return sides


# A slice consists of whether a line is horizontal or vertical, and the x/x or y/y value on either side.
@dataclasses.dataclass(frozen=True)
class Slice:
    hor: bool
    p1: int
    p2: int


#################################################################################
def process_input(input, part1):
    garden = Grid.create_from_input(input)
    regions: list[Region] = get_regions(garden)
    return calculate_cost(regions, part1)


# For a plant type in the garden (unique letter), check all adjacent plots
# to see if they are the same plant.  If they are, they are part of the region.
# If they aren't, they are not part of the region.
#
# If a section of the garden is None, then it means that that plot is already
# part of a region and does not need to be processed again.
def get_regions(garden: Grid) -> list[Region]:
    regions = []
    for p in garden.all_pos_iter():
        plant = garden.get_val(p)
        if plant is not None:
            regions.append(create_region(p, garden))
    return regions

# Create a region by starting at an initial plot and then finding all adjacent plots
# of the same plant type.  The region will contain all positions of plots in the region
# along with the directions of fence segments at that position.
def create_region(initial_plot: Position, garden: Grid) -> Region:
    plant_type = garden.get_val(initial_plot)
    reg = Region(plant_type)

    # Start with the initial plot that will define this region.  Find adjacent plots that are in
    # the region and add them to the set of plots to process.  This will find all the plots of an
    # identical plant type, thus defining the region.
    plots_to_process = {initial_plot}
    # print(f"Creating region of plant {plant_type} starting with plot pos {initial_plot}")
    while plots_to_process:
        p = plots_to_process.pop()

        # Get neighboring plots that haven't been visited and are in the same region (have the same plant type).
        # Also count the number of fences for this plot, counting garden boundaries as well as other regions.
        neighbors, fence_dirs = get_neighbors_and_fences(p, garden, set(reg.plots))

        # Add this plot and directions of fences it contributes to the region
        reg.add_plot(p, fence_dirs)

        # Add the new neighbors in the region to the list of plots to visit
        plots_to_process.update(neighbors)

        # Mark this plot's value as None so that when iterating over the entire garden,
        # this position gets skipped
        garden.set_val(p, None)

    # print(f"{reg.get_area()=}, {reg.get_fences()}")
    return reg


# For a given plot, return both a set of neighboring plots contained in the region (not out of bounds and not
# of a different plant type).  For the non-region neighbors there will be a fence - keep track of which direction
# that fence is relative to the plot.
def get_neighbors_and_fences(
    plot: Position, garden: Grid, plots_in_region: set[Position]
) -> tuple[set[Position], set[Dir]]:
    region_neighbors = set()
    fence_dirs = set()

    # For each direction from the given plot...
    for d in DIR_ORTHOG:
        new_plot = plot.go_dir(d)

        # Do not revisit a plot we've already seen in this region
        if new_plot in plots_in_region:
            continue

        # If this direction ends up being out of bounds, then there's a fence along that slice.
        elif new_plot.out_of_bounds(garden):
            fence_dirs.add(d)

        # Otherwise, compare the plant types.  If they match, then this is a valid neighbor in the region.
        # If they don't match, add a new fence in that direction.
        elif garden.get_val(plot) == garden.get_val(new_plot):
            region_neighbors.add(new_plot)
        else:
            fence_dirs.add(d)

    return region_neighbors, fence_dirs


# The cost is either area x perimeter (or fence segments) for part 1.  For part 2, it is the area x
# the number of sides.
def calculate_cost(regions: list[Region], part1) -> int:
    total = 0
    for r in regions:
        multiplier = r.get_fences() if part1 else r.get_sides()
        total += r.get_area() * multiplier
    return total


########### SCRIPT ARGUMENTS AND EXECUTION ###########
from aoc_libs import lib


def main(part1=True, use_example=True):
    input_text = lib.read_input(__file__, use_example)

    return process_input(input_text, part1)


if __name__ == "__main__":
    print(main(part1=False, use_example=False))
