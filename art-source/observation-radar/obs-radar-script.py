import bpy
import math
import os
from mathutils import Vector

# ============================================================
# FACTORIO OBSERVATION RADAR
# Blender 4.3.2
#
# TWO-OUTPUT ASSET PIPELINE
#
# 1. Inventory image:
#       inventory.png
#
#    - three-quarter / ~45 degree orthographic presentation
#    - one deliberately chosen radar-head orientation
#
# 2. Placed entity:
#       placed_frames/radar_00.png ... radar_15.png
#       placed_4x4_atlas.png
#
#    - almost-overhead
#    - front-aligned camera
#    - 16 exact head rotations at 22.5 degrees
# ============================================================


# ============================================================
# OUTPUT
# ============================================================

OUTPUT_DIR = os.path.join(
    os.path.expanduser("~"),
    "factorio_radar_output"
)

PLACED_FRAMES_DIR = os.path.join(
    OUTPUT_DIR,
    "placed_frames"
)

INVENTORY_PATH = os.path.join(
    OUTPUT_DIR,
    "inventory.png"
)

PLACED_ATLAS_PATH = os.path.join(
    OUTPUT_DIR,
    "placed_4x4_atlas.png"
)

RENDER_INVENTORY = True
RENDER_PLACED_ANIMATION = True
BUILD_PLACED_ATLAS = True

FRAME_SIZE = 256

TOTAL_FRAMES = 16
ANGLE_STEP_DEG = 360.0 / TOTAL_FRAMES

ATLAS_COLS = 4
ATLAS_ROWS = 4


# ============================================================
# INVENTORY PRESENTATION
# ============================================================

# Three-quarter camera.
#
# Positive X + negative Y gives us the familiar diagonal
# inventory presentation.
INVENTORY_CAMERA_LOCATION = (
    7.4,
    -7.4,
    7.7
)

INVENTORY_TARGET = (
    0.0,
    0.0,
    0.85
)

INVENTORY_ORTHO_SCALE = 5.25

# This is independent from placement frame 0.
#
# Adjust this one variable if another orientation gives
# a better inventory silhouette.
#
# 157.5 gives a reasonably expressive three-quarter dish pose.
INVENTORY_HEAD_ANGLE_DEG = 157.5


# ============================================================
# PLACED-ENTITY PRESENTATION
# ============================================================

# Camera lies directly on the object's front/back axis:
#
#       X = 0
#
# so there is no 45-degree azimuth rotation.
#
# The high Z value makes the presentation almost overhead,
# while the negative Y position keeps enough tilt to expose
# the entity's height and front face.
PLACED_CAMERA_LOCATION = (
    0.0,
    -6.2,
    11.5
)

PLACED_TARGET = (
    0.0,
    0.0,
    0.80
)

PLACED_ORTHO_SCALE = 4.75


# ============================================================
# RADAR HEAD GEOMETRY
# ============================================================

HEAD_Z = 1.50

DISH_PIVOT_Z = 0.55
DISH_FORWARD_OFFSET = 0.34
DISH_TILT_DEG = 22.0

DISH_RADIUS = 0.88
DISH_DEPTH = 0.24
DISH_THICKNESS = 0.045

FEED_FORWARD = 0.66

RIB_COUNT = 8
RIM_CLAMP_COUNT = 8


# ============================================================
# TRUNNION
# ============================================================

TRUNNION_HALF_WIDTH = 0.42
TRUNNION_ARM_RADIUS = 0.075
TRUNNION_REAR_Y = -0.28
TRUNNION_Z = DISH_PIVOT_Z
REAR_PEDESTAL_TOP_Z = 0.40


# ============================================================
# LIGHTING
# ============================================================

SUN_ENERGY = 2.2
AREA_ENERGY = 1200
FILL_ENERGY = 450


# ============================================================
# SCENE RESET
# ============================================================

def clear_scene():

    bpy.ops.object.select_all(
        action='SELECT'
    )

    bpy.ops.object.delete(
        use_global=False
    )

    collections = [
        bpy.data.meshes,
        bpy.data.materials,
        bpy.data.cameras,
        bpy.data.lights,
        bpy.data.curves,
        bpy.data.images,
    ]

    for collection in collections:

        for block in list(collection):

            if block.users == 0:
                collection.remove(block)


clear_scene()

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

os.makedirs(
    PLACED_FRAMES_DIR,
    exist_ok=True
)


# ============================================================
# RENDER SETTINGS
# ============================================================

scene = bpy.context.scene

scene.render.engine = 'BLENDER_EEVEE_NEXT'

scene.render.resolution_x = FRAME_SIZE
scene.render.resolution_y = FRAME_SIZE
scene.render.resolution_percentage = 100

