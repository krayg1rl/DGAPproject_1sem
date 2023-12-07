def circles_collide(obj1, obj2):
    return (obj1.pos - obj2.pos).magnitude_squared < (obj1.r + obj2.r)**2

#def rects_collide(obj1, obj2)