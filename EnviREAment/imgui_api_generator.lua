#!/usr/bin/env lua
-- imgui_api_generator.lua
-- Automated ImGui API Function Generator for EnviREAment
-- Extracts ALL ImGui functions from demo.lua and generates virtual implementations

local Generator = {}

-- ==================== API EXTRACTION SYSTEM ====================

-- Extract all ImGui function calls from a lua file
function Generator.extract_imgui_functions(file_path)
    local functions = {}
    local function_patterns = {}
    
    print("📁 Extracting ImGui functions from: " .. file_path)
    
    local file = io.open(file_path, "r")
    if not file then
        print("❌ Error: Could not open file: " .. file_path)
        return functions
    end
    
    local content = file:read("*all")
    file:close()
    
    -- Enhanced pattern matching for ImGui function calls
    local patterns = {
        "ImGui%.([%w_]+)%s*%(", -- ImGui.FunctionName(
        "r%.ImGui_([%w_]+)%s*%(", -- r.ImGui_FunctionName(
        "ImGui_([%w_]+)%s*%(", -- ImGui_FunctionName(
        "ctx%.([%w_]+)%s*%(", -- ctx.FunctionName( (for method-style calls)
    }
    
    for _, pattern in ipairs(patterns) do
        for func_name in content:gmatch(pattern) do
            if not functions[func_name] then
                functions[func_name] = {
                    name = func_name,
                    count = 0,
                    variations = {}
                }
            end
            functions[func_name].count = functions[func_name].count + 1
        end
    end
    
    -- Also extract function signatures with parameter analysis
    for func_name, func_data in pairs(functions) do
        local sig_pattern = "ImGui%.?" .. func_name .. "%s*%(([^%)]*)"
        for signature in content:gmatch(sig_pattern) do
            table.insert(func_data.variations, signature)
        end
    end
    
    print(string.format("✅ Extracted %d unique ImGui functions", table_count(functions)))
    return functions
end

-- Count table entries
function table_count(t)
    local count = 0
    for _ in pairs(t) do count = count + 1 end
    return count
end

-- ==================== IMPLEMENTATION ANALYSIS ====================

-- Check what functions are already implemented in virtual environment
function Generator.analyze_current_implementation(virtual_env_path)
    local implemented = {}
    
    print("🔍 Analyzing current implementation: " .. virtual_env_path)
    
    local file = io.open(virtual_env_path, "r")
    if not file then
        print("❌ Error: Could not open file: " .. virtual_env_path)
        return implemented
    end
    
    local content = file:read("*all")
    file:close()
    
    -- Extract currently implemented ImGui functions
    for func_name in content:gmatch("ImGui_([%w_]+)%s*=%s*function") do
        implemented[func_name] = true
    end
    
    print(string.format("✅ Found %d implemented functions", table_count(implemented)))
    return implemented
end

-- ==================== FUNCTION SIGNATURE ANALYSIS ====================

-- Analyze function parameters from usage patterns
function Generator.analyze_function_signature(func_name, variations)
    local signature = {
        name = func_name,
        params = {"ctx"}, -- All ImGui functions start with context
        returns = "nil", -- Default return
        category = "unknown"
    }
    
    -- Categorize functions by name patterns
    local categories = {
        {pattern = "^Begin", category = "container", returns = "boolean"},
        {pattern = "^End", category = "container", returns = "nil"},
        {pattern = "^Get", category = "getter", returns = "value"},
        {pattern = "^Set", category = "setter", returns = "nil"},
        {pattern = "^Is", category = "query", returns = "boolean"},
        {pattern = "^Push", category = "stack", returns = "nil"},
        {pattern = "^Pop", category = "stack", returns = "nil"},
        {pattern = "Button$", category = "widget", returns = "boolean"},
        {pattern = "Input", category = "input", returns = "boolean, value"},
        {pattern = "Slider", category = "input", returns = "boolean, value"},
        {pattern = "Drag", category = "input", returns = "boolean, value"},
        {pattern = "Color", category = "color", returns = "boolean, value"},
        {pattern = "Text", category = "display", returns = "nil"},
        {pattern = "Image", category = "display", returns = "nil"},
        {pattern = "Tree", category = "tree", returns = "boolean"},
        {pattern = "Table", category = "table", returns = "boolean"},
        {pattern = "Menu", category = "menu", returns = "boolean"},
        {pattern = "Tab", category = "tab", returns = "boolean"},
        {pattern = "Popup", category = "popup", returns = "boolean"},
        {pattern = "Flags", category = "constant", returns = "number"},
        {pattern = "Col_", category = "constant", returns = "number"},
        {pattern = "Key_", category = "constant", returns = "number"},
    }
    
    for _, cat in ipairs(categories) do
        if func_name:match(cat.pattern) then
            signature.category = cat.category
            signature.returns = cat.returns
            break
        end
    end
    
    -- Analyze parameter patterns from variations
    local common_params = {
        -- Text/Label functions
        {pattern = "text", params = {"text"}},
        {pattern = "label", params = {"label"}},
        {pattern = "hint", params = {"label", "hint"}},
        
        -- Size parameters
        {pattern = "size", params = {"size_w", "size_h"}},
        {pattern = "width.*height", params = {"width", "height"}},
        
        -- Value parameters
        {pattern = "value", params = {"value"}},
        {pattern = "min.*max", params = {"v_min", "v_max"}},
        
        -- Flags
        {pattern = "flags", params = {"flags"}},
        
        -- Colors
        {pattern = "color", params = {"color"}},
        {pattern = "col", params = {"col"}},
        
        -- Position
        {pattern = "pos", params = {"x", "y"}},
        
        -- ID/Name
        {pattern = "id", params = {"str_id"}},
        {pattern = "name", params = {"name"}},
    }
    
    -- Add common parameters based on function type
    if signature.category == "input" then
        table.insert(signature.params, "label")
        table.insert(signature.params, "value")
    elseif signature.category == "display" then
        table.insert(signature.params, "text")
    elseif signature.category == "widget" then
        table.insert(signature.params, "label")
    end
    
    return signature
end

-- ==================== CODE GENERATION ====================

-- Generate virtual implementation for a function
function Generator.generate_function_implementation(signature)
    local code = {}
    
    -- Function declaration
    local params_str = table.concat(signature.params, ", ")
    table.insert(code, string.format("  ImGui_%s = function(%s)", signature.name, params_str))
    
    -- Logging call
    local log_params = {}
    for _, param in ipairs(signature.params) do
        table.insert(log_params, param)
    end
    local log_params_str = table.concat(log_params, ", ")
    table.insert(code, string.format('    log_api_call("ImGui_%s", %s)', signature.name, log_params_str))
    
    -- Category-specific behavior
    if signature.category == "getter" then
        table.insert(code, "    -- Return mock values for getter functions")
        if signature.name:match("Size") then
            table.insert(code, "    return 100, 50  -- Mock width, height")
        elseif signature.name:match("Pos") then
            table.insert(code, "    return 10, 20  -- Mock x, y")
        elseif signature.name:match("Color") then
            table.insert(code, "    return 0xFFFFFFFF  -- Mock color")
        else
            table.insert(code, "    return 0  -- Mock value")
        end
    elseif signature.category == "query" then
        table.insert(code, "    -- Return false for query functions in virtual mode")
        table.insert(code, "    return false")
    elseif signature.category == "input" then
        table.insert(code, "    -- Return unchanged value for input widgets")
        table.insert(code, "    return false, value or 0")
    elseif signature.category == "widget" or signature.category == "container" then
        table.insert(code, "    -- Return false for interactive widgets in virtual mode")
        table.insert(code, "    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1")
        table.insert(code, "    return false")
    elseif signature.category == "constant" then
        table.insert(code, "    -- Return mock constant value")
        table.insert(code, "    return 0")
    else
        table.insert(code, "    -- Default virtual implementation")
        if signature.returns ~= "nil" then
            table.insert(code, "    return " .. (signature.returns:match("boolean") and "false" or "0"))
        end
    end
    
    table.insert(code, "  end,")
    table.insert(code, "")
    
    return table.concat(code, "\n")
end

-- ==================== MAIN GENERATION LOGIC ====================

-- Generate missing ImGui functions
function Generator.generate_missing_functions(demo_path, virtual_env_path, output_path)
    print("🚀 Starting ImGui API Generation Process")
    print("=" .. string.rep("=", 50))
    
    -- Step 1: Extract functions from demo
    local demo_functions = Generator.extract_imgui_functions(demo_path)
    
    -- Step 2: Analyze current implementation
    local implemented = Generator.analyze_current_implementation(virtual_env_path)
    
    -- Step 3: Find missing functions
    local missing = {}
    for func_name, func_data in pairs(demo_functions) do
        if not implemented[func_name] then
            missing[func_name] = func_data
        end
    end
    
    print(string.format("📊 Analysis Results:"))
    print(string.format("   • Functions in demo.lua: %d", table_count(demo_functions)))
    print(string.format("   • Currently implemented: %d", table_count(implemented)))
    print(string.format("   • Missing functions: %d", table_count(missing)))
    
    if table_count(missing) == 0 then
        print("✅ All functions are already implemented!")
        return
    end
    
    -- Step 4: Generate implementations
    print("\n🔧 Generating missing function implementations...")
    
    local generated_code = {}
    table.insert(generated_code, "  -- ==================== AUTO-GENERATED IMGUI FUNCTIONS ====================")
    table.insert(generated_code, "  -- Generated by imgui_api_generator.lua")
    table.insert(generated_code, "  -- Date: " .. os.date("%Y-%m-%d %H:%M:%S"))
    table.insert(generated_code, "")
    
    -- Sort functions by name for organized output
    local sorted_functions = {}
    for func_name in pairs(missing) do
        table.insert(sorted_functions, func_name)
    end
    table.sort(sorted_functions)
    
    for _, func_name in ipairs(sorted_functions) do
        local func_data = missing[func_name]
        print(string.format("   • Generating: ImGui_%s (used %d times)", func_name, func_data.count))
        
        local signature = Generator.analyze_function_signature(func_name, func_data.variations)
        local implementation = Generator.generate_function_implementation(signature)
        table.insert(generated_code, implementation)
    end
    
    -- Step 5: Write output
    print(string.format("\n💾 Writing generated code to: %s", output_path))
    
    local output_file = io.open(output_path, "w")
    if not output_file then
        print("❌ Error: Could not create output file: " .. output_path)
        return
    end
    
    output_file:write(table.concat(generated_code, "\n"))
    output_file:close()
    
    print("✅ Generation complete!")
    print(string.format("📄 Generated %d function implementations", table_count(missing)))
    
    -- Step 6: Generate integration instructions
    Generator.generate_integration_instructions(output_path, table_count(missing))
end

-- Generate instructions for integrating the new functions
function Generator.generate_integration_instructions(output_path, count)
    local instructions_path = output_path:gsub("%.lua$", "_integration_instructions.txt")
    
    local instructions = {
        "INTEGRATION INSTRUCTIONS FOR AUTO-GENERATED IMGUI FUNCTIONS",
        "=" .. string.rep("=", 60),
        "",
        string.format("Generated %d missing ImGui function implementations.", count),
        "",
        "To integrate these functions into enhanced_virtual_reaper.lua:",
        "",
        "1. Open enhanced_virtual_reaper.lua",
        "2. Locate the end of the existing ImGui function definitions",
        "3. Insert the generated code from: " .. output_path,
        "4. Make sure the functions are inside the main EnhancedVirtualReaper table",
        "5. Test the implementation with demo.lua",
        "",
        "TESTING:",
        "- Run the demo.lua script with the enhanced virtual environment",
        "- Check for any missing function errors",
        "- Verify that all function calls are logged properly",
        "",
        "CUSTOMIZATION:",
        "- Review generated functions for more realistic behavior",
        "- Add proper parameter validation where needed",
        "- Implement category-specific mock data as required",
        "",
        "Generated: " .. os.date("%Y-%m-%d %H:%M:%S"),
    }
    
    local file = io.open(instructions_path, "w")
    if file then
        file:write(table.concat(instructions, "\n"))
        file:close()
        print("📋 Integration instructions written to: " .. instructions_path)
    end
end

-- ==================== VALIDATION SYSTEM ====================

-- Create a test script to validate the virtual environment
function Generator.create_validation_script(output_path)
    local test_path = output_path:gsub("%.lua$", "_validation_test.lua")
    
    local test_code = {
        "#!/usr/bin/env lua",
        "-- validation_test.lua",
        "-- Test script for EnviREAment ImGui virtual environment",
        "",
        '-- Load the enhanced virtual environment',
        'dofile("enhanced_virtual_reaper.lua")',
        "",
        "-- Create test context",
        "local ctx = ImGui_CreateContext('ValidationTest')",
        "",
        "print('🧪 Starting EnviREAment Validation Test')",
        "print('=' .. string.rep('=', 40))",
        "",
        "-- Test basic window operations",
        "local function test_basic_operations()",
        "  print('Testing basic window operations...')",
        "  ",
        "  if ImGui_Begin(ctx, 'Test Window', true, 0) then",
        "    ImGui_Text(ctx, 'Hello, Virtual World!')",
        "    ",
        "    if ImGui_Button(ctx, 'Test Button') then",
        "      print('Button clicked (virtual)')",
        "    end",
        "    ",
        "    ImGui_End(ctx)",
        "  end",
        "end",
        "",
        "-- Test various widget types",
        "local function test_widgets()",
        "  print('Testing widget implementations...')",
        "  ",
        "  -- Test each category of widgets",
        "  ImGui_Text(ctx, 'Testing text widgets')",
        "  ImGui_Button(ctx, 'Testing buttons')",
        "  ImGui_Checkbox(ctx, 'Test Checkbox', false)",
        "  ImGui_SliderInt(ctx, 'Test Slider', 0, 0, 100)",
        "end",
        "",
        "-- Run tests",
        "test_basic_operations()",
        "test_widgets()",
        "",
        "-- Print statistics",
        "print('')",
        "print('📊 Validation Results:')",
        "print('   • API calls made: ' .. (VirtualState.stats.api_calls or 0))",
        "print('   • Widgets drawn: ' .. (VirtualState.stats.widgets_drawn or 0))",
        "print('   • Errors: ' .. (VirtualState.stats.errors or 0))",
        "print('   • Warnings: ' .. (VirtualState.stats.warnings or 0))",
        "",
        "-- Cleanup",
        "ImGui_DestroyContext(ctx)",
        "print('✅ Validation test completed!')",
    }
    
    local file = io.open(test_path, "w")
    if file then
        file:write(table.concat(test_code, "\n"))
        file:close()
        print("🧪 Validation test script created: " .. test_path)
    end
end

-- ==================== MAIN EXECUTION ====================

-- Main function to run the generator
function Generator.run()
    local demo_path = "c:\\Users\\CraftAuto-Sales\\Downloads\\reaimgui-master-git\\reaimgui-master\\examples\\demo.lua"
    local virtual_env_path = "c:\\Users\\CraftAuto-Sales\\AppData\\Roaming\\REAPER\\Scripts\\EnviREAment\\EnviREAment\\enhanced_virtual_reaper.lua"
    local output_path = "c:\\Users\\CraftAuto-Sales\\AppData\\Roaming\\REAPER\\Scripts\\EnviREAment\\EnviREAment\\generated_imgui_functions.lua"
    
    -- Verify input files exist
    local demo_file = io.open(demo_path, "r")
    if not demo_file then
        print("❌ Error: Demo file not found: " .. demo_path)
        print("Please ensure the reaimgui demo.lua file is available.")
        return
    end
    demo_file:close()
    
    local virtual_file = io.open(virtual_env_path, "r")
    if not virtual_file then
        print("❌ Error: Virtual environment file not found: " .. virtual_env_path)
        return
    end
    virtual_file:close()
    
    -- Run the generation process
    Generator.generate_missing_functions(demo_path, virtual_env_path, output_path)
    
    -- Create validation script
    Generator.create_validation_script(output_path)
    
    print("\n🎉 ImGui API Generation Process Complete!")
    print("Next steps:")
    print("1. Review generated functions in: generated_imgui_functions.lua")
    print("2. Integrate them into enhanced_virtual_reaper.lua")
    print("3. Run validation test: generated_imgui_functions_validation_test.lua")
end

-- Export the generator
return Generator