scene.render.film_transparent = True

scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'

try:
    scene.view_settings.look = 'AgX - Medium High Contrast'
except:
    pass


# ============================================================
# GENERAL HELPERS
# ============================================================

def add_empty(
    name,
    location=(0, 0, 0)
):

    bpy.ops.object.empty_add(
        type='PLAIN_AXES',
        location=location
    )

    obj = bpy.context.active_object
    obj.name = name

    return obj


def add_cube(
    name,
    location=(0, 0, 0),
    scale=(1, 1, 1),
    rotation=(0, 0, 0)
):

    bpy.ops.mesh.primitive_cube_add(
        location=location,
        rotation=rotation
    )

    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale

    return obj


def add_cylinder(
    name,
    radius,
    depth,
    location=(0, 0, 0),
    vertices=32,
    rotation=(0, 0, 0)
):

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation
    )

    obj = bpy.context.active_object
    obj.name = name

    return obj


def assign_material(
    obj,
    material
):

    if obj.data.materials:

        obj.data.materials[0] = material

    else:

        obj.data.materials.append(
            material
        )


def bevel(
    obj,
    width=0.01,
    segments=2
):

    mod = obj.modifiers.new(
        name="Bevel",
        type='BEVEL'
    )

    mod.width = width
    mod.segments = segments
    mod.limit_method = 'ANGLE'


def smooth(obj):

    if obj.type != 'MESH':
        return

    for polygon in obj.data.polygons:

        polygon.use_smooth = True


def add_arm(
    name,
    start,
    end,
    radius,
    material,
    parent=None,
    vertices=16
):

    p1 = Vector(start)
    p2 = Vector(end)

    direction = p2 - p1
    midpoint = (p1 + p2) / 2.0
    length = direction.length

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=length,
        location=midpoint
    )

    obj = bpy.context.active_object

    obj.name = name

    obj.rotation_mode = 'QUATERNION'

    obj.rotation_quaternion = (
        direction.to_track_quat(
            'Z',
            'Y'
        )
    )

    assign_material(
        obj,
        material
    )

    if parent is not None:

        obj.parent = parent

    smooth(obj)

    return obj


# ============================================================
# CAMERA HELPERS
# ============================================================

def point_camera_at(
    camera,
    target
):

    target_vec = Vector(target)

    direction = (
        target_vec
        - camera.location
    )

    # Blender cameras look down local -Z,
    # with local Y treated as "up".
    camera.rotation_euler = (
        direction
        .to_track_quat(
            '-Z',
            'Y'
        )
        .to_euler()
    )


def create_ortho_camera(
    name,
    location,
    target,
    ortho_scale
):

    camera_data = bpy.data.cameras.new(
        name + "_data"
    )

    camera = bpy.data.objects.new(
        name,
        camera_data
    )

    bpy.context.collection.objects.link(
        camera
    )

    camera.location = location

    camera.data.type = 'ORTHO'

    camera.data.ortho_scale = (
        ortho_scale
    )

    point_camera_at(
        camera,
        target
    )

    return camera


# ============================================================
# TAPERED HOUSING
# ============================================================

def create_tapered_box(
    name,
    bottom_x,
    bottom_y,
    top_x,
    top_y,
    height,
    z_bottom
):

    zb = z_bottom
    zt = z_bottom + height

    vertices = [

        (-bottom_x, -bottom_y, zb),
        ( bottom_x, -bottom_y, zb),
        ( bottom_x,  bottom_y, zb),
        (-bottom_x,  bottom_y, zb),

        (-top_x, -top_y, zt),
        ( top_x, -top_y, zt),
        ( top_x,  top_y, zt),
        (-top_x,  top_y, zt),
    ]

    faces = [

        (0, 1, 2, 3),
        (4, 7, 6, 5),

        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (3, 7, 4, 0),
    ]

    mesh = bpy.data.meshes.new(
        name + "_mesh"
    )

    mesh.from_pydata(
        vertices,
        [],
        faces
    )

    mesh.update()

    obj = bpy.data.objects.new(
        name,
        mesh
    )

    bpy.context.collection.objects.link(
        obj
    )

    return obj


# ============================================================
# MATERIALS
# ============================================================

