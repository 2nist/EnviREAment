#!/usr/bin/env lua
-- comprehensive_demo_test.lua
-- Test the enhanced virtual environment with demo.lua patterns

-- Load the enhanced virtual environment
package.path = package.path .. ";./?/init.lua"
dofile("enhanced_virtual_reaper.lua")

-- Initialize the environment
local mock_reaper = EnhancedVirtualReaper.create_environment()

print("🧪 Starting Comprehensive Demo.lua Compatibility Test")
print("=" .. string.rep("=", 50))

-- Create test context
local ctx = mock_reaper.ImGui_CreateContext('DemoTest')

-- Test critical demo.lua functions
local function test_demo_functions()
    print("Testing demo.lua function compatibility...")
    
    -- Test window creation
    if mock_reaper.ImGui_Begin(ctx, 'Demo Window Test', true, 0) then
        -- Test basic widgets
        mock_reaper.ImGui_Text(ctx, 'Demo compatibility test')
        
        -- Test tree nodes (heavily used in demo)
        if mock_reaper.ImGui_TreeNode(ctx, 'Test Tree Node') then
            mock_reaper.ImGui_Text(ctx, 'Tree content')
            mock_reaper.ImGui_TreePop(ctx)
        end
        
        -- Test tables (major demo feature)
        if mock_reaper.ImGui_BeginTable(ctx, 'Test Table') then
            mock_reaper.ImGui_TableSetupColumn(ctx, 'Column 1')
            mock_reaper.ImGui_TableHeadersRow(ctx)
            mock_reaper.ImGui_TableNextRow(ctx)
            mock_reaper.ImGui_TableNextColumn(ctx)
            mock_reaper.ImGui_Text(ctx, 'Cell content')
            mock_reaper.ImGui_EndTable(ctx)
        end
        
        -- Test input widgets
        local changed, value = mock_reaper.ImGui_DragFloat(ctx, 'Test Drag', 1.0, 0.1, 0.0, 10.0)
        local changed2, color = mock_reaper.ImGui_ColorEdit4(ctx, 'Test Color', 0xFFFFFFFF)
        
        -- Test layout functions
        mock_reaper.ImGui_PushID(ctx, 1)
        mock_reaper.ImGui_Button(ctx, 'Test Button')
        mock_reaper.ImGui_PopID(ctx)
        
        -- Test getter functions
        local width, height = mock_reaper.ImGui_GetContentRegionAvail(ctx)
        local x, y = mock_reaper.ImGui_GetCursorScreenPos(ctx)
        local font_size = mock_reaper.ImGui_GetFontSize(ctx)
        
        mock_reaper.ImGui_End(ctx)
    end
end

-- Test drawing functions
local function test_drawing_functions()
    print("Testing ImGui drawing functions...")
    
    local draw_list = mock_reaper.ImGui_GetWindowDrawList(ctx)
    if draw_list then
        -- These are heavily used in demo for custom drawing
        if mock_reaper.ImGui_DrawList_AddLine then
            mock_reaper.ImGui_DrawList_AddLine(draw_list, 0, 0, 100, 100, 0xFFFFFFFF, 1.0)
        end
        if mock_reaper.ImGui_DrawList_AddRect then
            mock_reaper.ImGui_DrawList_AddRect(draw_list, 10, 10, 50, 50, 0xFFFFFFFF, 0, 1.0)
        end
    end
end

-- Test query functions
local function test_query_functions()
    print("Testing ImGui query functions...")
    
    -- These are used throughout demo for interactive behavior
    local is_hovered = mock_reaper.ImGui_IsItemHovered(ctx, 0)
    local is_focused = mock_reaper.ImGui_IsWindowFocused(ctx, 0)
    local is_key_down = mock_reaper.ImGui_IsKeyDown and mock_reaper.ImGui_IsKeyDown(ctx, 65) -- 'A' key
    local is_mouse_down = mock_reaper.ImGui_IsMouseDown and mock_reaper.ImGui_IsMouseDown(ctx, 0)
end

-- Run all tests
test_demo_functions()
test_drawing_functions()
test_query_functions()

-- Print final statistics
print("")
print("📊 Test Results:")
print("   • API calls made: " .. (VirtualState.stats.api_calls or 0))
print("   • Widgets drawn: " .. (VirtualState.stats.widgets_drawn or 0))
print("   • Errors: " .. (VirtualState.stats.errors or 0))
print("   • Warnings: " .. (VirtualState.stats.warnings or 0))

-- Test if we can handle a subset of actual demo.lua calls
print("")
print("🎯 Demo.lua Function Coverage Test:")

local demo_functions = {
    "TreeNode", "TreePop", "BeginTable", "EndTable", "TableSetupColumn",
    "TableHeadersRow", "TableNextRow", "TableNextColumn", "DragFloat",
    "ColorEdit4", "PushID", "PopID", "GetContentRegionAvail", 
    "GetCursorScreenPos", "GetFontSize", "IsWindowFocused", "IsItemHovered"
}

local covered = 0
local total = #demo_functions

for _, func_name in ipairs(demo_functions) do
    local full_name = "ImGui_" .. func_name
    if mock_reaper[full_name] then
        covered = covered + 1
        print("   ✅ " .. full_name)
    else
        print("   ❌ " .. full_name .. " - MISSING")
    end
end

print("")
print("Coverage: " .. covered .. "/" .. total .. " (" .. math.floor(covered/total*100) .. "%)")

-- Cleanup
mock_reaper.ImGui_DestroyContext(ctx)
print("✅ Comprehensive demo compatibility test completed!")