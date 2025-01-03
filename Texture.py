import pygame as pg
import moderngl as mgl

class Texture:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/sand-texture.jpg')
        self.textures['boat'] = self.get_texture(path='objects/boat/boat.jpg')
        self.textures['beach_ball'] = self.get_texture(path='objects/beach_ball/Beach_Ball_diffuse.jpg')
        self.textures['beach_towels'] = self.get_texture(path='objects/beach_towels/Beach_Towels_diffuse.jpg')
        self.textures['umbrella'] = self.get_texture(path='objects/umbrella/10243_Patio_Umbrella_Open_v1_Diffuse.jpg')
        self.textures['skybox'] = self.get_texture_cube(dir_path='textures/skybox/', ext='png')
        self.textures['depth_texture'] = self.get_depth_texture()

    def get_depth_texture(self):
        depth_texture = self.ctx.depth_texture(self.app.WIN_SIZE)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def get_texture_cube(self, dir_path, ext='png'):
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f'{face}.{ext}').convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))

        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()

        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