def make_textured_material(
    name,
    dark_color,
    light_color,
    metallic,
    rough_low,
    rough_high,
    noise_scale,
    bump_scale,
    bump_strength
):

    mat = bpy.data.materials.new(
        name=name
    )

    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    nodes.clear()

    output = nodes.new(
        "ShaderNodeOutputMaterial"
    )

    output.location = (500, 0)

    bsdf = nodes.new(
        "ShaderNodeBsdfPrincipled"
    )

    bsdf.location = (220, 0)

    bsdf.inputs[
        "Metallic"
    ].default_value = metallic


    texcoord = nodes.new(
        "ShaderNodeTexCoord"
    )

    texcoord.location = (-900, 0)


    noise = nodes.new(
        "ShaderNodeTexNoise"
    )

    noise.location = (-650, 120)

    noise.inputs[
        "Scale"
    ].default_value = noise_scale

    noise.inputs[
        "Detail"
    ].default_value = 4.0

    noise.inputs[
        "Roughness"
    ].default_value = 0.68


    ramp = nodes.new(
        "ShaderNodeValToRGB"
    )

    ramp.location = (-380, 130)

    ramp.color_ramp.elements[
        0
    ].color = (
        *dark_color,
        1.0
    )

    ramp.color_ramp.elements[
        1
    ].color = (
        *light_color,
        1.0
    )


    roughness_ramp = nodes.new(
        "ShaderNodeValToRGB"
    )

    roughness_ramp.location = (
        -380,
        -40
    )

    roughness_ramp.color_ramp.elements[
        0
    ].color = (
        rough_low,
        rough_low,
        rough_low,
        1.0
    )

    roughness_ramp.color_ramp.elements[
        1
    ].color = (
        rough_high,
        rough_high,
        rough_high,
        1.0
    )


    fine_noise = nodes.new(
        "ShaderNodeTexNoise"
    )

    fine_noise.location = (
        -650,
        -240
    )

    fine_noise.inputs[
        "Scale"
    ].default_value = bump_scale

    fine_noise.inputs[
        "Detail"
    ].default_value = 3.0

    fine_noise.inputs[
        "Roughness"
    ].default_value = 0.6


    bump = nodes.new(
        "ShaderNodeBump"
    )

    bump.location = (
        -40,
        -220
    )

    bump.inputs[
        "Strength"
    ].default_value = bump_strength

    bump.inputs[
        "Distance"
    ].default_value = 0.025


    links.new(
        texcoord.outputs["Object"],
        noise.inputs["Vector"]
    )

    links.new(
        texcoord.outputs["Object"],
        fine_noise.inputs["Vector"]
    )

    links.new(
        noise.outputs["Fac"],
        ramp.inputs["Fac"]
    )

    links.new(
        noise.outputs["Fac"],
        roughness_ramp.inputs["Fac"]
    )

    links.new(
        ramp.outputs["Color"],
        bsdf.inputs["Base Color"]
    )

    links.new(
        roughness_ramp.outputs["Color"],
        bsdf.inputs["Roughness"]
    )

    links.new(
        fine_noise.outputs["Fac"],
        bump.inputs["Height"]
    )

    links.new(
        bump.outputs["Normal"],
        bsdf.inputs["Normal"]
    )

    links.new(
        bsdf.outputs["BSDF"],
        output.inputs["Surface"]
    )

    return mat


def make_emissive_material(
    name,
    color,
    strength=4.0
):

    mat = bpy.data.materials.new(
        name=name
    )

    mat.use_nodes = True

    bsdf = mat.node_tree.nodes[
        "Principled BSDF"
    ]

    bsdf.inputs[
        "Base Color"
    ].default_value = (
        *color,
        1.0
    )

    if "Emission Color" in bsdf.inputs:

        bsdf.inputs[
            "Emission Color"
        ].default_value = (
            *color,
            1.0
        )

    if "Emission Strength" in bsdf.inputs:

        bsdf.inputs[
            "Emission Strength"
        ].default_value = strength

    bsdf.inputs[
        "Roughness"
    ].default_value = 0.15

    return mat


MAT_BODY = make_textured_material(
    "ArmoredBody",
    dark_color=(0.20, 0.22, 0.22),
    light_color=(0.40, 0.42, 0.41),
    metallic=0.16,
    rough_low=0.60,
    rough_high=0.86,
    noise_scale=5.0,
    bump_scale=34.0,
    bump_strength=0.13
)


MAT_DECK = make_textured_material(
    "DarkTopDeck",
    dark_color=(0.12, 0.14, 0.15),
    light_color=(0.27, 0.30, 0.31),
    metallic=0.40,
    rough_low=0.42,
    rough_high=0.68,
    noise_scale=7.0,
    bump_scale=45.0,
    bump_strength=0.10
)


MAT_TRIM = make_textured_material(
    "StructuralSteel",
    dark_color=(0.065, 0.075, 0.085),
    light_color=(0.22, 0.25, 0.27),
    metallic=0.82,
    rough_low=0.24,
    rough_high=0.54,
    noise_scale=9.0,
    bump_scale=55.0,
    bump_strength=0.10
)


