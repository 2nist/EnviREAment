#!/usr/bin/env lua
-- run_imgui_generator.lua
-- Main script to run the ImGui API generator

print("🚀 EnviREAment ImGui API Generator")
print("==================================")

-- Load the generator module
local Generator = dofile("imgui_api_generator.lua")

-- Run the generation process
Generator.run()
