#pragma once

#include "taichi/ui/utils/utils.h"

#include "taichi/ui/common/gui_base.h"
#include "taichi/ui/ggui/app_context.h"

#ifdef TI_WITH_METAL

#include <imgui.h>
#include <imgui_impl_glfw.h>
#include "taichi/rhi/metal/metal_device.h"

namespace taichi::ui {

namespace vulkan {

class TI_DLL_EXPORT GuiMetal final : public GuiBase {
 public:
  GuiMetal(AppContext *app_context, TaichiWindow *window);
  ~GuiMetal() override;

  void init_render_resources(void *rpd);
  void cleanup_render_resources();

  void begin(const std::string &name,
             float x,
             float y,
             float width,
             float height) override;
  void end() override;
  void text(const std::string &text) override;
  void text(const std::string &text, glm::vec3 color) override;
  bool checkbox(const std::string &name, bool old_value) override;
  int slider_int(const std::string &name,
                 int old_value,
                 int minimum,
                 int maximum) override;
  float slider_float(const std::string &name,
                     float old_value,
                     float minimum,
                     float maximum) override;
  // TODO: consider renaming this?
  glm::vec3 color_edit_3(const std::string &name, glm::vec3 old_value) override;
  bool button(const std::string &text) override;
  std::string input_text(const std::string &name,
                         const std::string &old_value) override;
  void graph(const std::string &title,
             const std::vector<float> &values,
             float scale_min,
             float scale_max,
             float graph_size_x,
             float graph_size_y,
             const std::string &overlay_text) override;
  void graph_histogram(const std::string &title,
                       const std::vector<float> &values,
                       float scale_min,
                       float scale_max,
                       float graph_size_x,
                       float graph_size_y,
                       const std::string &overlay_text) override;

  int combo(const std::string &name,
            int old_value,
            const std::vector<std::string> &items) override;
  bool radio_button(const std::string &name, bool active) override;
  int listbox(const std::string &name,
              int old_value,
              const std::vector<std::string> &items,
              int height_in_items) override;
  int input_int(const std::string &name,
                int old_value,
                int step,
                int step_fast) override;
  float input_float(const std::string &name,
                    float old_value,
                    float step,
                    float step_fast) override;
  float drag_float(const std::string &name,
                   float old_value,
                   float speed,
                   float v_min,
                   float v_max) override;
  int drag_int(const std::string &name,
               int old_value,
               float speed,
               int v_min,
               int v_max) override;
  void progress_bar(float fraction,
                    float size_x,
                    float size_y,
                    const std::string &overlay) override;
  void separator() override;
  void same_line(float offset, float spacing) override;
  void text_wrapped(const std::string &text) override;
  bool collapsing_header(const std::string &name) override;
  bool tree_node(const std::string &name) override;
  void tree_pop() override;
  void tooltip(const std::string &text) override;
  glm::vec4 color_edit_4(const std::string &name,
                         glm::vec4 old_value) override;
  std::string input_text_multiline(const std::string &name,
                                   const std::string &old_value,
                                   float width,
                                   float height) override;
  bool begin_tab_bar(const std::string &name) override;
  void end_tab_bar() override;
  bool begin_tab_item(const std::string &name) override;
  void end_tab_item() override;
  bool begin_table(const std::string &name,
                   int column,
                   float outer_size_x,
                   float outer_size_y) override;
  void end_table() override;
  void table_next_row() override;
  bool table_next_column() override;
  void table_setup_column(const std::string &label) override;
  void table_headers_row() override;

  void prepare_for_next_frame() override;

  void draw(taichi::lang::CommandList *cmd_list);

  bool is_empty();

 private:
  bool is_empty_;
  AppContext *app_context_{nullptr};
  ImGuiContext *imgui_context_{nullptr};
  int widthBeforeDPIScale{0};
  int heightBeforeDPIScale{0};

  MTLRenderPassDescriptor *current_rpd_{nullptr};

  float abs_x(float x);

  float abs_y(float y);
};

}  // namespace vulkan

}  // namespace taichi::ui

#endif
