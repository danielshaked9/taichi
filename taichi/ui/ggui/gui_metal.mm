#include "gui_metal.h"
#include "taichi/ui/ggui/app_context.h"
#include "taichi/ui/ggui/swap_chain.h"
#include <imgui_impl_metal.h>

using namespace taichi::lang::metal;
using namespace taichi::lang;

namespace taichi::ui {

namespace vulkan {

GuiMetal::GuiMetal(AppContext *app_context, TaichiWindow *window) {
  app_context_ = app_context;

  IMGUI_CHECKVERSION();
  imgui_context_ = ImGui::CreateContext();
  [[maybe_unused]] ImGuiIO &io = ImGui::GetIO();

  ImGui::StyleColorsDark();

  if (app_context->config.show_window) {
    ImGui_ImplGlfw_InitForOpenGL(window, true);
    glfwGetWindowSize(window, &widthBeforeDPIScale, &heightBeforeDPIScale);
  } else {
    widthBeforeDPIScale = app_context->config.width;
    heightBeforeDPIScale = app_context->config.height;
  }
  auto &device =
      static_cast<taichi::lang::metal::MetalDevice &>(app_context_->device());

  ImGui_ImplMetal_Init(device.mtl_device());
}

void GuiMetal::init_render_resources(void *rpd) {
  current_rpd_ = (__bridge MTLRenderPassDescriptor *)rpd;
}

void GuiMetal::prepare_for_next_frame() {
  if (app_context_->config.show_window) {
    ImGui_ImplGlfw_NewFrame();
  } else {
    // io.DisplaySize is set during ImGui_ImplGlfw_NewFrame()
    // but since we're headless, we do it explicitly here
    auto w = app_context_->config.width;
    auto h = app_context_->config.height;
    ImGuiIO &io = ImGui::GetIO();
    io.DisplaySize = ImVec2((float)w, (float)h);
  }
  ImGui::NewFrame();
  is_empty_ = true;
}

float GuiMetal::abs_x(float x) { return x * widthBeforeDPIScale; }
float GuiMetal::abs_y(float y) { return y * heightBeforeDPIScale; }

void GuiMetal::begin(const std::string &name, float x, float y, float width,
                     float height) {
  ImGui::SetNextWindowPos(ImVec2(abs_x(x), abs_y(y)), ImGuiCond_Once);
  ImGui::SetNextWindowSize(ImVec2(abs_x(width), abs_y(height)), ImGuiCond_Once);
  ImGui::Begin(name.c_str());
  is_empty_ = false;
}
void GuiMetal::end() { ImGui::End(); }
void GuiMetal::text(const std::string &text) {
  ImGui::Text("%s", text.c_str());
}
void GuiMetal::text(const std::string &text, glm::vec3 color) {
  ImGui::TextColored(ImVec4(color[0], color[1], color[2], 1.0f), "%s",
                     text.c_str());
}
bool GuiMetal::checkbox(const std::string &name, bool old_value) {
  ImGui::Checkbox(name.c_str(), &old_value);
  return old_value;
}
int GuiMetal::slider_int(const std::string &name, int old_value, int minimum,
                         int maximum) {
  ImGui::SliderInt(name.c_str(), &old_value, minimum, maximum);
  return old_value;
}
float GuiMetal::slider_float(const std::string &name, float old_value,
                             float minimum, float maximum) {
  ImGui::SliderFloat(name.c_str(), &old_value, minimum, maximum, "%.7g");
  return old_value;
}
glm::vec3 GuiMetal::color_edit_3(const std::string &name, glm::vec3 old_value) {
  ImGui::ColorEdit3(name.c_str(), (float *)&old_value);
  return old_value;
}
bool GuiMetal::button(const std::string &text) {
  return ImGui::Button(text.c_str());
}
std::string GuiMetal::input_text(const std::string &name,
                                 const std::string &old_value) {
  char buf[256];
  strncpy(buf, old_value.c_str(), sizeof(buf) - 1);
  buf[sizeof(buf) - 1] = '\0';
  ImGui::InputText(name.c_str(), buf, sizeof(buf));
  return std::string(buf);
}
void GuiMetal::graph(const std::string &title,
                     const std::vector<float> &values,
                     float scale_min,
                     float scale_max,
                     float graph_size_x,
                     float graph_size_y,
                     const std::string &overlay_text) {
  const char *overlay = overlay_text.empty() ? nullptr : overlay_text.c_str();
  ImGui::PlotLines(title.c_str(), values.data(), (int)values.size(), 0, overlay,
                   scale_min, scale_max, ImVec2(graph_size_x, graph_size_y));
}
void GuiMetal::graph_histogram(const std::string &title,
                               const std::vector<float> &values,
                               float scale_min,
                               float scale_max,
                               float graph_size_x,
                               float graph_size_y,
                               const std::string &overlay_text) {
  const char *overlay = overlay_text.empty() ? nullptr : overlay_text.c_str();
  ImGui::PlotHistogram(title.c_str(), values.data(), (int)values.size(), 0,
                       overlay, scale_min, scale_max,
                       ImVec2(graph_size_x, graph_size_y));
}

int GuiMetal::combo(const std::string &name,
                    int old_value,
                    const std::vector<std::string> &items) {
  std::vector<const char *> c_items;
  c_items.reserve(items.size());
  for (const auto &s : items) {
    c_items.push_back(s.c_str());
  }
  ImGui::Combo(name.c_str(), &old_value, c_items.data(), (int)c_items.size());
  return old_value;
}
bool GuiMetal::radio_button(const std::string &name, bool active) {
  return ImGui::RadioButton(name.c_str(), active);
}
int GuiMetal::listbox(const std::string &name,
                      int old_value,
                      const std::vector<std::string> &items,
                      int height_in_items) {
  std::vector<const char *> c_items;
  c_items.reserve(items.size());
  for (const auto &s : items) {
    c_items.push_back(s.c_str());
  }
  ImGui::ListBox(name.c_str(), &old_value, c_items.data(), (int)c_items.size(),
                 height_in_items);
  return old_value;
}
int GuiMetal::input_int(const std::string &name,
                        int old_value,
                        int step,
                        int step_fast) {
  ImGui::InputInt(name.c_str(), &old_value, step, step_fast);
  return old_value;
}
float GuiMetal::input_float(const std::string &name,
                            float old_value,
                            float step,
                            float step_fast) {
  ImGui::InputFloat(name.c_str(), &old_value, step, step_fast);
  return old_value;
}
float GuiMetal::drag_float(const std::string &name,
                           float old_value,
                           float speed,
                           float v_min,
                           float v_max) {
  ImGui::DragFloat(name.c_str(), &old_value, speed, v_min, v_max);
  return old_value;
}
int GuiMetal::drag_int(const std::string &name,
                       int old_value,
                       float speed,
                       int v_min,
                       int v_max) {
  ImGui::DragInt(name.c_str(), &old_value, speed, v_min, v_max);
  return old_value;
}
void GuiMetal::progress_bar(float fraction,
                            float size_x,
                            float size_y,
                            const std::string &overlay) {
  const char *ovl = overlay.empty() ? nullptr : overlay.c_str();
  ImGui::ProgressBar(fraction, ImVec2(size_x, size_y), ovl);
}
void GuiMetal::separator() {
  ImGui::Separator();
}
void GuiMetal::same_line(float offset, float spacing) {
  ImGui::SameLine(offset, spacing);
}
void GuiMetal::text_wrapped(const std::string &text) {
  ImGui::TextWrapped("%s", text.c_str());
}
bool GuiMetal::collapsing_header(const std::string &name) {
  return ImGui::CollapsingHeader(name.c_str());
}
bool GuiMetal::tree_node(const std::string &name) {
  return ImGui::TreeNode(name.c_str());
}
void GuiMetal::tree_pop() {
  ImGui::TreePop();
}
void GuiMetal::tooltip(const std::string &text) {
  if (ImGui::IsItemHovered()) {
    ImGui::SetTooltip("%s", text.c_str());
  }
}
glm::vec4 GuiMetal::color_edit_4(const std::string &name,
                                 glm::vec4 old_value) {
  ImGui::ColorEdit4(name.c_str(), (float *)&old_value);
  return old_value;
}
std::string GuiMetal::input_text_multiline(const std::string &name,
                                           const std::string &old_value,
                                           float width,
                                           float height) {
  char buf[4096];
  strncpy(buf, old_value.c_str(), sizeof(buf) - 1);
  buf[sizeof(buf) - 1] = '\0';
  ImGui::InputTextMultiline(name.c_str(), buf, sizeof(buf),
                            ImVec2(width, height));
  return std::string(buf);
}
bool GuiMetal::begin_tab_bar(const std::string &name) {
  return ImGui::BeginTabBar(name.c_str());
}
void GuiMetal::end_tab_bar() {
  ImGui::EndTabBar();
}
bool GuiMetal::begin_tab_item(const std::string &name) {
  return ImGui::BeginTabItem(name.c_str());
}
void GuiMetal::end_tab_item() {
  ImGui::EndTabItem();
}
bool GuiMetal::begin_table(const std::string &name,
                           int column,
                           float outer_size_x,
                           float outer_size_y) {
  return ImGui::BeginTable(name.c_str(), column, 0,
                           ImVec2(outer_size_x, outer_size_y));
}
void GuiMetal::end_table() {
  ImGui::EndTable();
}
void GuiMetal::table_next_row() {
  ImGui::TableNextRow();
}
bool GuiMetal::table_next_column() {
  return ImGui::TableNextColumn();
}
void GuiMetal::table_setup_column(const std::string &label) {
  ImGui::TableSetupColumn(label.c_str());
}
void GuiMetal::table_headers_row() {
  ImGui::TableHeadersRow();
}

void GuiMetal::draw(taichi::lang::CommandList *cmd_list) {
  ImGui_ImplMetal_NewFrame(current_rpd_);

  // Rendering
  ImGui::Render();

  @autoreleasepool {
    MTLCommandBuffer_id buffer =
        static_cast<MetalCommandList *>(cmd_list)->finalize();

    MTLRenderCommandEncoder_id rce =
        [buffer renderCommandEncoderWithDescriptor:current_rpd_];
    ImGui_ImplMetal_RenderDrawData(ImGui::GetDrawData(), buffer, rce);
    [rce endEncoding];
  }
}
void GuiMetal::cleanup_render_resources() {
  ImGui_ImplMetal_Shutdown();
  current_rpd_ = nullptr;
}

GuiMetal::~GuiMetal() {
  if (app_context_->config.show_window) {
    ImGui_ImplGlfw_Shutdown();
  }
  cleanup_render_resources();
  ImGui::DestroyContext(imgui_context_);
}

bool GuiMetal::is_empty() { return is_empty_; }

} // namespace vulkan

} // namespace taichi::ui
