"""
Per-feature screenshot test for all GGUI features.

Each phase renders **only one feature category** in a clean window,
takes a screenshot, then advances to the next phase.  After all
12 phases complete the script exits.

Run:
    python tests/test_ggui_features.py

Screenshots are saved to tests/screenshots/.
"""

import os
import math
import taichi as ti

ti.init(arch=ti.vulkan)

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

RES = (1024, 720)

window = ti.ui.Window("GGUI Feature Demo", RES, vsync=True)

# ---------------------------------------------------------------------------
# Phase configuration
# ---------------------------------------------------------------------------
FRAMES_PER_PHASE = 6        # frames to render per phase
SCREENSHOT_FRAME = 3         # take screenshot on this frame within each phase

PHASES = [
    ("01_basic_widgets",       "Basic Widgets"),
    ("02_selection_widgets",   "Selection Widgets"),
    ("03_input_widgets",       "Input Widgets"),
    ("04_display_layout",      "Display & Layout"),
    ("05_structural_widgets",  "Structural Widgets"),
    ("06_color_pickers",       "Color Pickers"),
    ("07_tabs",                "Tabs"),
    ("08_tables",              "Tables"),
    ("09_graph_histogram",     "Graph & Histogram"),
    ("10_rgba_canvas",         "RGBA 2D Canvas"),
    ("11_directional_light",   "Directional Light"),
    ("12_window_title_scroll", "Window Title & Scroll"),
]

# ---------------------------------------------------------------------------
# Widget state (persistent across phases so values look natural)
# ---------------------------------------------------------------------------
combo_idx = 1
radio_sel = 0
listbox_idx = 0
input_int_val = 42
input_float_val = 3.14
drag_float_val = 0.5
drag_int_val = 10
check_val = True
slider_f = 0.5
slider_i = 50
color3 = (0.2, 0.6, 1.0)
color4 = (1.0, 0.3, 0.1, 0.8)
text_val = "Hello GGUI"
multiline_val = "Line 1\nLine 2\nLine 3"

# ---------------------------------------------------------------------------
# Phase 10 — RGBA triangles / circles / lines
# ---------------------------------------------------------------------------
tri_verts = ti.Vector.field(3, ti.f32, shape=6)
tri_colors = ti.Vector.field(4, ti.f32, shape=6)

tri_verts[0] = [0.15, 0.25, 0]; tri_verts[1] = [0.45, 0.25, 0]; tri_verts[2] = [0.30, 0.60, 0]
tri_colors[0] = [1, 0, 0, 0.5]; tri_colors[1] = [1, 0, 0, 0.5]; tri_colors[2] = [1, 0, 0, 0.5]

tri_verts[3] = [0.25, 0.20, 0]; tri_verts[4] = [0.55, 0.20, 0]; tri_verts[5] = [0.40, 0.55, 0]
tri_colors[3] = [0, 1, 0, 0.5]; tri_colors[4] = [0, 1, 0, 0.5]; tri_colors[5] = [0, 1, 0, 0.5]

num_circles = 20
circle_centers = ti.Vector.field(3, ti.f32, shape=num_circles)
circle_colors = ti.Vector.field(4, ti.f32, shape=num_circles)

@ti.kernel
def init_circles():
    for i in range(num_circles):
        t = i / num_circles
        circle_centers[i] = [0.10 + t * 0.80, 0.75 + 0.05 * ti.sin(t * 6.28), 0]
        circle_colors[i] = [t, 0.5, 1.0 - t, 0.3 + 0.7 * t]

init_circles()

num_line_pts = 20
line_verts = ti.Vector.field(3, ti.f32, shape=num_line_pts)
line_colors = ti.Vector.field(4, ti.f32, shape=num_line_pts)

@ti.kernel
def init_lines():
    for i in range(num_line_pts):
        t = i / (num_line_pts - 1)
        line_verts[i] = [0.10 + t * 0.80, 0.88 + 0.05 * ti.sin(t * 12.56), 0]
        line_colors[i] = [1.0, 1.0 - t, t, 0.2 + 0.8 * t]

init_lines()

# ---------------------------------------------------------------------------
# Phase 11 — Directional light: mesh + particles
# ---------------------------------------------------------------------------
mesh_verts = ti.Vector.field(3, ti.f32, shape=4)
mesh_indices = ti.field(ti.i32, shape=6)
mesh_verts[0] = [-0.5, 0, -0.5]
mesh_verts[1] = [ 0.5, 0, -0.5]
mesh_verts[2] = [ 0.5, 0,  0.5]
mesh_verts[3] = [-0.5, 0,  0.5]
mesh_indices[0] = 0; mesh_indices[1] = 1; mesh_indices[2] = 2
mesh_indices[3] = 0; mesh_indices[4] = 2; mesh_indices[5] = 3

num_particles = 200
particle_pos = ti.Vector.field(3, ti.f32, shape=num_particles)

