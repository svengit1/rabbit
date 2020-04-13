import pyglet


class MapEntity:
    def __init__(self, *args, **kwargs):
        self.window_height = kwargs['window'].height
        self.window_width = kwargs['window'].width
        self.batch = kwargs['batch']
        self.group = kwargs['group']
        self.content = []

    def get_sprite(self, img, x, y):
        return pyglet.sprite.Sprite(img=img, y=y, x=x,
                                    batch=self.batch, group=self.group)

    def get_y(self, vpos):
        assert 0 <= vpos <= self.window_height // 32, "Invalid vpos range"
        return vpos * 32

    def get_x(self, hpos):
        return hpos * 32