MAT_DARK = make_textured_material(
    "MachineryDark",
    dark_color=(0.04, 0.05, 0.055),
    light_color=(0.13, 0.15, 0.16),
    metallic=0.62,
    rough_low=0.32,
    rough_high=0.62,
    noise_scale=10.0,
    bump_scale=50.0,
    bump_strength=0.08
)


MAT_DISH = make_textured_material(
    "DishSteel",
    dark_color=(0.27, 0.34, 0.38),
    light_color=(0.58, 0.67, 0.71),
    metallic=0.92,
    rough_low=0.22,
    rough_high=0.46,
    noise_scale=10.0,
    bump_scale=48.0,
    bump_strength=0.07
)


MAT_COPPER = make_textured_material(
    "Copper",
    dark_color=(0.24, 0.08, 0.03),
    light_color=(0.72, 0.33, 0.10),
    metallic=0.94,
    rough_low=0.24,
    rough_high=0.46,
    noise_scale=11.0,
    bump_scale=45.0,
    bump_strength=0.05
)


MAT_BLUE = make_emissive_material(
    "BlueLight",
    (0.05, 0.45, 0.95),
    4.5
)


# ============================================================
# PARABOLIC DISH
# ============================================================

def create_parabolic_dish(
    name,
    radius,
    depth,
    thickness,
    radial_segments=64,
    rings=14
):

    vertices = []
    faces = []

    # Concave/front surface.
    for ring in range(
        rings + 1
    ):

        r = (
            radius
            * ring
            / rings
        )

        y = (
            -depth
            + depth
            * (r / radius) ** 2
        )

        for seg in range(
            radial_segments
        ):

            theta = (
                2
                * math.pi
                * seg
                / radial_segments
            )

            vertices.append(
                (
                    r * math.cos(theta),
                    y,
                    r * math.sin(theta)
                )
            )


    front_count = len(vertices)


    # Rear shell.
    for ring in range(
        rings + 1
    ):

        r = (
            radius
            * ring
            / rings
        )

        y = (
            -depth
            + depth
            * (r / radius) ** 2
            - thickness
        )

        for seg in range(
            radial_segments
        ):

            theta = (
                2
                * math.pi
                * seg
                / radial_segments
            )

            vertices.append(
                (
                    r * math.cos(theta),
                    y,
                    r * math.sin(theta)
                )
            )


    for ring in range(rings):

        for seg in range(
            radial_segments
        ):

            nxt = (
                seg + 1
            ) % radial_segments

            a = (
                ring
                * radial_segments
                + seg
            )

            b = (
                ring
                * radial_segments
                + nxt
            )

            c = (
                (ring + 1)
                * radial_segments
                + nxt
            )

            d = (
                (ring + 1)
                * radial_segments
                + seg
            )

            faces.append(
                (a, b, c, d)
            )

            faces.append(
                (
                    front_count + d,
                    front_count + c,
                    front_count + b,
                    front_count + a
                )
            )


    outer = rings

    for seg in range(
        radial_segments
    ):

        nxt = (
            seg + 1
        ) % radial_segments

        fa = (
            outer
            * radial_segments
            + seg
        )

        fb = (
            outer
            * radial_segments
            + nxt
        )

        ba = front_count + fa
        bb = front_count + fb

        faces.append(
            (fa, ba, bb, fb)
        )


    mesh = bpy.data.meshes.new(
        name + "_mesh"
    )

    mesh.from_pydata(
        vertices,
        [],
        faces
    )

    mesh.update()


    obj = bpy.data.objects.new(
        name,
        mesh
    )

    bpy.context.collection.objects.link(
        obj
    )

    smooth(obj)

    return obj


# ============================================================
# ROOT HIERARCHY
# ============================================================

ROOT = add_empty(
    "RadarRoot"
)

STATIC_ROOT = add_empty(
    "StaticRoot"
)

STATIC_ROOT.parent = ROOT


ROT_ROOT = add_empty(
    "RotatingRoot",
    location=(
        0,
        0,
        HEAD_Z
    )
)

ROT_ROOT.parent = ROOT


DISH_PIVOT = add_empty(
    "DishPivot",
    location=(
        0,
        0,
        DISH_PIVOT_Z
    )
)

DISH_PIVOT.parent = ROT_ROOT

DISH_PIVOT.rotation_euler[
    0
] = math.radians(
    DISH_TILT_DEG
)


DISH_ASSEMBLY = add_empty(
    "DishAssembly",
    location=(
        0,
        DISH_FORWARD_OFFSET,
        0
    )
)

DISH_ASSEMBLY.parent = (
    DISH_PIVOT
)


# ============================================================
# BASE
# ============================================================

foundation = add_cube(
    "Foundation",
    location=(0, 0, 0.10),
    scale=(1.05, 1.05, 0.10)
)

assign_material(
    foundation,
    MAT_TRIM
)