@ti.kernel
def init_particles():
    for i in range(num_particles):
        t = i / num_particles
        particle_pos[i] = [
            ti.sin(t * 6.28 * 3) * 0.3,
            t * 1.5 - 0.3,
            ti.cos(t * 6.28 * 3) * 0.3,
        ]

init_particles()

# ---------------------------------------------------------------------------
# Phase renderers — each draws exactly one feature category
# ---------------------------------------------------------------------------

def render_basic_widgets(g, frame):
    global check_val, slider_f, slider_i
    g.text("Basic Widgets Demo")
    g.separator()
    g.text("Static text label")
    g.button("Click Me")
    slider_i = g.slider_int("SliderInt", slider_i, 0, 100)
    slider_f = g.slider_float("SliderFloat", slider_f, 0.0, 1.0)
    check_val = g.checkbox("Checkbox", check_val)


def render_selection_widgets(g, frame):
    global combo_idx, radio_sel, listbox_idx
    g.text("Selection Widgets Demo")
    g.separator()
    combo_idx = g.combo("Combo", combo_idx, ["Apple", "Banana", "Cherry", "Date"])

    for i, label in enumerate(["Radio A", "Radio B", "Radio C"]):
        if g.radio_button(label, radio_sel == i):
            radio_sel = i
        if i < 2:
            g.same_line()

    listbox_idx = g.listbox("Listbox", listbox_idx, ["Item 0", "Item 1", "Item 2", "Item 3"], 3)


def render_input_widgets(g, frame):
    global input_int_val, input_float_val, drag_float_val, drag_int_val
    global text_val, multiline_val
    g.text("Input Widgets Demo")
    g.separator()
    input_int_val = g.input_int("InputInt", input_int_val, step=1, step_fast=10)
    input_float_val = g.input_float("InputFloat", input_float_val, step=0.1, step_fast=1.0)
    drag_float_val = g.drag_float("DragFloat", drag_float_val, speed=0.005, v_min=0.0, v_max=1.0)
    drag_int_val = g.drag_int("DragInt", drag_int_val, speed=0.5, v_min=0, v_max=100)
    text_val = g.input_text("InputText", text_val)
    multiline_val = g.input_text_multiline("Multiline", multiline_val, width=0, height=60)


def render_display_layout(g, frame):
    progress = (math.sin(frame * 0.1) + 1.0) / 2.0
    g.text("Display & Layout Demo")
    g.separator()
    g.progress_bar(progress, overlay=f"{progress * 100:.0f}%")
    g.separator()
    g.text("Label A")
    g.same_line()
    g.text("Label B (same line)")
    g.text_wrapped(
        "This text is word-wrapped. It demonstrates the text_wrapped() "
        "widget which automatically breaks long lines to fit the window width. "
        "Resize the window to see how it reflows."
    )


def render_structural_widgets(g, frame):
    global check_val, slider_f, slider_i
    g.text("Structural Widgets Demo")
    g.separator()
    if g.collapsing_header("Collapsing Header"):
        g.text("Content inside collapsing header")
        check_val = g.checkbox("Checkbox", check_val)
        slider_f = g.slider_float("SliderF", slider_f, 0.0, 1.0)
        slider_i = g.slider_int("SliderI", slider_i, 0, 100)

    with g.tree("Tree Node A") as opened:
        if opened:
            g.text("Leaf content A")
            with g.tree("Nested Node") as nested:
                if nested:
                    g.text("Deep leaf content")

    g.button("Hover me for tooltip")
    g.tooltip("This tooltip appears on hover!")


def render_color_pickers(g, frame):
    global color3, color4
    g.text("Color Pickers Demo")
    g.separator()
    color3 = g.color_edit_3("RGB Color", color3)
    color4 = g.color_edit_4("RGBA Color", color4)


def render_tabs(g, frame):
    g.text("Tabs Demo")
    g.separator()
    with g.tab_bar("DemoTabs") as visible:
        if visible:
            with g.tab("Info") as sel:
                if sel:
                    g.text(f"Combo selection: {combo_idx}")
                    g.text(f"Radio: {radio_sel}  Listbox: {listbox_idx}")
            with g.tab("Values") as sel:
                if sel:
                    g.text(f"int={input_int_val}  float={input_float_val:.2f}")
                    g.text(f"dragF={drag_float_val:.3f}  dragI={drag_int_val}")
            with g.tab("Extra") as sel:
                if sel:
                    g.text("Additional tab content")


def render_tables(g, frame):
    g.text("Tables Demo")
    g.separator()
    with g.table("DemoTable", 3) as tbl:
        if tbl:
            g.table_setup_column("Name")
            g.table_setup_column("Type")
            g.table_setup_column("Value")
            g.table_headers_row()

            for name, typ, val in [
                ("combo_idx", "int", str(combo_idx)),
                ("drag_float", "float", f"{drag_float_val:.3f}"),
                ("color4.a", "float", f"{color4[3]:.2f}"),
                ("slider_i", "int", str(slider_i)),
            ]:
                g.table_next_row()
                g.table_next_column(); g.text(name)
                g.table_next_column(); g.text(typ)
                g.table_next_column(); g.text(val)


