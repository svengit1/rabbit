import pyglet

from resources import player_image


class PlayerAnimation:
    RUN_LEFT = 1
    RUN_RIGHT = 2
    STAND_RIGHT = 3
    STAND_LEFT = 4
    JUMP_LEFT = 5
    JUMP_RIGHT = 6
    ROLL_RIGHT = 7
    ROLL_LEFT = 8
    FLY_LEFT = 9
    FLY_RIGHT = 10
    LAND_LEFT = 11
    LAND_RIGHT = 12
    FALL_LEFT = 13
    FALL_RIGHT = 14
    KICK_LEFT = 15
    KICK_RIGHT = 16
    POWER_KICK_LEFT = 17
    POWER_KICK_RIGHT = 18
    PUNCH_LEFT = 19
    PUNCH_RIGHT = 20

    class ImgRegion:
        def __init__(self, **kwargs):
            self.width = kwargs['width']
            self.height = kwargs['height']
            self.x = kwargs['x']
            self.y = kwargs['y']

    def __init__(self):
        self.imgs = dict()

        width = 54
        self.imgs[PlayerAnimation.FLY_RIGHT] = [
            self.carve_img(self.ImgRegion(x=15, y=18, width=width, height=84)),
            self.carve_img(self.ImgRegion(x=80, y=18, width=width, height=84)),
            self.carve_img(self.ImgRegion(x=136, y=18, width=width, height=84))
        ]
        self.flip(PlayerAnimation.FLY_LEFT, PlayerAnimation.FLY_RIGHT)
        width = 54
        self.imgs[PlayerAnimation.KICK_RIGHT] = [
            self.carve_img(
                self.ImgRegion(x=i * 63, y=196, width=width, height=78))
            for i in range(3)
        ]
        self.flip(PlayerAnimation.KICK_LEFT, PlayerAnimation.KICK_RIGHT)
        width = 54
        self.imgs[PlayerAnimation.POWER_KICK_RIGHT] = [
            self.carve_img(self.ImgRegion(x=0, y=276, width=54, height=78),
                           60),
            self.carve_img(self.ImgRegion(x=63, y=276, width=54, height=78)),
            self.carve_img(self.ImgRegion(x=125, y=274, width=62, height=78)),
            self.carve_img(self.ImgRegion(x=204, y=274, width=62, height=78))
        ]

        self.flip(PlayerAnimation.POWER_KICK_LEFT,
                  PlayerAnimation.POWER_KICK_RIGHT)
        self.imgs[PlayerAnimation.PUNCH_RIGHT] = [
            self.carve_img(self.ImgRegion(x=5, y=578, width=45, height=78),
                           63),
            self.carve_img(self.ImgRegion(x=47, y=578, width=63, height=78),
                           63),
            self.carve_img(self.ImgRegion(x=5, y=578, width=45, height=78),
                           63),
            self.carve_img(self.ImgRegion(x=151, y=578, width=45, height=78),
                           63),
            self.carve_img(self.ImgRegion(x=195, y=578, width=63, height=78),
                           63)
        ]
        self.flip(PlayerAnimation.PUNCH_LEFT, PlayerAnimation.PUNCH_RIGHT)
        width = 68
        self.imgs[PlayerAnimation.RUN_RIGHT] = [
            self.carve_img(
                self.ImgRegion(x=i * width, y=929, width=width, height=63))
            for i in range(3)
        ]
        self.flip(PlayerAnimation.RUN_LEFT, PlayerAnimation.RUN_RIGHT)
        y = 752
        self.imgs[PlayerAnimation.ROLL_RIGHT] = [
            self.carve_img(self.ImgRegion(x=16, y=y, width=45, height=78)),
            self.carve_img(self.ImgRegion(x=66, y=y, width=45, height=78)),
            self.carve_img(self.ImgRegion(x=111, y=y, width=40, height=78)),
            self.carve_img(self.ImgRegion(x=151, y=y, width=35, height=78)),
            self.carve_img(self.ImgRegion(x=186, y=y, width=32, height=78)),
            self.carve_img(self.ImgRegion(x=218, y=y, width=32, height=78)),
            self.carve_img(self.ImgRegion(x=252, y=y, width=32, height=78)),
            self.carve_img(self.ImgRegion(x=284, y=y, width=32, height=78)),
            self.carve_img(self.ImgRegion(x=151, y=y, width=35, height=78)),
            self.carve_img(self.ImgRegion(x=111, y=y, width=40, height=78)),
            self.carve_img(self.ImgRegion(x=66, y=y, width=45, height=78)),
            self.carve_img(self.ImgRegion(x=16, y=y, width=45, height=78))
        ]
        self.flip(PlayerAnimation.ROLL_LEFT, PlayerAnimation.ROLL_RIGHT)

        self.imgs[PlayerAnimation.STAND_RIGHT] = [
            self.carve_img(
                self.ImgRegion(x=6 + i * 45, y=1005, width=45, height=78))
            for i in range(4)
        ]
        self.flip(PlayerAnimation.STAND_LEFT, PlayerAnimation.STAND_RIGHT)
        self.imgs[PlayerAnimation.JUMP_RIGHT] = [
            self.carve_img(self.ImgRegion(x=85, y=112, width=45, height=84)),
            self.carve_img(self.ImgRegion(x=145, y=108, width=45, height=84)),
            self.carve_img(self.ImgRegion(x=210, y=108, width=45, height=84)),
            self.carve_img(self.ImgRegion(x=260, y=108, width=45, height=84)),
            self.carve_img(self.ImgRegion(x=305, y=108, width=45, height=84))
        ]

        self.flip(PlayerAnimation.JUMP_LEFT, PlayerAnimation.JUMP_RIGHT)

        self.imgs[PlayerAnimation.FALL_RIGHT] = [
            self.carve_img(self.ImgRegion(x=348, y=840, width=50, height=84))
        ]
        self.flip(PlayerAnimation.FALL_LEFT, PlayerAnimation.FALL_RIGHT)

    def flip(self, dest, src):
        self.imgs[dest] = [
            i.get_transform(flip_x=True) for i in self.imgs[src]
        ]

    def carve_img(self, img_region, target_width=0):
        if target_width == 0:
            target_width = img_region.width
        image = pyglet.image.Texture.create(target_width, img_region.height)
        image.blit_into(
            player_image.get_region(img_region.x, img_region.y,
                                    img_region.width,
                                    img_region.height).get_image_data(), 0, 0,
            0)
        return image

    def get_animation(self, animation_type, **kwargs):
        duration = kwargs.get('duration')
        loop = bool(kwargs.get('loop'))
        if duration:
            duration = float(duration)
        else:
            duration = 0.8

        return pyglet.image.Animation.from_image_sequence(
            self.imgs[animation_type], duration, loop)