bevel(
    foundation,
    0.03,
    3
)

foundation.parent = STATIC_ROOT


# Heavy four-corner feet.
for i, (x, y) in enumerate(
    [
        (-0.91, -0.91),
        ( 0.91, -0.91),
        (-0.91,  0.91),
        ( 0.91,  0.91),
    ]
):

    foot = add_cube(
        f"HeavyFoot_{i}",
        location=(
            x,
            y,
            0.18
        ),
        scale=(
            0.25,
            0.25,
            0.18
        )
    )

    assign_material(
        foot,
        MAT_TRIM
    )

    bevel(
        foot,
        0.035,
        3
    )

    foot.parent = STATIC_ROOT


lower_skirt = create_tapered_box(
    "LowerSkirt",
    bottom_x=0.91,
    bottom_y=0.91,
    top_x=0.83,
    top_y=0.83,
    height=0.20,
    z_bottom=0.22
)

assign_material(
    lower_skirt,
    MAT_TRIM
)

bevel(
    lower_skirt,
    0.025,
    3
)

lower_skirt.parent = (
    STATIC_ROOT
)


housing = create_tapered_box(
    "ArmoredHousing",
    bottom_x=0.78,
    bottom_y=0.78,
    top_x=0.66,
    top_y=0.66,
    height=0.48,
    z_bottom=0.40
)

assign_material(
    housing,
    MAT_BODY
)

bevel(
    housing,
    0.025,
    3
)

housing.parent = STATIC_ROOT


# Large armor panels.
panel_specs = [

    (
        "FrontArmorPanel",
        (0, -0.735, 0.62),
        (0.43, 0.025, 0.16)
    ),

    (
        "BackArmorPanel",
        (0, 0.735, 0.62),
        (0.43, 0.025, 0.16)
    ),

    (
        "LeftArmorPanel",
        (-0.735, 0, 0.62),
        (0.025, 0.43, 0.16)
    ),

    (
        "RightArmorPanel",
        (0.735, 0, 0.62),
        (0.025, 0.43, 0.16)
    ),
]


for name, location, scale in panel_specs:

    panel = add_cube(
        name,
        location=location,
        scale=scale
    )

    assign_material(
        panel,
        MAT_DARK
    )

    bevel(
        panel,
        0.012,
        2
    )

    panel.parent = STATIC_ROOT


# Four structural ribs.
for i, (x, y) in enumerate(
    [
        (-0.69, -0.69),
        ( 0.69, -0.69),
        (-0.69,  0.69),
        ( 0.69,  0.69),
    ]
):

    rib = add_cube(
        f"CornerRib_{i}",
        location=(
            x,
            y,
            0.64
        ),
        scale=(
            0.065,
            0.065,
            0.21
        )
    )

    assign_material(
        rib,
        MAT_TRIM
    )

    bevel(
        rib,
        0.012,
        2
    )

    rib.parent = STATIC_ROOT


# Dark top deck.
deck = add_cube(
    "TopDeck",
    location=(
        0,
        0,
        0.97
    ),
    scale=(
        0.78,
        0.78,
        0.07
    )
)

assign_material(
    deck,
    MAT_DECK
)

bevel(
    deck,
    0.022,
    3
)

deck.parent = STATIC_ROOT


deck_lip = add_cube(
    "DeckLip",
    location=(
        0,
        0,
        1.055
    ),
    scale=(
        0.72,
        0.72,
        0.018
    )
)

assign_material(
    deck_lip,
    MAT_TRIM
)

bevel(
    deck_lip,
    0.007,
    2
)

deck_lip.parent = STATIC_ROOT


# Control enclosure.
control = add_cube(
    "ControlBox",
    location=(
        0,
        -0.48,
        1.15
    ),
    scale=(
        0.18,
        0.11,
        0.13
    )
)

assign_material(
    control,
    MAT_DARK
)

bevel(
    control,
    0.015,
    2
)

control.parent = STATIC_ROOT


for i in range(2):

    indicator = add_cube(
        f"Indicator_{i}",
        location=(
            -0.055 + i * 0.11,
            -0.596,
            1.18
        ),
        scale=(
            0.025,
            0.008,
            0.022
        )
    )

    assign_material(
        indicator,
        MAT_BLUE
    )

    indicator.parent = STATIC_ROOT


# Bearing.
bearing_base = add_cylinder(
    "BearingBase",
    radius=0.46,
    depth=0.10,
    location=(
        0,
        0,
        1.12
    ),
    vertices=48
)

assign_material(
    bearing_base,
    MAT_TRIM
)

bearing_base.parent = (
    STATIC_ROOT
)


