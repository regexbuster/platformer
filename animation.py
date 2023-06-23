from glob import glob

import pygame.image
import utils


class Animation:
    def __init__(self, images_dir, frame_delay):
        self.images_dir = images_dir
        self.frame_delay = frame_delay

        self.images = []

        image_list = glob(f'./{images_dir}/*.gif')
        for image in image_list:
            sur = pygame.image.load(image)
            sur.set_colorkey(utils.colors["Background_Color_Key"])
            self.images.append(sur)

        self.frames = len(self.images)

        self.current_frame = 0
        self.current_delay = 0

    def get_current_frame(self):
        frame = self.images[self.current_frame]

        if self.current_delay < self.frame_delay:
            self.current_delay += 1
        else:
            self.current_delay = 0
            if self.current_frame + 1 >= self.frames:
                self.current_frame = 0
            else:
                self.current_frame += 1

        return frame

    def add_frame(self, frame):
        self.images.append(frame)
        self.frame = len(self.images)

    def get_size(self):
        return self.images[0].get_size()
