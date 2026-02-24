#pragma once
#include <string>
#include <vector>
#include "taichi/ui/utils/utils.h"

namespace taichi::ui {

class GuiBase {
 public:
  virtual void begin(const std::string &name,
                     float x,
                     float y,
                     float width,
                     float height) = 0;
  virtual void end() = 0;
  virtual void text(const std::string &text) = 0;
  virtual void text(const std::string &text, glm::vec3 color) = 0;
  virtual bool checkbox(const std::string &name, bool old_value) = 0;
  virtual int slider_int(const std::string &name,
                         int old_value,
                         int minimum,
                         int maximum) = 0;
  virtual float slider_float(const std::string &name,
                             float old_value,
                             float minimum,
                             float maximum) = 0;
  virtual glm::vec3 color_edit_3(const std::string &name,
                                 glm::vec3 old_value) = 0;
  virtual bool button(const std::string &text) = 0;
  virtual std::string input_text(const std::string &name,
                                 const std::string &old_value) = 0;
  virtual void graph(const std::string &title,
                     const std::vector<float> &values,
                     float scale_min,
                     float scale_max,
                     float graph_size_x,
                     float graph_size_y,
                     const std::string &overlay_text) = 0;
  virtual void graph_histogram(const std::string &title,
                               const std::vector<float> &values,
                               float scale_min,
                               float scale_max,
                               float graph_size_x,
                               float graph_size_y,
                               const std::string &overlay_text) = 0;

  // Selection widgets
  virtual int combo(const std::string &name,
                    int old_value,
                    const std::vector<std::string> &items) = 0;
  virtual bool radio_button(const std::string &name, bool active) = 0;
  virtual int listbox(const std::string &name,
                      int old_value,
                      const std::vector<std::string> &items,
                      int height_in_items) = 0;

  // Input widgets
  virtual int input_int(const std::string &name,
                        int old_value,
                        int step,
                        int step_fast) = 0;
  virtual float input_float(const std::string &name,
                            float old_value,
                            float step,
                            float step_fast) = 0;
  virtual float drag_float(const std::string &name,
                           float old_value,
                           float speed,
                           float v_min,
                           float v_max) = 0;
  virtual int drag_int(const std::string &name,
                       int old_value,
                       float speed,
                       int v_min,
                       int v_max) = 0;

  // Display/Layout widgets
  virtual void progress_bar(float fraction,
                            float size_x,
                            float size_y,
                            const std::string &overlay) = 0;
  virtual void separator() = 0;
  virtual void same_line(float offset, float spacing) = 0;
  virtual void text_wrapped(const std::string &text) = 0;

  // Structural/Advanced widgets
  virtual bool collapsing_header(const std::string &name) = 0;
  virtual bool tree_node(const std::string &name) = 0;
  virtual void tree_pop() = 0;
  virtual void tooltip(const std::string &text) = 0;
  virtual glm::vec4 color_edit_4(const std::string &name,
                                 glm::vec4 old_value) = 0;
  virtual std::string input_text_multiline(const std::string &name,
                                           const std::string &old_value,
                                           float width,
                                           float height) = 0;

  // Tabs
  virtual bool begin_tab_bar(const std::string &name) = 0;
  virtual void end_tab_bar() = 0;
  virtual bool begin_tab_item(const std::string &name) = 0;
  virtual void end_tab_item() = 0;

  // Tables
  virtual bool begin_table(const std::string &name,
                           int column,
                           float outer_size_x,
                           float outer_size_y) = 0;
  virtual void end_table() = 0;
  virtual void table_next_row() = 0;
  virtual bool table_next_column() = 0;
  virtual void table_setup_column(const std::string &label) = 0;
  virtual void table_headers_row() = 0;

  virtual void prepare_for_next_frame() = 0;
  virtual ~GuiBase() = default;
};

}  // namespace taichi::ui