bearing_ring = add_cylinder(
    "BearingRing",
    radius=0.37,
    depth=0.075,
    location=(
        0,
        0,
        1.18
    ),
    vertices=48
)

assign_material(
    bearing_ring,
    MAT_DARK
)

bearing_ring.parent = (
    STATIC_ROOT
)


# ============================================================
# ROTATING LOWER ASSEMBLY
# ============================================================

rot_ring1 = add_cylinder(
    "RotRing1",
    radius=0.35,
    depth=0.12,
    location=(0, 0, 0.06),
    vertices=48
)

assign_material(
    rot_ring1,
    MAT_TRIM
)

rot_ring1.parent = ROT_ROOT


rot_ring2 = add_cylinder(
    "RotRing2",
    radius=0.29,
    depth=0.10,
    location=(0, 0, 0.15),
    vertices=48
)

assign_material(
    rot_ring2,
    MAT_DARK
)

rot_ring2.parent = ROT_ROOT


# ============================================================
# TRUNNION MOUNT
# ============================================================

rear_pedestal = add_cube(
    "RearPedestal",
    location=(
        0,
        TRUNNION_REAR_Y,
        REAR_PEDESTAL_TOP_Z * 0.60
    ),
    scale=(
        0.16,
        0.14,
        REAR_PEDESTAL_TOP_Z * 0.45
    )
)

assign_material(
    rear_pedestal,
    MAT_TRIM
)

bevel(
    rear_pedestal,
    0.025,
    3
)

rear_pedestal.parent = ROT_ROOT


add_arm(
    "RearCrossbar",
    (
        -TRUNNION_HALF_WIDTH,
        TRUNNION_REAR_Y,
        TRUNNION_Z
    ),
    (
        TRUNNION_HALF_WIDTH,
        TRUNNION_REAR_Y,
        TRUNNION_Z
    ),
    0.065,
    MAT_TRIM,
    ROT_ROOT,
    20
)


add_arm(
    "LeftTrunnionSupport",
    (
        -0.13,
        TRUNNION_REAR_Y,
        REAR_PEDESTAL_TOP_Z
    ),
    (
        -TRUNNION_HALF_WIDTH,
        TRUNNION_REAR_Y,
        TRUNNION_Z
    ),
    TRUNNION_ARM_RADIUS,
    MAT_TRIM,
    ROT_ROOT,
    20
)


add_arm(
    "RightTrunnionSupport",
    (
        0.13,
        TRUNNION_REAR_Y,
        REAR_PEDESTAL_TOP_Z
    ),
    (
        TRUNNION_HALF_WIDTH,
        TRUNNION_REAR_Y,
        TRUNNION_Z
    ),
    TRUNNION_ARM_RADIUS,
    MAT_TRIM,
    ROT_ROOT,
    20
)


# ============================================================
# DISH
# ============================================================

dish = create_parabolic_dish(
    "Dish",
    DISH_RADIUS,
    DISH_DEPTH,
    DISH_THICKNESS,
    64,
    14
)

assign_material(
    dish,
    MAT_DISH
)

dish.parent = DISH_ASSEMBLY


# Rim.
bpy.ops.mesh.primitive_torus_add(
    major_radius=DISH_RADIUS,
    minor_radius=0.025,
    major_segments=64,
    minor_segments=12,
    rotation=(
        math.radians(90),
        0,
        0
    )
)

rim = bpy.context.active_object
rim.name = "DishRim"

assign_material(
    rim,
    MAT_TRIM
)

rim.parent = DISH_ASSEMBLY


# Radial ribs.
for i in range(
    RIB_COUNT
):

    theta = (
        2
        * math.pi
        * i
        / RIB_COUNT
    )

    outer = Vector(
        (
            DISH_RADIUS
            * 0.92
            * math.cos(theta),

            -0.01,

            DISH_RADIUS
            * 0.92
            * math.sin(theta)
        )
    )

    inner = Vector(
        (
            0.16
            * math.cos(theta),

            -DISH_DEPTH
            * 0.82,

            0.16
            * math.sin(theta)
        )
    )

    add_arm(
        f"DishRib_{i}",
        inner,
        outer,
        0.009,
        MAT_TRIM,
        DISH_ASSEMBLY,
        10
    )


# Rim clamps.
for i in range(
    RIM_CLAMP_COUNT
):

    theta = (
        2
        * math.pi
        * i
        / RIM_CLAMP_COUNT
    )

    clamp = add_cube(
        f"RimClamp_{i}",
        location=(
            DISH_RADIUS
            * math.cos(theta),

            0.01,

            DISH_RADIUS
            * math.sin(theta)
        ),
        scale=(
            0.055,
            0.035,
            0.035
        )
    )

    assign_material(
        clamp,
        MAT_TRIM
    )

    bevel(
        clamp,
        0.008,
        2
    )

    clamp.parent = (
        DISH_ASSEMBLY
    )


