from os.path import join, dirname

from OCC.Display.SimpleGui import init_display

from cadracks_core.model import AnchorablePart, Assembly
from cadracks_core.joints import Joint
from cadracks_core.display import display_anchorable_part


b = AnchorablePart.from_stepzip(join(dirname(__file__),
                                     "./cad/robotic_arm/parts/base.zip"), name="base")
bp = AnchorablePart.from_stepzip(join(dirname(__file__),
                                      "./cad/robotic_arm/parts/base_plate.zip"),
                                 name="base_plate")
a1 = AnchorablePart.from_stepzip(join(dirname(__file__),
                                      "./cad/robotic_arm/parts/arm_1.zip"),
                                 name="arm_1")


def build(ang_1=0., ang_2=0.):

    assembly = Assembly(root_part=b, name="main")
    at, jo = assembly.add_part(part_to_add=bp,
                               part_to_add_anchors=["Plate_axis"],
                               receiving_parts=[b],
                               receiving_parts_anchors=["A1"],
                               links=[Joint(anchor=b.transformed_anchors['A1'], rx=ang_1)])

    at1, jo1 = assembly.add_part(part_to_add=a1,
                                 part_to_add_anchors=["E1"],
                                 receiving_parts=[bp],
                                 receiving_parts_anchors=["Arm_axis"],
                                 links=[Joint(anchor=bp.transformed_anchors['Arm_axis'], ry=ang_2)])

    return assembly


display, start_display, add_menu, add_function_to_menu = init_display()
display.SetRaytracingMode()
# display.FitAll()

# a = build()

colors = ["BLUE", "CYAN", "ORANGE"]

for i in range(10):
    ang_1 = 0.1 * i
    ang_2 = -0.1 * i
    a = build(ang_1, ang_2)
    # display.EraseAll()
    for j, p in enumerate(a._parts):
        display_anchorable_part(display, p, color=colors[j], update=False)
    display.Repaint()
    if i == 0:
        display.FitAll()

start_display()