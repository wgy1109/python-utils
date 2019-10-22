from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import Polygon

from shapely.ops import snap
import shapely.geos
from shapely.wkb import dumps, loads
from shapely.geometry import mapping

print("---------------Point-----------------")
point = Point(0, 0)
# geom_type 显示属性
print(point.geom_type)
# distance 两点间距离
len = Point(0,0).distance(Point(1,1))
# round 保留 n 位小数
print(round(len,3))
# bounds
print(point.bounds)
# coords 坐标，坐标值通过坐标 x、y、z 属性访问
print(list(point.coords))
print(point.x)
print(point.y)
# print("x 坐标： "+point.x+", y 坐标： "+point.y)
# has_z 二维点 返回 false； 三维点 返回 true
print(Point(0,0).has_z)
print(Point(0,0,0).has_z)
# buffer 缓冲器，如果是个点，会缓冲出一个圆，
print(point.buffer(10.0).area)
# buffer 缓冲区分辨率为1 时，为方形补丁
print(point.buffer(10.0, 1).area)
# wkt 文本， wkb二进制文件，   Point(0,0).wkb.encode('hex')  ==  wkb_hex
print(point.wkt)
print(point.wkb_hex)
# 将几何对象序列化为二进制或文本字符串， 使用 dumps(),
# 反序列化字符串并获取适当类型的新几何对象， 使用 loads()
wkt = dumps(point)
print(wkt)
print(loads(wkt).wkt)
# mapping
class GeoThing(object):
    def __init__(self, d):
        self.__geo_interface__ = d

thing = GeoThing({"type":"Point", "coordinates":(0.0, 0.0)})
m = mapping(thing)
print("" , m['type'])
print(m['coordinates'])

print("---------------LineStriing-----------------")
line = LineString([(2,0),(2,2),(0,2)])
# area 面积
print(line.area)
# length 长度
print(line.length)
# hausdorff_distance  豪斯多夫 距离
print(point.hausdorff_distance(line))
print(point.distance(Point(2,2)))
print(list(line.coords))
print(line.coords[0])
print(line.coords[1:])
for x, y in line.coords:
    print("x = {}，y = {} ".format(x,y))
# == 和 equals 的区别
a = LineString([(0,0),(1,1)])
b = LineString([(0,0),(0.5,0.5),(1,1)])
c = LineString([(0,0),(0,0),(1,1)])
print(a.equals(b))
print(a == b)
print(b.equals(c))
print(b == c)
# contains 包含于， within 被包含于
coords = [(0,0),(1,1)]
print("线包含点： ", LineString(coords).contains(Point(0.5,0.5)))
print("点被线包含：", Point(0.5,0.5).within(LineString(coords)))
# 端点不在线的包含内
print("端点不在线包含内： ",LineString(coords).contains(Point(1,1)))
# corsses 有重叠部分，不能是包含或 被包含
print(LineString(coords).crosses(LineString([(0,1),(1,0)])))
print(LineString(coords).crosses(LineString([(0,0),(0.5,0.5)])))
# is_simple 如果功能本身不交叉，则返回 true
print(LineString([(0,0),(1,1),(1,-1),(0,1)]).is_simple)


print("---------------Polygon-----------------")
polygon = Polygon([(0,0),(0,2),(2,2),(2,0)])
print(polygon.area)
print(polygon.length)
# bounds 边界框 （最小、最小、最大、最大）元组
print(polygon.bounds)
# 组件 环， exterior 外部、 interiors 内部
print(list(polygon.exterior.coords))
print(list(polygon.interiors))


print("---------------snap-----------------")
square = Polygon([(1,1),(2,1),(2,2),(1,2),(1,1)])
line = LineString([(0,0),(0.8,0.8),(1.8,0.95),(2.6,0.5)])
result = snap(line, square, 0.5)
print(result.wkt)

# 未成功测试， substring
# line = LineString(([0, 0], [2, 0]))
# result = substring(line, 0.5, 0.6)
# print(result.wkt)

print("---------------geos-----------------")
print("shapely version : ", shapely.__version__)
print("shapely geos version : ", shapely.geos.geos_version)
print("shapely geos version string : ", shapely.geos.geos_version_string )

