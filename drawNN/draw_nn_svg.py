import numpy as np
from collections import defaultdict

svg_width = 500
svg_height = 500
nn_structure = (2,3,1)
desc = ("x", "h", "y")

add_node_desc = True
add_edge_desc = True

padding_x, padding_y = (50, 50)
r = 10

c = '<circle cx="%s" cy="%s" r="10" stroke="black" fill="white"></circle>'
l = '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="black" marker-end="url(#markerArrow)"></line>'
xl = '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="black" id="%s" marker-end="url(#markerArrow)"></line>'
xl_t = '''<text><textPath xlink:href="#%s" fill="grey" font-size="0.6em" startOffset="60@" >W
        <tspan dy="-8" font-size="0.6em">(%s)</tspan>
        <tspan dy="7" dx="-7" font-size="0.6em">%s</tspan>
        </textPath></text>'''
arrow = '''<defs>
    <marker id="markerArrow" markerWidth="13" markerHeight="13" refX="2" refY="2" orient="auto">
        <path d="M0,0 L6,2 L0,4 L0,0" />
    </marker>
</defs>
'''
t = '<text x="%s" y="%s" fill="grey" font-size="0.8em">%s<tspan baseline-shift="sub" font-size="0.7em">%s</tspan></text>'
svg = '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%s" height="%s">%s</svg>'''

layers = len(nn_structure)
points = defaultdict(list)
max_n = 5
a = (svg_height/2 - padding_y)/(max_n - 1)
x_pos = np.linspace(padding_x, svg_width-padding_x, layers)
for index,i in enumerate(nn_structure):
    y_li = min((i-1)*a, svg_height/2 - padding_y)
    y_pos = np.linspace(svg_height/2+y_li, svg_height/2-y_li, i)
    p = [(int(x_pos[index]),int(y)) for y in y_pos]
    points[index] = p
content = arrow

#Draw edges
i = 0
while i< layers-1:
    links = [(x1,y1,x2,y2, i1,i2) for i1,(x1,y1) in enumerate(points[i]) for i2,(x2,y2) in enumerate(points[i+1])]
    for index,ii in enumerate(links):
        ii, ie = ii[:4], ii[4:]
        d = np.sqrt((ii[0]-ii[2])**2 + (ii[1]-ii[3])**2)
        xy_ = (int(ii[2]-r*(ii[2]-ii[0])/d)-2, int(ii[3]+r*(ii[1]-ii[3])/d))
        if add_edge_desc:
            id_ = "edge"+str(i)+str(index)
            content += xl%(ii[:2] + xy_ + (id_,)) 
            content += (xl_t%(id_, i+1, str(ie[0])+","+str(ie[1]))).replace("@", "%")
        else:
            content += l%(ii[:2] + xy_)
    i += 1

#Draw nodes
for i in range(layers):
    content += '/n'.join([c%ii for ii in points[i]])
    if add_node_desc:
        content += '/n'.join([t%((value[0]-5,value[1]+3)+(desc[i], str(index))) for index,value in enumerate(points[i])])

#input&output arrow
content += "/n".join([l%(i[0]-40,i[1],i[0]-r-3,i[1]) for i in points[0]])
content += "/n".join([l%(i[0]+r,i[1],i[0]+r+30,i[1]) for i in points[layers-1]])

with open("nn.svg", "w+") as f:
    f.write(svg%(svg_width, svg_height, content))

