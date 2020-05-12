from map_objects.map_entity import MapEntity
from resources import map_images, segment_height, segment_width


class Bush(MapEntity):
    def __init__(self, **kwargs):
        self.image = map_images[38].get_image_data()
        self.x = kwargs['hpos'] * segment_width
        self.y = kwargs['vpos'] * segment_height
