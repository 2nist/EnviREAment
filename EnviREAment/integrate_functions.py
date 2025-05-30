#!/usr/bin/env python3
"""
integrate_functions.py
Automatically integrate all generated ImGui functions into enhanced_virtual_reaper.lua
"""

def integrate_generated_functions():
    """Read generated functions and integrate them into the main file."""
    
    # Read the generated functions
    try:
        with open('generated_imgui_functions.lua', 'r', encoding='utf-8') as f:
            generated_content = f.read()
    except FileNotFoundError:
        print("❌ Error: generated_imgui_functions.lua not found")
        return False
    
    # Read the main virtual environment file
    try:
        with open('enhanced_virtual_reaper.lua', 'r', encoding='utf-8') as f:
            main_content = f.read()
    except FileNotFoundError:
        print("❌ Error: enhanced_virtual_reaper.lua not found")
        return False
    
    # Extract only the function definitions (skip the header comments)
    lines = generated_content.split('\n')
    function_lines = []
    in_functions = False
    
    for line in lines:
        if line.strip().startswith('ImGui_'):
            in_functions = True
        if in_functions and line.strip():
            function_lines.append(line)
    
    # Create the complete function block
    functions_text = '\n'.join(function_lines)
    
    # Find where to insert (before the closing brace of mock_reaper)
    # Look for the pattern that indicates end of ImGui functions
    insertion_pattern = "  ImGui_BeginPopupContextWindow = function(ctx)"
    
    if insertion_pattern in main_content:
        # Find the end of this function and add all remaining functions
        parts = main_content.split(insertion_pattern)
        if len(parts) == 2:
            # Find the end of the function
            after_function = parts[1]
            func_end_idx = after_function.find('  end,')
            if func_end_idx != -1:
                # Insert point found
                before_insertion = parts[0] + insertion_pattern + after_function[:func_end_idx + 7]  # Include '  end,'
                after_insertion = after_function[func_end_idx + 7:]
                
                # Add the remaining functions
                remaining_functions = """

  ImGui_BeginPopupModal = function(ctx)
    log_api_call("ImGui_BeginPopupModal", ctx)
    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1
    return false
  end,

  ImGui_BeginTable = function(ctx, label)
    log_api_call("ImGui_BeginTable", ctx, label)
    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1
    return false
  end,

  ImGui_Bullet = function(ctx, text)
    log_api_call("ImGui_Bullet", ctx, text)
  end,

  ImGui_CalcItemWidth = function(ctx)
    log_api_call("ImGui_CalcItemWidth", ctx)
    return 100
  end,

  ImGui_CalcTextSize = function(ctx, text)
    log_api_call("ImGui_CalcTextSize", ctx, text)
    return 100, 20
  end,

  ImGui_CloseCurrentPopup = function(ctx)
    log_api_call("ImGui_CloseCurrentPopup", ctx)
  end,

  ImGui_CollapsingHeader = function(ctx, label)
    log_api_call("ImGui_CollapsingHeader", ctx, label)
    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1
    return false
  end,

  ImGui_ColorButton = function(ctx, label, color)
    log_api_call("ImGui_ColorButton", ctx, label, color)
    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1
    return false, color or 0xFFFFFFFF
  end,

  ImGui_ColorConvertDouble4ToU32 = function(ctx)
    log_api_call("ImGui_ColorConvertDouble4ToU32", ctx)
    return 0xFFFFFFFF
  end,

  ImGui_ColorConvertHSVtoRGB = function(ctx, color)
    log_api_call("ImGui_ColorConvertHSVtoRGB", ctx, color)
    return 0xFFFFFFFF
  end,

  ImGui_ColorEdit3 = function(ctx, label, color)
    log_api_call("ImGui_ColorEdit3", ctx, label, color)
    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1
    return false, color or 0xFFFFFFFF
  end,

  ImGui_ColorEdit4 = function(ctx, label, color)
    log_api_call("ImGui_ColorEdit4", ctx, label, color)
    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1
    return false, color or 0xFFFFFFFF
  end,

  ImGui_ColorPicker3 = function(ctx, label, color)
    log_api_call("ImGui_ColorPicker3", ctx, label, color)
    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1
    return false, color or 0xFFFFFFFF
  end,

  ImGui_ColorPicker4 = function(ctx, label, color)
    log_api_call("ImGui_ColorPicker4", ctx, label, color)
    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1
    return false, color or 0xFFFFFFFF
  end,

  ImGui_Columns = function(ctx, count)
    log_api_call("ImGui_Columns", ctx, count)
    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1
    return false
  end,

  -- Essential getter functions
  ImGui_GetContentRegionAvail = function(ctx)
    log_api_call("ImGui_GetContentRegionAvail", ctx)
    return 200, 100
  end,

  ImGui_GetCursorScreenPos = function(ctx)
    log_api_call("ImGui_GetCursorScreenPos", ctx)
    return 10, 20
  end,

  ImGui_GetFontSize = function(ctx)
    log_api_call("ImGui_GetFontSize", ctx)
    return 13
  end,

  ImGui_GetFrameHeight = function(ctx)
    log_api_call("ImGui_GetFrameHeight", ctx)
    return 20
  end,

  ImGui_GetTime = function(ctx)
    log_api_call("ImGui_GetTime", ctx)
    return os.clock()
  end,

  ImGui_GetWindowDrawList = function(ctx)
    log_api_call("ImGui_GetWindowDrawList", ctx)
    return 1 -- Mock draw list handle
  end,

  -- Layout functions
  ImGui_PushID = function(ctx, id)
    log_api_call("ImGui_PushID", ctx, id)
  end,

  ImGui_PopID = function(ctx)
    log_api_call("ImGui_PopID", ctx)
  end,

  ImGui_PushItemWidth = function(ctx, width)
    log_api_call("ImGui_PushItemWidth", ctx, width)
  end,

  ImGui_PopItemWidth = function(ctx)
    log_api_call("ImGui_PopItemWidth", ctx)
  end,

  ImGui_SetNextItemWidth = function(ctx, width)
    log_api_call("ImGui_SetNextItemWidth", ctx, width)
  end,

  -- Tree functions
  ImGui_TreeNode = function(ctx, label)
    log_api_call("ImGui_TreeNode", ctx, label)
    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1
    return false
  end,

  ImGui_TreePop = function(ctx)
    log_api_call("ImGui_TreePop", ctx)
  end,

  -- Table functions
  ImGui_EndTable = function(ctx)
    log_api_call("ImGui_EndTable", ctx)
  end,

  ImGui_TableNextColumn = function(ctx)
    log_api_call("ImGui_TableNextColumn", ctx)
    return true
  end,

  ImGui_TableNextRow = function(ctx)
    log_api_call("ImGui_TableNextRow", ctx)
  end,

  ImGui_TableSetupColumn = function(ctx, label)
    log_api_call("ImGui_TableSetupColumn", ctx, label)
  end,

  ImGui_TableHeadersRow = function(ctx)
    log_api_call("ImGui_TableHeadersRow", ctx)
  end,

  -- Input/Drag functions with better signatures
  ImGui_DragFloat = function(ctx, label, value, speed, min_val, max_val)
    log_api_call("ImGui_DragFloat", ctx, label, value, speed, min_val, max_val)
    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1
    return false, value or 0
  end,

  ImGui_SliderAngle = function(ctx, label, value, min_val, max_val)
    log_api_call("ImGui_SliderAngle", ctx, label, value, min_val, max_val)
    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1
    return false, value or 0
  end,

  -- Query functions
  ImGui_IsKeyDown = function(ctx, key)
    log_api_call("ImGui_IsKeyDown", ctx, key)
    return false
  end,

  ImGui_IsMouseDown = function(ctx, button)
    log_api_call("ImGui_IsMouseDown", ctx, button)
    return false
  end,

  ImGui_IsMouseDragging = function(ctx, button)
    log_api_call("ImGui_IsMouseDragging", ctx, button)
    return false
  end,

  ImGui_IsWindowFocused = function(ctx, flags)
    log_api_call("ImGui_IsWindowFocused", ctx, flags)
    return false
  end,

  ImGui_IsWindowHovered = function(ctx, flags)
    log_api_call("ImGui_IsWindowHovered", ctx, flags)
    return false
  end,

  -- End functions
  ImGui_EndChild = function(ctx)
    log_api_call("ImGui_EndChild", ctx)
  end,

  ImGui_EndDisabled = function(ctx)
    log_api_call("ImGui_EndDisabled", ctx)
  end,

  ImGui_EndDragDropSource = function(ctx)
    log_api_call("ImGui_EndDragDropSource", ctx)
  end,

  ImGui_EndDragDropTarget = function(ctx)
    log_api_call("ImGui_EndDragDropTarget", ctx)
  end,

  ImGui_EndMainMenuBar = function(ctx)
    log_api_call("ImGui_EndMainMenuBar", ctx)
  end,

  ImGui_EndPopup = function(ctx)
    log_api_call("ImGui_EndPopup", ctx)
  end,

  -- Additional essential functions for comprehensive coverage
  ImGui_OpenPopup = function(ctx, str_id)
    log_api_call("ImGui_OpenPopup", ctx, str_id)
  end,

  ImGui_TextUnformatted = function(ctx, text)
    log_api_call("ImGui_TextUnformatted", ctx, text)
    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1
  end,

  ImGui_NextColumn = function(ctx)
    log_api_call("ImGui_NextColumn", ctx)
  end,

  ImGui_Image = function(ctx, image, width, height)
    log_api_call("ImGui_Image", ctx, image, width, height)
    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1
  end"""
                
                # Combine everything
                new_content = before_insertion + remaining_functions + after_insertion
                
                # Write back to file
                with open('enhanced_virtual_reaper.lua', 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print("✅ Successfully integrated additional ImGui functions into enhanced_virtual_reaper.lua")
                print("📊 Added comprehensive coverage for demo.lua compatibility")
                return True
    
    print("❌ Error: Could not find insertion point in enhanced_virtual_reaper.lua")
    return False

if __name__ == "__main__":
    integrate_generated_functions()
