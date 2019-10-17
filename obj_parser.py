import glm


class ObjParser:
    def __init__(self):
        self.uv = []
        self.vertices = []
        self.normals = []

    def get_shape(self, file):
        f = open(file, 'r')
        while True:
            line = f.readline()
            if not line:
                break
            if "v " in line:
                line = line[2:]
                v_list = [float(i) for i in line.split(" ")]
                v = glm.vec3(v_list[0], v_list[1], v_list[2])
                self.vertices.append(v)
            elif "vt " in line:
                line = line[3:]
                vt_list = [float(i) for i in line.split(" ")]
                vt = glm.vec(vt_list[0], vt_list[1])
                self.uv.append(vt)
            elif "vn " in line:
                line = line[3:]
                vn_list = [float(i) for i in line.split(" ")]
                vn = glm.vec3(vn_list[0], vn_list[1], vn_list[2])
                self.normals.append(vn)
            elif "f " in line:
                pass
                # TODO
            # TODO => process data and create shape
        f.close()

ObjParser().get_shape("resources/cube.obj")  # for testing purpose
