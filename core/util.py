def get_up_down_face_coords(obbs):
    v = [[] for i in range(len(obbs))]
    for i, obb in enumerate(obbs):
        cent = obbs[i][:3]
        hsize0 = obbs[i][-3] * 0.5
        hsize1 = obbs[i][-2] * 0.5
        hsize2 = obbs[i][-1] * 0.5
        axis0 = obbs[i][3:6]
        axis1 = obbs[i][6:9]
        axis2 = obbs[i][9:12]
        # 计算上面四个个顶点

        v[i].append(cent + axis0 * hsize0 - axis1 * hsize1 - axis2 * hsize2)

        v[i].append(cent + axis0 * hsize0 + axis1 * hsize1 - axis2 * hsize2)

        v[i].append(cent - axis0 * hsize0 + axis1 * hsize1 - axis2 * hsize2)

        v[i].append(cent - axis0 * hsize0 - axis1 * hsize1 - axis2 * hsize2)

        v[i].append(cent + axis0 * hsize0 - axis1 * hsize1 + axis2 * hsize2)

        v[i].append(cent + axis0 * hsize0 + axis1 * hsize1 + axis2 * hsize2)

        v[i].append(cent - axis0 * hsize0 - axis1 * hsize1 + axis2 * hsize2)
        v[i].append(cent - axis0 * hsize0 + axis1 * hsize1 + axis2 * hsize2)
    # 计算下面四个顶点
    # print(v[i],v[i])
    return v
