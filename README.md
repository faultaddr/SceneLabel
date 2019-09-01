# SceneLabel
This is an example of PyQt5 + pyopengl. Mouse rotation, translation, and zoom is referenced from Pangolin.

## required Libraries
* PyQt5
* pyopengl
* numpy

## functions
* label the point cloud data 
* label the mesh data
* label the AABB/OBB data
* export labeled result
* visualized view

---

<center style="position:absolute;top:0;right:0;width:5%;height:5%">
![avatar](https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1567522041&di=cffc73300d37423c2023e8c03f3ffc8a&imgtype=jpg&er=1&src=http%3A%2F%2Ffiles.eduuu.com%2Fimg%2F2015%2F01%2F05%2F142329_54aa2de1b3046.jpg)
</center>
<center style="position:absolute;top:0;right:5%;width:5%;height:5%">
![avarar](https://gss1.bdstatic.com/9vo3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike80%2C5%2C5%2C80%2C26/sign=103631955c4e9258b2398ebcfdebba3d/8718367adab44aed37666715b91c8701a18bfb13.jpg)
</center>

## <center>计算机图形学课程设计报告</center>

---

<br></br>
<br></br>
<br></br>
<center style="position:relative;width:100%;height=auto">![avatar](https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=3501382343,3988719200&fm=26&gp=0.jpg)</center>
<br></br>
<br></br>
<br></br>
<br></br>
<br></br>
<br></br>
<br></br>
<center>
### 姓名：<u>潘云逸</u>

### 学号：<u>MG1833058</u>

### 项目名称：<u>SceneLabel Tool</u>

</center>

---
<br></br>
### 设计背景：

&emsp;&emsp;自从深度学习日益火热，三维视觉也逐渐吸引了更多研究人员积极参与，但三维数据格式多种多样，一个成熟的用于标注以产生大规模训练数据的工具应运而生。SceneLabel Tools 主要用于层次化的分割组织场景，将instance level 的点云、面片数据组成成树状结构，将场景自底向上组织成多叉树结构，这样不论是在目标检测还是分割等领域上都有着重要的作用。为了实现这一目标，我采用了pyqt5 作为GUI的基础库，结合pyOpenGL进行场景的绘制、渲染等工作，并提供简单的标注手段，能够对Scannet、S3DIS等公共数据集自行进行组织标注。

### 设计细节：
- #### 基于python 3.6.9 进行编写 各依赖库版本如下：

    - PyQt 5.9.2
    - pyopengl 3.1.1a1
    - qt 5.9.7
    - open3d-python 0.7.0.0 (如果需要使用面片标注工具 必须从源码编译)
    - numpy 1.16.4 (版本需要)
    - imageio
    - pillow

- #### 界面设计：
    - **OBB 标注**：

    &emsp;&emsp; 通过计算OBB和AABB 将OBB或者AABB 通过opengl画出

    - **Mesh 标注**：

    &emsp;&emsp;Mesh 标注的过程中，面片数据需要加上纹理和光照信息以便于数据可视化和标注工作，故Mesh标注工具进行了光照和纹理渲染。

    - **PointCloud 标注**：

    &emsp;&emsp;PointCloud 标注过程中，则基本使用原始的点云信息，未进行光照渲染。

-  #### 功能设计：


    - **标注功能**:
    
    &emsp;&emsp;基本的业务逻辑包括 点选、合并、撤销、写入、一键写入、写入后的检查功能等。

    &emsp;&emsp;OBB标注主要包含 相互关系的标注（旋转对称支撑平移等，本质上还是关系标注）

#### 实现细节：

- **OBB标注**：

	&emsp;&emsp;首先读入点云数据求取instance level的bounding box，再通过OpenGL绘制出bounding box 的边界，进行显示。点云数据作为辅助显示帮助标注人员进行更好的标注。

	- 基础显示
	
	![](/home/panyunyi/Desktop/DeepinScreenshot_select-area_20190828101831.png) 
	
	- 显示组合AABB
	
	![](/home/panyunyi/Desktop/DeepinScreenshot_select-area_20190828101903.png)
	 
	- 显示点云便于可视化标注
	
	![ ](/home/panyunyi/Desktop/DeepinScreenshot_select-area_20190828101918.png  "显示点云")
	
	- 显示可选关系
	
	![](/home/panyunyi/Desktop/DeepinScreenshot_select-area_20190828102321.png) 
	
	- 标注关系后进行查看
	
	![](/home/panyunyi/Desktop/DeepinScreenshot_select-area_20190828102444.png) 
	


- **Mesh 标注**：

	&emsp;&emsp; 读入面片信息，通过OpenGL渲染绘制纹理光照和基础的面片Triangle，进行显示。
	
	- 基础显示
	![](/home/panyunyi/Desktop/DeepinScreenshot_select-area_20190828104605.png) 
	
	- 显示组合Mesh
	
	![](/home/panyunyi/Desktop/DeepinScreenshot_select-area_20190828104729.png) 
	
	- 显示待合并面片并进行合并
	![](/home/panyunyi/Desktop/DeepinScreenshot_select-area_20190828104713.png) 
	
- **点云标注**：

	&emsp;&emsp; 读入点云信息，通过OpenGL绘制渲染以便于显示
	
	- 基础显示
	![](/home/panyunyi/Desktop/DeepinScreenshot_select-area_20190828105605.png) 
	
	- 显示进度条
	![](/home/panyunyi/Desktop/DeepinScreenshot_select-area_20190828105619.png) 
	
	- 显示选中instance （可进行合并 更改label等操作）
	![](/home/panyunyi/Desktop/DeepinScreenshot_select-area_20190828105841.png) ![](/home/panyunyi/Desktop/DeepinScreenshot_select-area_20190828105903.png) 
	
	
### 代码细节：

- **OBB求取**：

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

- **VBO机制**：

	因为在绘制过程中，需要旋转 平移等各类导致画面重新绘制的操作，所以每次都进行绘制计算并不合理，在这里我们使用了VBO机制。

	- VBO就是通过几个函数，是显卡存储空间里一块缓存区BUFFER，用于存储和顶点以及其属性相关的信息（顶点信息，颜色信息，法线信息，纹理坐标信息和索引信息等），那么为什么会产生这种方式呢？

	- 解决什么问题: 由于最早的openGL不支持实例化绘制，导致在绘制大量相似图元的时候，需要反复向GPU提交代码渲染，这点在OpenGL中的二次方图元和实例化绘制已经提到过了，会严重导致瓶颈效应。

	- VBO其实就是显卡中的显存，为了提高渲染速度，可以将要绘制的顶点数据缓存在显存中，这样就不需要将要绘制的顶点数据重复从CPU发送到GPU, 浪费带宽资源。
	

			def create_vbo(self, id_list_str):
				if self.data:
				    buffers_list = []
				    lens = []
				    for single_data in self.data:
					vex = single_data[0]
					color = single_data[1]
					index = np.arange(len(vex))
					buffers = glGenBuffers(3)
					glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
					glBufferData(GL_ARRAY_BUFFER, (ctypes.c_float * len(vex))(*vex), GL_STATIC_DRAW)
					glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
					glBufferData(GL_ARRAY_BUFFER, (ctypes.c_float * len(color))(*color), GL_STATIC_DRAW)
					glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[2])
					glBufferData(GL_ELEMENT_ARRAY_BUFFER,
						     (ctypes.c_int * len(index))(*index),
						     GL_STATIC_DRAW)
					buffers_list.append(buffers)
					lens.append(len(vex))
				    return buffers_list, lens
				else:
				    return [], 0
	

