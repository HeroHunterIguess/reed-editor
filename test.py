### test 


import pyglet, rendering

window = pyglet.window.Window(1000, 650)

@window.event
def on_draw():
    window.clear()

pyglet.app.run()


