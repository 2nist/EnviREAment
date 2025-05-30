#!/usr/bin/env lua
-- validation_test.lua
-- Test script for EnviREAment ImGui virtual environment

-- Load the enhanced virtual environment
dofile("enhanced_virtual_reaper.lua")

-- Create test context
local ctx = ImGui_CreateContext('ValidationTest')

print('🧪 Starting EnviREAment Validation Test')
print('=' .. string.rep('=', 40))

-- Test basic window operations
local function test_basic_operations()
  print('Testing basic window operations...')
  
  if ImGui_Begin(ctx, 'Test Window', true, 0) then
    ImGui_Text(ctx, 'Hello, Virtual World!')
    
    if ImGui_Button(ctx, 'Test Button') then
      print('Button clicked (virtual)')
    end
    
    ImGui_End(ctx)
  end
end

-- Test various widget types
local function test_widgets()
  print('Testing widget implementations...')
  
  -- Test each category of widgets
  ImGui_Text(ctx, 'Testing text widgets')
  ImGui_Button(ctx, 'Testing buttons')
  ImGui_Checkbox(ctx, 'Test Checkbox', false)
  ImGui_SliderInt(ctx, 'Test Slider', 0, 0, 100)
end

-- Run tests
test_basic_operations()
test_widgets()

-- Print statistics
print('')
print('📊 Validation Results:')
print('   • API calls made: ' .. (VirtualState.stats.api_calls or 0))
print('   • Widgets drawn: ' .. (VirtualState.stats.widgets_drawn or 0))
print('   • Errors: ' .. (VirtualState.stats.errors or 0))
print('   • Warnings: ' .. (VirtualState.stats.warnings or 0))

-- Cleanup
ImGui_DestroyContext(ctx)
print('✅ Validation test completed!')