from game.map_entity import MapEntity
from game.resources import map_images


class Bush(MapEntity):
    def __init__(self):
        self.image = map_images[38].get_image_data()
