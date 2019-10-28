import glm
import numpy


class ObjParser:
    """
    simple .obj files parser, won't work with articulated obj or any complex .obj file
    -Only vertices, normals and texture coordinates are processed
    """
    def __init__(self):
        self.uv = []
        self.vertices = []
        self.normals = []
        self.indices = []
        self.out_vertices = []
        self.out_normals = []
        self.out_uvs = []
        self.out_indices = []
        self.indexed_vertices = []
        self.indexed_normals = []
        self.indexed_uvs = []
        self.tmp_index = 0

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
            self.out_uvs.append(self.uv[i[1] - 1])
            self.out_normals.append(self.normals[i[2] - 1])
        #self.out_vertices = numpy.array(self.out_vertices, dtype='f')
        #self.out_normals = numpy.array(self.out_normals, dtype='f')
        #self.out_uvs = numpy.array(self.out_uvs, dtype='f')
        self.index_vbo()

    @staticmethod
    def _is_near(v1, v2):
        return abs(v1 - v2) < 0.01

    def _get_similar_vertex_index(self, in_vertex, in_uv, in_normal):
        for i in range(len(self.indexed_vertices)):
            if (
                self._is_near(in_vertex[0], self.indexed_vertices[i][0]) and
                self._is_near(in_vertex[1], self.indexed_vertices[i][1]) and
                self._is_near(in_vertex[2], self.indexed_vertices[i][2]) and
                self._is_near(in_uv[0], self.indexed_uvs[i][0]) and
                self._is_near(in_uv[1], self.indexed_uvs[i][1]) and
                self._is_near(in_normal[0], self.indexed_normals[i][0]) and
                self._is_near(in_normal[1], self.indexed_normals[i][1]) and
                self._is_near(in_normal[2], self.indexed_normals[i][2])
            ):
                self.tmp_index = i
                return True
        return False

    def index_vbo(self):
        triangle_vertices_array = []
        for i in range(len(self.out_vertices)):
            self.tmp_index = 0
            found = self._get_similar_vertex_index(self.out_vertices[i], self.out_uvs[i], self.out_normals[i])
            if found:
                # self.out_indices.append(self.tmp_index)
                triangle_vertices_array.append(self.tmp_index)
            else:
                self.indexed_vertices.append(self.out_vertices[i])
                self.indexed_uvs.append(self.out_uvs[i])
                self.indexed_normals.append(self.out_normals[i])
                self.tmp_index = len(self.indexed_vertices) - 1
                triangle_vertices_array.append(self.tmp_index)
            if len(triangle_vertices_array) >= 3:
                self.out_indices.append(numpy.array(triangle_vertices_array, dtype='i2'))  # by default 'i' = 'i4' = int32  --> i2 = int16
                triangle_vertices_array.clear()

        self.indexed_vertices = numpy.array(self.indexed_vertices, dtype='f')
        self.indexed_uvs = numpy.array(self.indexed_uvs, dtype='f')
        self.indexed_normals = numpy.array(self.indexed_normals, dtype='f')
        self.out_indices = numpy.array(self.out_indices, dtype='i')