# Receiver.
receiver = add_cylinder(
    "Receiver",
    radius=0.105,
    depth=0.34,
    location=(
        0,
        FEED_FORWARD,
        0
    ),
    vertices=24,
    rotation=(
        math.radians(90),
        0,
        0
    )
)

assign_material(
    receiver,
    MAT_TRIM
)

receiver.parent = (
    DISH_ASSEMBLY
)


receiver_cap = add_cylinder(
    "ReceiverCap",
    radius=0.082,
    depth=0.08,
    location=(
        0,
        FEED_FORWARD + 0.19,
        0
    ),
    vertices=24,
    rotation=(
        math.radians(90),
        0,
        0
    )
)

assign_material(
    receiver_cap,
    MAT_DARK
)

receiver_cap.parent = (
    DISH_ASSEMBLY
)


# Receiver indicator ring.
bpy.ops.mesh.primitive_torus_add(
    major_radius=0.106,
    minor_radius=0.012,
    major_segments=32,
    minor_segments=8,
    location=(
        0,
        FEED_FORWARD + 0.10,
        0
    ),
    rotation=(
        math.radians(90),
        0,
        0
    )
)

receiver_ring = (
    bpy.context.active_object
)

receiver_ring.name = (
    "ReceiverBlueRing"
)

assign_material(
    receiver_ring,
    MAT_BLUE
)

receiver_ring.parent = (
    DISH_ASSEMBLY
)


# Four supports.
rim_points = [

    (-0.64, 0.06,  0.02),
    ( 0.64, 0.06,  0.02),

    (-0.20, 0.06, -0.40),
    ( 0.20, 0.06, -0.40),
]


feed_points = [

    (
        -0.08,
        FEED_FORWARD - 0.08,
        0.03
    ),

    (
        0.08,
        FEED_FORWARD - 0.08,
        0.03
    ),

    (
        -0.035,
        FEED_FORWARD - 0.06,
        -0.005
    ),

    (
        0.035,
        FEED_FORWARD - 0.06,
        -0.005
    ),
]


for i in range(4):

    add_arm(
        f"FeedSupport_{i}",
        rim_points[i],
        feed_points[i],
        0.022,
        MAT_TRIM,
        DISH_ASSEMBLY,
        14
    )


# ============================================================
# FINAL MESH PASS
# ============================================================

for obj in bpy.data.objects:

    if obj.type != 'MESH':
        continue

    if (
        obj.name != "Dish"
        and not any(
            modifier.type == 'BEVEL'
            for modifier in obj.modifiers
        )
    ):

        bevel(
            obj,
            0.008,
            2
        )

    smooth(obj)


# ============================================================
# CAMERAS
# ============================================================

INVENTORY_CAMERA = create_ortho_camera(
    "InventoryCamera",
    INVENTORY_CAMERA_LOCATION,
    INVENTORY_TARGET,
    INVENTORY_ORTHO_SCALE
)


PLACED_CAMERA = create_ortho_camera(
    "PlacedCamera",
    PLACED_CAMERA_LOCATION,
    PLACED_TARGET,
    PLACED_ORTHO_SCALE
)


# ============================================================
# LIGHTS
# ============================================================

sun_data = bpy.data.lights.new(
    "Sun",
    type='SUN'
)

sun_data.energy = SUN_ENERGY

sun = bpy.data.objects.new(
    "Sun",
    sun_data
)

bpy.context.collection.objects.link(
    sun
)

sun.rotation_euler = (
    math.radians(42),
    0,
    math.radians(32)
)


area_data = bpy.data.lights.new(
    "AreaKey",
    type='AREA'
)

area_data.energy = AREA_ENERGY
area_data.shape = 'DISK'
area_data.size = 6.0

area = bpy.data.objects.new(
    "AreaKey",
    area_data
)

bpy.context.collection.objects.link(
    area
)

area.location = (
    -4.5,
    -3.0,
    7.0
)


point_camera_at(
    area,
    (0, 0, 0.8)
)


fill_data = bpy.data.lights.new(
    "Fill",
    type='AREA'
)

fill_data.energy = FILL_ENERGY
fill_data.size = 5.0

fill = bpy.data.objects.new(
    "Fill",
    fill_data
)

bpy.context.collection.objects.link(
    fill
)

fill.location = (
    4.0,
    2.0,
    4.0
)


point_camera_at(
    fill,
    (0, 0, 0.8)
)


# ============================================================
# WORLD
# ============================================================

world = scene.world

world.use_nodes = True

background = world.node_tree.nodes[
    "Background"
]

background.inputs[
    "Color"
].default_value = (
    0.006,
    0.008,
    0.010,
    1.0
)

