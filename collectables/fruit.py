from collectables.collectable import Collectable
from resources import map_images


class Fruit(Collectable):
    CARROT = 216
    GRAPE = 204
    LEMON = 192
    PEAR = 180

    def __init__(self, *args, **kwargs):
        image = map_images[kwargs['type']]
        self.points = kwargs['points']
        kwargs.pop('type')
        kwargs.pop('points')
        super().__init__(image, 0, **kwargs)
        self.shape.collision_type = 2
        self.shape.sprite = self
