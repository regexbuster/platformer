import pygame

colors = {
    "Black": pygame.Color(1, 1, 1),
    "Dark_Red": pygame.Color(128, 0, 0),
    "Red": pygame.Color(255, 0, 0),
    "Pink": pygame.Color(255, 0, 255),
    "Teal": pygame.Color(0, 128, 128),
    "Green": pygame.Color(0, 128, 0),
    "Bright_Green": pygame.Color(0, 255, 0),
    "Turquoise": pygame.Color(0, 255, 255),
    "Dark_Blue": pygame.Color(0, 0, 128),
    "Violet": pygame.Color(128, 0, 128),
    "Blue": pygame.Color(0, 0, 255),
    "Quarter_Gray": pygame.Color(192, 192, 192),
    "Half_Gray": pygame.Color(128, 128, 128),
    "Dark_Yellow": pygame.Color(128, 128, 0),
    "Yellow": pygame.Color(255, 255, 0),
    "White": pygame.Color(255, 255, 255),
    "Orange": pygame.Color(255, 165, 0),
    "Brown": pygame.Color(139,69,19)
}


def letter_to_color(letter):
    letter = letter.upper()
    if letter == "B":
        return colors["Black"]
    if letter == "R":
        return colors["Red"]
    if letter == "P":
        return colors["Purple"]
    if letter == "T":
        return colors["Teal"]
    if letter == "G":
        return colors["Green"]
    if letter == "Q":
        return colors["Turquoise"]
    if letter == "V":
        return colors["Violet"]
    if letter == "U":
        return colors["Blue"]
    if letter == "Y":
        return colors["Yellow"]
    if letter == "W":
        return colors["White"]
    if letter == "O":
        return colors["Orange"]
    if letter == "GR":
        return colors["Half_Gray"]
    if letter == "BR":
        return colors["Brown"]

    raise TypeError("Invalid value of letter")


def pixels_to_rect_list(pixel_matrix, pixel_scale, x_start, y_start):
    rect_map = []
    color_map = []
    for y in range(len(pixel_matrix)):
        for x in range(len(pixel_matrix[0])):
            if pixel_matrix[y][x] != " ":
                rect_map.append(pygame.Rect(x_start + (pixel_scale * x), y_start + (pixel_scale * y), pixel_scale, pixel_scale))
                color_map.append(letter_to_color(pixel_matrix[y][x]))
    return rect_map, color_map
