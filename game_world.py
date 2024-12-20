import pickle

world = [[] for _ in range(3)]
collision_pairs = {}

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[],[]]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def add_object(o, depth = 0):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o) # world에서 o를 삭제
            remove_collision_object(o) # collision pairs에서 o를 삭제
            del o # 메모리에서 o를 삭제
            return
    raise ValueError('Cannot delete non existing object')

def clear():
    for layer in world:
        layer.clear()

def collide(a, b):
    al,ab,ar,at = a.get_bb()
    bl,bb,br,bt = b.get_bb()

    if ar < bl: return False
    if al > br: return False
    if at < bb: return False
    if ab > bt: return False
    return True

def head_collide(a, b):
    al,ab,ar,at = a.get_bb()
    bl,bb,br,bt = b.get_head_box()

    if ar < bl: return False
    if al > br: return False
    if at < bb: return False
    if ab > bt: return False
    return True

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if group == 'mario-on' and head_collide(a,b) == True:
                    print(f'{group} on')
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
                    return
                elif collide(a,b) == True and head_collide(a,b) == False:
                    print(f'{group} collide')
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
                    return

def all_objects():
    for layer in world:
        for obj in layer:
            yield obj


def save():
    game = [world, collision_pairs]
    with open('game.save', 'wb') as f:
        pickle.dump(game, f)


def load():
    global world, collision_pairs
    with open('game.save', 'rb') as f:
        game = pickle.load(f)
        world, collision_pairs = game[0], game[1]