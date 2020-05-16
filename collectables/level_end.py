from collectables.collectable import Collectable
from resources import map_images


class LevelEnd(Collectable):
    MUSHROOM = 27

    def __init__(self, *args, **kwargs):
        image = map_images[self.MUSHROOM]
        super().__init__(image, 50, **kwargs)
        self.shape.collision_type = 10
        self.shape.sprite = self
        self.shape.friction = 1

