import glm
import numpy
from check_opti import CheckOpti


class ObjParser:
    def __init__(self):
        self.uv = []
        self.vertices = []
        self.normals = []
        self.indices = []
        self.out_vertices = []
        self.out_normals = []
        self.out_uvs = []

    def get_shape(self, file):
        f = open(file, 'r')
        if not f:
            print("couldnt open %s obj file", file)
            return 0
        while True:
            line = f.readline()
            if not line:
                break
            if "v " in line:
                line = line[2:]
                v_list = [float(i) for i in line.split(" ")]
                v = [v_list[0], v_list[1], v_list[2]]
                self.vertices.append(v)
            elif "vt " in line:
                line = line[3:]
                vt_list = [float(i) for i in line.split(" ")]
                vt = [vt_list[0], vt_list[1]]
                self.uv.append(vt)
            elif "vn " in line:
                line = line[3:]
                vn_list = [float(i) for i in line.split(" ")]
                vn = [vn_list[0], vn_list[1], vn_list[2]]
                self.normals.append(vn)
            elif "f " in line:
                line = line[2:]
                line = line.strip("\n")
                for i in line.split(" "):
                    list = []
                    list.append([int(j) for j in i.split("/")])
                    list = list[0]
                    self.indices.append(list)
        f.close()
        self.process_data()

    def process_data(self):
        for i in self.indices:
            self.out_vertices.append(self.vertices[i[0] - 1])
        self.out_vertices = numpy.array(self.out_vertices, dtype='f')
        # TODO out_normals and out_uvs
