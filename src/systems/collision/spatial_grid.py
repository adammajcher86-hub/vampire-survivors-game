"""
Spatial Grid
Divides world space into cells for efficient collision detection
Only checks entities in same/nearby cells
"""


class SpatialGrid:
    """
    Spatial partitioning grid for efficient collision detection
    Reduces collision checks from O(n²) to O(n)
    """

    def __init__(self, cell_size=100):
        """
        Initialize spatial grid

        Args:
            cell_size: Size of each grid cell in pixels (default 100)
                      Adjust based on entity size for best performance
        """
        self.cell_size = cell_size
        self.grid = {}  # {(cell_x, cell_y): [entities]}

    def clear(self):
        """Clear all entities from grid"""
        self.grid.clear()

    def _get_cell(self, position):
        """
        Get cell coordinates for a position

        Args:
            position: pygame.math.Vector2

        Returns:
            tuple: (cell_x, cell_y)
        """
        cell_x = int(position.x // self.cell_size)
        cell_y = int(position.y // self.cell_size)
        return (cell_x, cell_y)

    def _get_cells_for_entity(self, entity, radius=None):
        """
        Get all cells that an entity occupies

        Args:
            entity: Entity with position attribute
            radius: Optional collision radius (auto-detect if None)

        Returns:
            list: List of cell coordinates [(x1,y1), (x2,y2), ...]
        """
        # Determine radius
        if radius is None:
            if hasattr(entity, "collision_radius"):
                radius = entity.collision_radius
            elif hasattr(entity, "radius"):
                radius = entity.radius
            else:
                radius = 20  # Default fallback

        # Calculate cell range
        min_x = int((entity.position.x - radius) // self.cell_size)
        max_x = int((entity.position.x + radius) // self.cell_size)
        min_y = int((entity.position.y - radius) // self.cell_size)
        max_y = int((entity.position.y + radius) // self.cell_size)

        # Return all cells in range
        cells = []
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                cells.append((x, y))

        return cells

    def add_entity(self, entity, radius=None):
        """
        Add entity to grid

        Args:
            entity: Entity to add (must have position attribute)
            radius: Optional collision radius
        """
        cells = self._get_cells_for_entity(entity, radius)

        for cell in cells:
            if cell not in self.grid:
                self.grid[cell] = []
            self.grid[cell].append(entity)

    def get_nearby_entities(self, position, radius=50):
        """
        Get all entities near a position

        Args:
            position: pygame.math.Vector2 or entity with position
            radius: Search radius in pixels

        Returns:
            set: Set of nearby entities (deduplicated)
        """
        # Handle entity or position
        if hasattr(position, "position"):
            pos = position.position
            if hasattr(position, "collision_radius"):
                radius = max(radius, position.collision_radius)
        else:
            pos = position

        # Calculate cells to check
        min_x = int((pos.x - radius) // self.cell_size)
        max_x = int((pos.x + radius) // self.cell_size)
        min_y = int((pos.y - radius) // self.cell_size)
        max_y = int((pos.y + radius) // self.cell_size)

        # Collect entities from nearby cells
        nearby = set()
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                cell = (x, y)
                if cell in self.grid:
                    nearby.update(self.grid[cell])

        return nearby

    def get_entities_in_range(self, position, radius, entity_list=None):
        """
        Get entities within exact radius of position
        (Uses grid for initial filtering, then exact distance check)

        Args:
            position: pygame.math.Vector2
            radius: Exact radius to check
            entity_list: Optional list to filter (if None, checks all nearby)

        Returns:
            list: Entities within exact radius
        """
        # Get nearby entities from grid
        nearby = self.get_nearby_entities(position, radius)

        # Filter by entity list if provided
        if entity_list is not None:
            nearby = nearby.intersection(set(entity_list))

        # Exact distance check
        in_range = []
        for entity in nearby:
            distance = entity.position.distance_to(position)
            if distance <= radius:
                in_range.append(entity)

        return in_range

    def debug_info(self):
        """Get debug information about grid state"""
        total_entities = sum(len(entities) for entities in self.grid.values())
        return {
            "cells_used": len(self.grid),
            "total_entities": total_entities,
            "avg_per_cell": total_entities / len(self.grid) if self.grid else 0,
        }
