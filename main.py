import arcade
import random


SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SPRITE_SCALING_CAR = 0.5
SPRITE_SCALING_WALL = 0.5
CAR_MOVEMENT_SPEED = 3
WALL_MOVEMENT_SPEED = 3

class Sprite:
    @property
    def center_x(self):
        return self.sprite.center_x
    
    @center_x.setter
    def center_x(self, value):
        self.sprite.center_x = value

    @property
    def center_y(self):
        return self.sprite.center_y

    @center_y.setter
    def center_y(self, value):
        self.sprite.center_y = value

    @property
    def change_x(self):
        return self.sprite.change_x
    
    @change_x.setter
    def change_x(self, value):
        self.sprite.change_x = value

    @property
    def change_y(self):
        return self.sprite.change_y

    @change_y.setter
    def change_y(self, value):
        self.sprite.change_y = value

    @property
    def width(self):
        return self.sprite.width

    @property
    def height(self):
        return self.sprite.height


class Car(Sprite):
    def __init__(self):
        self.sprite = arcade.Sprite("resources/car.png", SPRITE_SCALING_CAR)

        self.recreate()

    def recreate(self):
        self.sprite.center_x = self.sprite.width // 2
        self.sprite.center_y = SCREEN_HEIGHT // 2

    def update(self):
        edge = self.width * SPRITE_SCALING_CAR / 2 + self.change_y
        if edge < self.center_y < (SCREEN_HEIGHT - edge):
            self.center_y += self.change_y
        else:
            self.center_y = (edge + 1) if self.center_y < edge else (SCREEN_HEIGHT - edge - 1)
            self.change_y = 0



class Wall(Sprite):
    def __init__(self, speed: float = WALL_MOVEMENT_SPEED):
        self.sprite = arcade.Sprite("resources/wall.png", SPRITE_SCALING_WALL)

        self.speed = speed
        self._acceleration = 0.5

        self.recreate()

    def recreate(self):
        edge_width = self.width // 2
        edge_height = self.height // 2
        self.center_x = SCREEN_WIDTH - edge_width
        self.center_y = random.randint(edge_height + 1, SCREEN_HEIGHT - edge_height - 1)
        self.speed += self._acceleration

    def update(self):
        edge = self.width // 2
        if self.center_x > edge:
            self.center_x -= self.speed
        else:
            self.recreate()


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.car_sprites = None
        self.walls_sprites = None

        self.car = None
        self.walls = None

        self.is_car_crashed = False
        self.score = 0

    def setup(self):
        arcade.set_background_color(arcade.color.ASH_GREY)

        self.car_sprites = arcade.SpriteList()
        self.walls_sprites = arcade.SpriteList()

        self.car = Car()
        self.car_sprites.append(self.car.sprite)
        self.walls = [Wall() for i in range(7)]
        self.walls_sprites.extend([i.sprite for i in self.walls])


    def on_draw(self):
        arcade.start_render()

        self.car_sprites.draw()
        self.walls_sprites.draw()


        score_output = f"Score: {self.score}"
        if self.is_car_crashed:
            restart_message = "The car was crashed press SPACE to restart"
            score_output = f"{score_output} {restart_message:^100}"

        arcade.draw_text(score_output, 10, 20, arcade.color.WHITE, 14)


    def update(self, delta_time):
        self.is_car_crashed = bool(arcade.check_for_collision_with_list(self.car_sprites[0], self.walls_sprites))
        if not self.is_car_crashed:
            self.car.update()
            for wall in self.walls:
                wall.update()
            self.score += 1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.car.change_y = CAR_MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.car.change_y = -CAR_MOVEMENT_SPEED
        elif key == arcade.key.SPACE and self.is_car_crashed:
            self.car.recreate()
            for wall in self.walls:
                wall.speed = WALL_MOVEMENT_SPEED
                wall.recreate()
            self.score = 0

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.car.change_y = 0


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "FarFarThisCar")
    window.setup()

    arcade.run()


if __name__ == "__main__":
    main()
