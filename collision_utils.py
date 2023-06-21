def most_min(values):
    minimum = values[0]
    for value in values:
        if value < minimum:
            minimum = value
    return minimum


def is_colliding(boundary, player, velocity):
    if not boundary.colliderect(player):
        return 0

    # left sided collision
    pright_in_bleft = player.rect.right - boundary.left
    # right sided collision
    pleft_in_bright = boundary.right - player.rect.left

    # top sided collision
    pbottom_in_btop = player.rect.bottom - boundary.top
    # bottom sided collision
    ptop_in_bbottom = boundary.bottom - player.rect.top

    minimum = most_min([pright_in_bleft, pleft_in_bright, pbottom_in_btop, ptop_in_bbottom])

    # left sided collision
    if pright_in_bleft == minimum:
        player.rect.right = boundary.left
        velocity.x = 0
        return 2
    # right sided collision
    if pleft_in_bright == minimum:
        player.rect.left = boundary.right
        velocity.x = 0
        return 2
    # top collision
    if pbottom_in_btop == minimum:
        player.rect.bottom = boundary.top
        velocity.y = 0
        return 1
    # bottom collision
    if ptop_in_bbottom == minimum:
        player.rect.top = boundary.bottom
        velocity.y = 0
        return 2

    return 0