- **多线程加载**：

	在点云、面片等数据进行加载的过程中，因为数据集的原因，需要绘制一百多万个点，在使用了VBO之后，首次加载还是会非常缓慢，最大的场景需要9.6秒才能完全加载成功，因此在考虑数据分布后发现各个instance的数据加载并不需要顺序执行，这给我们提供了天然的便利，即能够天然的进行并行加载，由于python 默认的cython解释器在多线程加载的问题上不能很好的提升效率，我们使用multiprocessing 来进行多进程加载。

		pool = ProcessPoolExecutor(max_workers=16)
		result = list(pool.map(process_data, [str(y) for y in self.hier_data]))
			
	 	from concurrent.futures import ProcessPoolExecutor
	 		
	 	def process_data(d):
		    data = eval(d)
		    if data['parent'] == -1:
			instance_path = data['path']
			instance_label = data['label']
			v = []
			c = []
			mean_xyz = [0, 0, 0]
			for instance in instance_path:
			    new_path = '/'.join(instance.split('/')[0:4]) + '/gt/' + '/'.join(instance.split('/')[4:])
			    new_path = new_path.replace('.txt', '_color01.txt')
			    original_data = np.loadtxt(new_path)
			    vex = original_data[:, :3]
			    mean_xyz = np.mean(vex, axis=0)
			    color = original_data[:, 3:6]
			    vex = np.reshape(vex, (1, -1))
			    color = np.reshape(color, (1, -1))
			    v.extend(vex.tolist()[0])
			    c.extend(color.tolist()[0])
			return (v, c), instance_label, mean_xyz, data['id']
			
- **TTL Cache**

	只有指定存活时长的Cache，通过Cache机制，使得在二次打开同一个点云数据时，不需要再计算VBO，直接从Cache Pool中取出即可进行渲染操作。
	
		from cachetools import LRUCache, RRCache, cachedmethod, cached, TTLCache
		cache = TTLCache(maxsize=400, ttl=300)
	

### 后续工作

将功能整合后，作为一个整体发布，能够自行判别数据类型并提供OBB、法向量等辅助计算工具。
软件将在github开源，基本遵循Apache协议，保留专利权，不允许修改和商用，若为科研目的则必须在作者列表注明。开源地址和主页为：

开源地址：[https://github.com/panyunyi97/SceneLabel](https://github.com/panyunyi97/SceneLabel).

项目主页：[www.panyunyi.cn/SceneLabel](www.panyunyi.cn/SceneLabel)
