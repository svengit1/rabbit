import pyglet


class EnemyAnimation:
    WALK_LEFT = 1
    WALK_RIGHT = 2
    IDLE_RIGHT = 3
    IDLE_LEFT = 4
    ATTACK_LEFT = 5
    ATTACK_RIGHT = 6
    DEAD_RIGHT = 7
    DEAD_LEFT = 8
    __instance = None

    def __init__(self, size):
        self.imgs = dict()

        self.imgs[EnemyAnimation.WALK_RIGHT] = [
            self.reduce_size(
                size,
                pyglet.resource.image("m-walk-{}.png".format(i), atlas=False))
            for i in range(1, 11)
        ]
        self.flip(EnemyAnimation.WALK_LEFT, EnemyAnimation.WALK_RIGHT)

        self.imgs[EnemyAnimation.ATTACK_RIGHT] = [
            self.reduce_size(
                size,
                pyglet.resource.image("m-attack-{}.png".format(i),
                                      atlas=False)) for i in range(1, 9)
        ]
        self.flip(EnemyAnimation.ATTACK_LEFT, EnemyAnimation.ATTACK_RIGHT)

    @staticmethod
    def instance(size):
        if EnemyAnimation.__instance is None:
            EnemyAnimation.__instance = EnemyAnimation(size)
        return EnemyAnimation.__instance

    @staticmethod
    def reduce_size(to_parcentage, image):
        assert to_parcentage > 0
        image.width = int(image.width * (to_parcentage / 100))
        image.height = int(image.height * (to_parcentage / 100))
        image.anchor_x = 1  #image.width // 2
        return image

    def flip(self, dest, src):
        self.imgs[dest] = []
        for i in self.imgs[src]:
            new_image = i.get_transform(flip_x=True)
            new_image.anchor_x = 0  #new_image.width // 4
            self.imgs[dest].append(new_image)

    def get_animation(self, animation_type, **kwargs):
        duration = kwargs.get('duration')
        loop = bool(kwargs.get('loop'))
        if duration:
            duration = float(duration)
        else:
            duration = 0.8
        return pyglet.image.Animation.from_image_sequence(
            self.imgs[animation_type], duration, loop)
