import numpy as np
import os
from scipy.spatial import ConvexHull



def my_print(fp, s):
    print(s)
    fp.write(s + '\n')


def rotationArc(v0, v1):
    cross = np.cross(v0, v1)
    d = np.dot(v0, v1)
    s = np.sqrt((1 + d) * 2)
    if np.abs(s) <= 1e-15:
        return -1, None
    cross = cross / s
    return 0, np.concatenate([cross, [s * 0.5]])


def quatToMatrix(quat):
    xx = quat[0] * quat[0]
    yy = quat[1] * quat[1]
    zz = quat[2] * quat[2]
    xy = quat[0] * quat[1]
    xz = quat[0] * quat[2]
    yz = quat[1] * quat[2]
    wx = quat[3] * quat[0]
    wy = quat[3] * quat[1]
    wz = quat[3] * quat[2]

    matrix = np.eye(4)
    matrix[0, 0] = 1 - 2 * (yy + zz)
    matrix[1, 0] = 2 * (xy - wz)
    matrix[2, 0] = 2 * (xz + wy)

    matrix[0, 1] = 2 * (xy + wz)
    matrix[1, 1] = 1 - 2 * (xx + zz)
    matrix[2, 1] = 2 * (yz - wx)

    matrix[0, 2] = 2 * (xz - wy)
    matrix[1, 2] = 2 * (yz + wx)
    matrix[2, 2] = 1 - 2 * (xx + yy)

    # matrix[3, 0] = matrix[3, 1] = matrix[3, 2] = 0.0
    # matrix[0, 3] = matrix[1, 3] = matrix[2, 3] = 0.0
    # matrix[3, 3] = 1.0
    return matrix


def planeToMatrix(plane):
    ref = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    for i in range(3):
        check, quat = rotationArc(ref[i], plane[:3])
        if check == 0:
            break
    matrix = quatToMatrix(quat)
    matrix[3, 0] = matrix[1, 0] * -plane[3] + matrix[3, 0]
    matrix[3, 1] = matrix[1, 1] * -plane[3] + matrix[3, 1]
    matrix[3, 2] = matrix[1, 2] * -plane[3] + matrix[3, 2]
    return matrix


def computeBestFitPlane(verts):
    vcount = verts.shape[0]
    kOrigin = np.mean(verts, 0)
    kDiff = verts - kOrigin
    C = np.dot(kDiff.T, kDiff) / vcount
    _, ev = np.linalg.eigh(C)
    plane = np.zeros(4)
    kNormal = ev[:, 0]
    ax = np.argmax(np.abs(kNormal))
    if kNormal[ax] < 0:
        kNormal = -kNormal
    plane[0] = kNormal[0]
    plane[1] = kNormal[1]
    plane[2] = kNormal[2]
    plane[3] = -np.dot(kNormal, kOrigin)
    return plane


def eulerToQuat(roll, pitch, yaw):
    roll *= 0.5
    pitch *= 0.5
    yaw *= 0.5
    cr = np.cos(roll)
    cp = np.cos(pitch)
    cy = np.cos(yaw)
    sr = np.sin(roll)
    sp = np.sin(pitch)
    sy = np.sin(yaw)
    cpcy = cp * cy
    spsy = sp * sy
    spcy = sp * cy
    cpsy = cp * sy
    quat = np.zeros(4)
    quat[0] = sr * cpcy - cr * spsy
    quat[1] = cr * spcy + sr * cpsy
    quat[2] = cr * cpsy - sr * spcy
    quat[3] = cr * cpcy + sr * spsy
    return quat


def computeOBB(verts, matrix):
    p = verts - matrix[3, :3]
    p = np.dot(p, matrix[:3, :3].T)
    bmin = np.min(p, 0)
    bmax = np.max(p, 0)
    sides = bmax - bmin
    center = (bmax + bmin) * 0.5
    matrix[3, 0] += matrix[0, 0] * center[0] + matrix[1, 0] * center[1] + matrix[2, 0] * center[2]
    matrix[3, 1] += matrix[0, 1] * center[0] + matrix[1, 1] * center[1] + matrix[2, 1] * center[2]
    matrix[3, 2] += matrix[0, 2] * center[0] + matrix[1, 2] * center[1] + matrix[2, 2] * center[2]
    return sides


def FitObb(verts):
    hull = ConvexHull(verts)
    verts = verts[hull.vertices]
    # compute AABB
    p_min = np.min(verts, 0)
    p_max = np.max(verts, 0)
    scale = p_max - p_min
    avolume = scale[0] * scale[1] * scale[2]
    # compute best fit plane
    plane = computeBestFitPlane(verts)
    # convert a plane equation to a 4x4 rotation matrix
    matrix = planeToMatrix(plane)
    # computeOBB
    sides = computeOBB(verts, matrix)
    volume = sides[0] * sides[1] * sides[2]
    # rotation
    stepSize = 3  # FS_SLOW_FIT
    FM_DEG_TO_RAD = ((2.0 * np.pi) / 360.0)
    refmatrix = matrix.copy()
    for a in range(0, 180, stepSize):
        quat = eulerToQuat(0, a * FM_DEG_TO_RAD, 0)
        matrix_tmp = quatToMatrix(quat)
        pmatrix = np.dot(matrix_tmp, refmatrix)
        psides = computeOBB(verts, pmatrix)
        v = psides[0] * psides[1] * psides[2]
        if v < volume:
            volume = v
            sides = psides.copy()
            matrix = pmatrix.copy()
    if avolume < volume:
        matrix = np.eye(4)
        matrix[3, 0] = (p_max[0] + p_min[0]) * 0.5
        matrix[3, 1] = (p_max[1] + p_min[1]) * 0.5
        matrix[3, 2] = (p_max[2] + p_min[2]) * 0.5
        sides = scale
    Axis0 = matrix[0, :3]
    Axisl = matrix[1, :3]
    Axis2 = matrix[2, :3]
    center = matrix[3, :3]
    return np.concatenate([center, Axis0, Axisl, Axis2, sides], 0)


def getInterval(obb, axis):
    def projectPoint(p, axis):
        dot = axis.dot(p)
        return dot * np.linalg.norm(p, 2)

    # 获取obb 中心点 xyz 坐标
    centroid = obb[:3]
    # 三个轴方向的距离
    l1 = obb[3:6] * obb[-3] * 0.5
    l2 = obb[6:9] * obb[-2] * 0.5
    l3 = obb[9:12] * obb[-1] * 0.5
    min_ = None
    max_ = None
    for i in range(2):
        for j in range(2):
            for k in range(2):
                point = centroid + l1 * (i * 2 - 1) + \
                        l2 * (j * 2 - 1) + l3 * (k * 2 - 1)
                v = projectPoint(point, axis)
                if not min_ and not max_:
                    min_ = v
                    max_ = v
                else:
                    min_ = min(min_, v)
                    max_ = max(max_, v)
    return min_, max_


def save_obb(fn, objs):
    """
    save_obj: 0: not save;  1: save as one obj file; 2: save as independent objs
    """
    template1 = ' '.join(['%g'] * 15) + '\n'
    if not os.path.exists(os.path.dirname(fn)):
        os.makedirs(os.path.dirname(fn))
    with open(fn, 'w') as fp:
        for o in objs:
            fp.write(template1 % tuple(o))