background.inputs[
    "Strength"
].default_value = 0.12


# ============================================================
# INVENTORY RENDER
# ============================================================

def render_inventory():

    scene.camera = (
        INVENTORY_CAMERA
    )

    ROT_ROOT.rotation_euler[
        2
    ] = math.radians(
        INVENTORY_HEAD_ANGLE_DEG
    )

    scene.render.filepath = (
        INVENTORY_PATH
    )

    bpy.ops.render.render(
        write_still=True
    )

    print(
        f"Inventory image: "
        f"{INVENTORY_PATH}"
    )


# ============================================================
# PLACED FRAME RENDER
# ============================================================

def render_placed_frame(
    frame_index
):

    scene.camera = (
        PLACED_CAMERA
    )

    angle_deg = (
        frame_index
        * ANGLE_STEP_DEG
    )

    ROT_ROOT.rotation_euler[
        2
    ] = math.radians(
        angle_deg
    )

    filename = (
        f"radar_"
        f"{frame_index:02d}.png"
    )

    filepath = os.path.join(
        PLACED_FRAMES_DIR,
        filename
    )

    scene.render.filepath = (
        filepath
    )

    bpy.ops.render.render(
        write_still=True
    )

    print(
        f"Placed frame "
        f"{frame_index:02d} "
        f"({angle_deg:.1f} deg)"
    )

    return filepath


# ============================================================
# 4x4 ATLAS
# ============================================================

def build_4x4_atlas(
    frame_paths,
    atlas_path,
    frame_size,
    cols=4,
    rows=4
):

    atlas_width = (
        frame_size
        * cols
    )

    atlas_height = (
        frame_size
        * rows
    )

    atlas_pixels = (
        [0.0]
        * (
            atlas_width
            * atlas_height
            * 4
        )
    )

    loaded_images = []


    for index, path in enumerate(
        frame_paths
    ):

        image = bpy.data.images.load(
            path,
            check_existing=False
        )

        loaded_images.append(
            image
        )


        if (
            image.size[0]
            != frame_size
            or image.size[1]
            != frame_size
        ):

            raise ValueError(
                f"{path} is not "
                f"{frame_size}x"
                f"{frame_size}"
            )


        source_pixels = list(
            image.pixels[:]
        )


        # Desired visual sequence:
        #
        # 00 01 02 03
        # 04 05 06 07
        # 08 09 10 11
        # 12 13 14 15

        display_row = (
            index // cols
        )

        column = (
            index % cols
        )

        destination_x = (
            column
            * frame_size
        )

        # Blender image data is bottom-up.
        destination_y = (
            rows
            - 1
            - display_row
        ) * frame_size


        for y in range(
            frame_size
        ):

            source_start = (
                y
                * frame_size
                * 4
            )

            source_end = (
                source_start
                + frame_size
                * 4
            )

            destination_row = (
                destination_y
                + y
            )

            destination_start = (
                (
                    destination_row
                    * atlas_width
                    + destination_x
                )
                * 4
            )

            destination_end = (
                destination_start
                + frame_size
                * 4
            )

            atlas_pixels[
                destination_start:
                destination_end
            ] = source_pixels[
                source_start:
                source_end
            ]


    atlas = bpy.data.images.new(
        "PlacedRadarAtlas",
        width=atlas_width,
        height=atlas_height,
        alpha=True,
        float_buffer=False
    )

    atlas.pixels.foreach_set(
        atlas_pixels
    )

    atlas.filepath_raw = (
        atlas_path
    )

    atlas.file_format = 'PNG'

    atlas.save()


    for image in loaded_images:

        bpy.data.images.remove(
            image
        )


    print(
        f"Placed atlas: "
        f"{atlas_path}"
    )


# ============================================================
# EXECUTE
# ============================================================

if RENDER_INVENTORY:

    render_inventory()


placed_paths = []

if RENDER_PLACED_ANIMATION:

    for frame_index in range(
        TOTAL_FRAMES
    ):

        placed_paths.append(
            render_placed_frame(
                frame_index
            )
        )


if (
    BUILD_PLACED_ATLAS
    and len(placed_paths)
    == TOTAL_FRAMES
):

    build_4x4_atlas(
        placed_paths,
        PLACED_ATLAS_PATH,
        FRAME_SIZE,
        ATLAS_COLS,
        ATLAS_ROWS
    )


print("")
print("======================================")
print("RADAR ASSET PIPELINE COMPLETE")
print("======================================")
print("")
print("Inventory:")
print(INVENTORY_PATH)
print("")
print("Placed frames:")
print(PLACED_FRAMES_DIR)
print("")
print("Placed atlas:")
print(PLACED_ATLAS_PATH)
print("")