def render_graph_histogram(g, frame):
    g.text("Graph & Histogram Demo")
    g.separator()
    # Line graph — sine wave
    sin_values = [math.sin(i * 0.3) for i in range(40)]
    g.graph("Sine Wave", sin_values, scale_min=-1.0, scale_max=1.0,
            graph_size_x=0, graph_size_y=80)

    # Histogram — sample distribution
    hist_values = [abs(math.sin(i * 0.5)) * 10 for i in range(20)]
    g.graph_histogram("Distribution", hist_values, scale_min=0.0, scale_max=10.0,
                      graph_size_x=0, graph_size_y=80)


# Map phase index → render function (for GUI-only phases)
GUI_RENDERERS = {
    0:  render_basic_widgets,
    1:  render_selection_widgets,
    2:  render_input_widgets,
    3:  render_display_layout,
    4:  render_structural_widgets,
    5:  render_color_pickers,
    6:  render_tabs,
    7:  render_tables,
    8:  render_graph_histogram,
}

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
frame = 0
phase = 0
phase_frame = 0
screenshots_taken = 0

while window.running and phase < len(PHASES):
    frame += 1
    phase_frame += 1

    filename, title = PHASES[phase]

    # --- Phase 12: Window title & scroll (special: uses set_title + scroll) ---
    if phase == 11:
        window.set_title(f"GGUI Feature Demo — Frame {frame}")
        scroll_x, scroll_y = window.get_scroll_delta()
        gui = window.get_gui()
        with gui.sub_window(title, 0.1, 0.1, 0.8, 0.8) as g:
            g.text("Window Title & Scroll Demo")
            g.separator()
            g.text(f"Window title updated to: 'GGUI Feature Demo — Frame {frame}'")
            g.text(f"Scroll delta: ({scroll_x:.1f}, {scroll_y:.1f})")
            g.text("Use set_title() to update the window title at runtime.")
            g.text("Use get_scroll_delta() to read mouse wheel events.")
        canvas = window.get_canvas()
        canvas.set_background_color((0.12, 0.12, 0.18))

    # --- Phase 10: RGBA 2D canvas ---
    elif phase == 9:
        canvas = window.get_canvas()
        canvas.set_background_color((0.15, 0.15, 0.2))
        canvas.triangles(tri_verts, per_vertex_color=tri_colors)
        canvas.circles(circle_centers, radius=0.015, per_vertex_color=circle_colors)
        canvas.lines(line_verts, width=0.005, per_vertex_color=line_colors)

    # --- Phase 11: Directional light 3D scene ---
    elif phase == 10:
        canvas = window.get_canvas()
        canvas.set_background_color((0.1, 0.1, 0.15))
        scene = window.get_scene()
        camera = ti.ui.Camera()
        camera.position(0, 1.5, 3)
        camera.lookat(0, 0.3, 0)
        camera.up(0, 1, 0)
        scene.set_camera(camera)

        scene.ambient_light((0.15, 0.15, 0.15))
        scene.point_light(pos=(2, 2, 1), color=(0.8, 0.6, 0.3))
        scene.directional_light(direction=(-1, -1, -0.5), color=(0.3, 0.5, 0.9))
        scene.directional_light(direction=(0, -0.5, 1), color=(0.4, 0.4, 0.4))

        scene.mesh(mesh_verts, indices=mesh_indices, color=(0.6, 0.6, 0.6), two_sided=True)
        scene.particles(particle_pos, radius=0.03, color=(0.9, 0.4, 0.2))

        canvas.scene(scene)

    # --- GUI-only phases (0-8) ---
    elif phase in GUI_RENDERERS:
        canvas = window.get_canvas()
        canvas.set_background_color((0.12, 0.12, 0.18))
        gui = window.get_gui()
        with gui.sub_window(title, 0.05, 0.05, 0.9, 0.9) as g:
            GUI_RENDERERS[phase](g, frame)

    # -----------------------------------------------------------------------
    # Screenshot
    # -----------------------------------------------------------------------
    if phase_frame == SCREENSHOT_FRAME:
        path = os.path.join(SCREENSHOT_DIR, filename + ".png")
        window.save_image(path)
        print(f"[phase {phase + 1}/{len(PHASES)}] Saved: {path}")
        screenshots_taken += 1

    window.show()

    # Advance phase
    if phase_frame >= FRAMES_PER_PHASE:
        phase += 1
        phase_frame = 0

print(f"\nDone. {frame} frames rendered, {screenshots_taken} screenshots saved.")
print(f"Screenshots saved to: {SCREENSHOT_DIR}/")
