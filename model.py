import moderngl as mgl
import numpy as np
import glm


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.pos = pos
        self.vao_name = vao_name
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()

        m_model = glm.translate(m_model, self.pos)

        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))

        m_model = glm.scale(m_model, self.scale)
        return m_model

    def render(self):
        self.update()
        self.vao.render()


class ExtendedBaseModel(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos, rot, scale):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.texture.use(location=0)
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def update_shadow(self):
        self.shadow_program['m_model'].write(self.m_model)

    def render_shadow(self):
        self.update_shadow()
        self.shadow_vao.render()

    def on_init(self):
        self.program['m_view_light'].write(self.app.light.m_view_light)

        self.program['u_resolution'].write(glm.vec2(self.app.WIN_SIZE))

        self.depth_texture = self.app.mesh.texture.textures['depth_texture']
        self.program['shadowMap'] = 1
        self.depth_texture.use(location=1)

        self.shadow_vao = self.app.mesh.vao.vaos['shadow_' + self.vao_name]
        self.shadow_program = self.shadow_vao.program
        self.shadow_program['m_proj'].write(self.camera.m_proj)
        self.shadow_program['m_view_light'].write(self.app.light.m_view_light)
        self.shadow_program['m_model'].write(self.m_model)

        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use(location=0)

        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)


class Cube(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class Boat(ExtendedBaseModel):
    def __init__(self, app, vao_name='boat', tex_id='boat',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class Beach_Ball(ExtendedBaseModel):
    def __init__(self, app, vao_name='beach_ball', tex_id='beach_ball',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class Beach_Towels(ExtendedBaseModel):
    def __init__(self, app, vao_name='beach_towels', tex_id='beach_towels',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class Umbrella(ExtendedBaseModel):
    def __init__(self, app, vao_name='umbrella', tex_id='umbrella',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class SkyBox(ExtendedBaseModel):
    def __init__(self, app, vao_name='skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))

    def on_init(self):

        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)

        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))