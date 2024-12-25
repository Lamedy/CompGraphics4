from VBO import VBO
from ShaderProgram import ShaderProgram

class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        # куб vao
        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['cube'])
        # тень куба vao
        self.vaos['shadow_cube'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo = self.vbo.vbos['cube'])

        # лодка vao
        self.vaos['boat'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['boat'])
        # тень лодки vao
        self.vaos['shadow_boat'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['boat'])

        # Пляжный мяч vao
        self.vaos['beach_ball'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['beach_ball'])
        # Тень пляжного мяча vao
        self.vaos['shadow_beach_ball'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['beach_ball'])

        # Пляжное полотенце vao
        self.vaos['beach_towels'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['beach_towels'])
        # Тень пляжного полотенца vao
        self.vaos['shadow_beach_towels'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['beach_towels'])

        # Зонтик vao
        self.vaos['umbrella'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['umbrella'])
        # Тень зонтика vao
        self.vaos['shadow_umbrella'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['umbrella'])

        # skybox vao
        self.vaos['skybox'] = self.get_vao(
            program=self.program.programs['skybox'],
            vbo=self.vbo.vbos['skybox'])

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True)
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()
