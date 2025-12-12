"""
Collision Manager
Centralized collision detection system using spatial grid
Handles all game collision types efficiently
"""

from .spatial_grid import SpatialGrid


class CollisionManager:
    """
    Manages all collision detection in the game
    Uses spatial grid for O(n) performance instead of O(n²)
    """

    def __init__(self, cell_size=100):
        """
        Initialize collision manager

        Args:
            cell_size: Size of spatial grid cells (default 100)
        """
        self.grid = SpatialGrid(cell_size)

        # Collision results (populated after check_all)
        self.projectile_hits = []  # [(projectile, enemy)]
        self.enemy_projectile_hits = []  # [(projectile, player)]
        self.player_enemy_collisions = []  # [enemy]
        self.bomb_hits = []  # [(bomb, [enemies])]
        self.pickup_collections = []  # [pickup]

    def clear_results(self):
        """Clear collision results from last frame"""
        self.projectile_hits.clear()
        self.enemy_projectile_hits.clear()
        self.player_enemy_collisions.clear()
        self.bomb_hits.clear()
        self.pickup_collections.clear()

    def rebuild_grid(self, enemies, projectiles, enemy_projectiles, bombs, pickups):
        """
        Rebuild spatial grid with all entities
        Call once per frame before collision checks

        Args:
            enemies: List of enemy entities
            projectiles: List of player projectiles
            enemy_projectiles: List of enemy projectiles
            bombs: List of bombs
            pickups: List of pickups
        """
        self.grid.clear()

        # Add enemies to grid
        for enemy in enemies:
            self.grid.add_entity(enemy)

        # Add projectiles to grid
        for projectile in projectiles:
            self.grid.add_entity(projectile, radius=10)

        # Add enemy projectiles to grid
        for projectile in enemy_projectiles:
            self.grid.add_entity(projectile, radius=10)

        # Add bombs to grid (larger radius for explosion)
        for bomb in bombs:
            self.grid.add_entity(
                bomb,
                radius=(
                    bomb.explosion_radius if hasattr(bomb, "explosion_radius") else 150
                ),
            )

        # Add pickups to grid
        for pickup in pickups:
            self.grid.add_entity(pickup, radius=20)

    # ==================== PROJECTILE vs ENEMY ====================

    def check_projectile_collisions(self, projectiles, enemies):
        """
        Check player projectiles hitting enemies

        Args:
            projectiles: List of player projectiles
            enemies: List of enemies

        Returns:
            list: [(projectile, enemy)] pairs that collided
        """
        hits = []

        for projectile in projectiles:
            # Get nearby enemies using spatial grid
            nearby_enemies = self.grid.get_nearby_entities(projectile, radius=50)

            # Filter to only enemies in the list
            nearby_enemies = [e for e in nearby_enemies if e in enemies]

            # Check exact collision
            for enemy in nearby_enemies:
                # Use projectile's collision check if available
                if hasattr(projectile, "check_collision"):
                    if projectile.check_collision(enemy):
                        hits.append((projectile, enemy))
                        break  # Projectile can only hit one enemy
                else:
                    # Default circle collision
                    distance = projectile.position.distance_to(enemy.position)
                    proj_radius = getattr(projectile, "radius", 5)
                    enemy_radius = getattr(enemy, "collision_radius", 20)

                    if distance < proj_radius + enemy_radius:
                        hits.append((projectile, enemy))
                        break

        return hits

    # ==================== ENEMY PROJECTILE vs PLAYER ====================

    def check_enemy_projectile_collisions(self, enemy_projectiles, player):
        """
        Check enemy projectiles hitting player

        Args:
            enemy_projectiles: List of enemy projectiles
            player: Player entity

        Returns:
            list: [projectile] list of projectiles that hit player
        """
        hits = []

        # Get player collision radius
        player_radius = getattr(player, "collision_radius", 20)

        for projectile in enemy_projectiles:
            # Check distance
            distance = projectile.position.distance_to(player.position)
            proj_radius = getattr(projectile, "radius", 5)

            if distance < proj_radius + player_radius:
                hits.append(projectile)

        return hits

    # ==================== PLAYER vs ENEMY ====================

    def check_player_enemy_collisions(self, player, enemies):
        """
        Check player colliding with enemies (contact damage)

        Args:
            player: Player entity
            enemies: List of enemies

        Returns:
            list: [enemy] list of enemies touching player
        """
        collisions = []

        # Get nearby enemies using spatial grid
        player_radius = getattr(player, "collision_radius", 20)
        nearby_enemies = self.grid.get_nearby_entities(
            player, radius=player_radius + 50
        )

        # Filter to only enemies in the list
        nearby_enemies = [e for e in nearby_enemies if e in enemies]

        # Check exact collision
        for enemy in nearby_enemies:
            distance = player.position.distance_to(enemy.position)
            enemy_radius = getattr(enemy, "collision_radius", 20)

            if distance < player_radius + enemy_radius:
                collisions.append(enemy)

        return collisions

    # ==================== BOMB EXPLOSIONS ====================

    def check_bomb_explosions(self, bombs, enemies):
        """
        Check bombs that should explode and which enemies they hit

        Args:
            bombs: List of bombs
            enemies: List of enemies

        Returns:
            list: [(bomb, [enemies])] - bomb and list of enemies it hits
        """
        explosions = []

        for bomb in bombs:
            # Check if bomb should explode
            if not hasattr(bomb, "is_expired") or not bomb.is_expired():
                continue

            # Get explosion radius
            explosion_radius = getattr(bomb, "explosion_radius", 150)

            # Use grid to find nearby enemies
            nearby_enemies = self.grid.get_nearby_entities(
                bomb, radius=explosion_radius
            )

            # Filter to only enemies in the list
            nearby_enemies = [e for e in nearby_enemies if e in enemies]

            # Check exact distance
            hit_enemies = []
            for enemy in nearby_enemies:
                distance = bomb.position.distance_to(enemy.position)
                if distance <= explosion_radius:
                    hit_enemies.append(enemy)

            if hit_enemies:
                explosions.append((bomb, hit_enemies))

        return explosions

    # ==================== PICKUP COLLECTION ====================

    def check_pickup_collection(self, player, pickups, collection_radius=50):
        """
        Check pickups that player should collect

        Args:
            player: Player entity
            pickups: List of pickups
            collection_radius: Pickup collection radius

        Returns:
            list: [pickup] list of pickups to collect
        """
        collections = []

        # Use grid to find nearby pickups
        nearby_pickups = self.grid.get_nearby_entities(player, radius=collection_radius)

        # Filter to only pickups in the list
        nearby_pickups = [p for p in nearby_pickups if p in pickups]

        # Check exact distance
        for pickup in nearby_pickups:
            distance = player.position.distance_to(pickup.position)
            if distance <= collection_radius:
                collections.append(pickup)

        return collections

    # ==================== MASTER CHECK ====================

    def check_all(
        self, player, enemies, projectiles, enemy_projectiles, bombs, pickups
    ):
        """
        Perform all collision checks in one call
        Results stored in class attributes

        Args:
            player: Player entity
            enemies: List of enemies
            projectiles: List of player projectiles
            enemy_projectiles: List of enemy projectiles
            bombs: List of bombs
            pickups: List of pickups
        """
        # Clear previous results
        self.clear_results()

        # Rebuild spatial grid
        self.rebuild_grid(enemies, projectiles, enemy_projectiles, bombs, pickups)

        # Run all collision checks
        self.projectile_hits = self.check_projectile_collisions(projectiles, enemies)
        self.enemy_projectile_hits = self.check_enemy_projectile_collisions(
            enemy_projectiles, player
        )
        self.player_enemy_collisions = self.check_player_enemy_collisions(
            player, enemies
        )
        self.bomb_hits = self.check_bomb_explosions(bombs, enemies)
        self.pickup_collections = self.check_pickup_collection(player, pickups)

    # ==================== RESULTS ACCESS ====================

    def get_projectile_hits(self):
        """Get list of (projectile, enemy) pairs that collided"""
        return self.projectile_hits

    def get_enemy_projectile_hits(self):
        """Get list of enemy projectiles that hit player"""
        return self.enemy_projectile_hits

    def get_player_enemy_collisions(self):
        """Get list of enemies touching player"""
        return self.player_enemy_collisions

    def get_bomb_hits(self):
        """Get list of (bomb, [enemies]) that exploded"""
        return self.bomb_hits

    def get_pickup_collections(self):
        """Get list of pickups player collected"""
        return self.pickup_collections

    # ==================== DEBUG ====================

    def get_debug_info(self):
        """Get debug information about collision system"""
        grid_info = self.grid.debug_info()
        return {
            "grid_cells": grid_info["cells_used"],
            "entities_in_grid": grid_info["total_entities"],
            "avg_per_cell": grid_info["avg_per_cell"],
            "projectile_hits": len(self.projectile_hits),
            "enemy_projectile_hits": len(self.enemy_projectile_hits),
            "player_collisions": len(self.player_enemy_collisions),
            "bomb_explosions": len(self.bomb_hits),
            "pickups_collected": len(self.pickup_collections),
        }
