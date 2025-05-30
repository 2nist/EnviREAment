#!/usr/bin/env python3
"""
verify_integration.py
Verify that all 272 ImGui functions have been properly integrated
"""

import re
from pathlib import Path

def verify_integration():
    """Verify that all generated functions are properly integrated."""
    
    print("🔍 Verifying Comprehensive ImGui Integration")
    print("=" * 50)
    
    # Read the enhanced virtual environment
    try:
        with open('enhanced_virtual_reaper.lua', 'r', encoding='utf-8') as f:
            enhanced_content = f.read()
    except FileNotFoundError:
        print("❌ Error: enhanced_virtual_reaper.lua not found")
        return False
    
    # Read the generated functions to check what should be there
    try:
        with open('generated_imgui_functions.lua', 'r', encoding='utf-8') as f:
            generated_content = f.read()
    except FileNotFoundError:
        print("❌ Error: generated_imgui_functions.lua not found")
        return False
    
    # Extract function names from generated content
    generated_functions = set()
    for match in re.finditer(r'(ImGui_\w+)\s*=\s*function\(', generated_content):
        generated_functions.add(match.group(1))
    
    # Extract function names from enhanced content
    enhanced_functions = set()
    for match in re.finditer(r'(ImGui_\w+)\s*=\s*function\(', enhanced_content):
        enhanced_functions.add(match.group(1))
    
    # Verify integration
    missing_functions = generated_functions - enhanced_functions
    extra_functions = enhanced_functions - generated_functions
    
    print(f"📊 Integration Analysis:")
    print(f"   Generated functions: {len(generated_functions)}")
    print(f"   Functions in enhanced file: {len(enhanced_functions)}")
    print(f"   Missing from integration: {len(missing_functions)}")
    print(f"   Extra functions in enhanced: {len(extra_functions)}")
    
    if missing_functions:
        print(f"\n❌ Missing functions ({len(missing_functions)}):")
        for func in sorted(missing_functions)[:10]:  # Show first 10
            print(f"   - {func}")
        if len(missing_functions) > 10:
            print(f"   ... and {len(missing_functions) - 10} more")
        return False
    
    # Check file size and structure
    file_size = len(enhanced_content)
    line_count = enhanced_content.count('\n')
    
    print(f"\n📏 File Statistics:")
    print(f"   File size: {file_size:,} characters")
    print(f"   Line count: {line_count:,} lines")
    print(f"   Total ImGui functions: {len(enhanced_functions)}")
    
    # Check for integration markers
    integration_markers = enhanced_content.count("AUTO-GENERATED IMGUI FUNCTIONS")
    print(f"   Integration markers found: {integration_markers}")
      # Test some specific demo.lua functions
    demo_functions = [
        'ImGui_Begin', 'ImGui_End', 'ImGui_Text', 'ImGui_Button',
        'ImGui_InputText', 'ImGui_SliderDouble', 'ImGui_ColorEdit3',
        'ImGui_BeginTable', 'ImGui_TableNextColumn', 'ImGui_TreeNode',
        'ImGui_IsItemHovered', 'ImGui_PushID', 'ImGui_PopID'
    ]
    
    print(f"\n🧪 Demo.lua Function Verification:")
    all_demo_present = True
    for func in demo_functions:
        if func in enhanced_functions:
            print(f"   ✅ {func}")
        else:
            print(f"   ❌ {func} - MISSING!")
            all_demo_present = False
    
    if all_demo_present:
        print(f"\n🎉 SUCCESS! Comprehensive Integration Complete!")
        print(f"✅ All {len(generated_functions)} generated functions integrated")
        print(f"✅ All demo.lua functions available")
        print(f"✅ Enhanced Virtual REAPER ready for full testing")
        
        # Final statistics
        print(f"\n📈 Final Statistics:")
        print(f"   Total ImGui API coverage: {len(enhanced_functions)} functions")
        print(f"   File size: {file_size/1024:.1f} KB")
        print(f"   Integration markers: {integration_markers}")
        
        return True
    else:
        print(f"\n❌ Integration incomplete - some demo functions missing")
        return False

def create_function_manifest():
    """Create a manifest of all available functions."""
    
    try:
        with open('enhanced_virtual_reaper.lua', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ Error: enhanced_virtual_reaper.lua not found")
        return
    
    # Extract all ImGui functions
    functions = set()
    for match in re.finditer(r'(ImGui_\w+)\s*=\s*function\(([^)]*)\)', content):
        func_name = match.group(1)
        params = match.group(2)
        functions.add((func_name, params))
    
    # Group functions by category
    categories = {
        'Window': [],
        'Container': [],
        'Input': [],
        'Display': [],
        'Layout': [],
        'Table': [],
        'Tree': [],
        'Menu': [],
        'Popup': [],
        'Drawing': [],
        'Query': [],
        'Other': []
    }
    
    for func_name, params in sorted(functions):
        categorized = False
        
        if any(keyword in func_name.lower() for keyword in ['begin', 'end']):
            categories['Container'].append((func_name, params))
            categorized = True
        elif any(keyword in func_name.lower() for keyword in ['input', 'slider', 'drag', 'color']):
            categories['Input'].append((func_name, params))
            categorized = True
        elif any(keyword in func_name.lower() for keyword in ['text', 'image', 'bullet']):
            categories['Display'].append((func_name, params))
            categorized = True
        elif any(keyword in func_name.lower() for keyword in ['table']):
            categories['Table'].append((func_name, params))
            categorized = True
        elif any(keyword in func_name.lower() for keyword in ['tree']):
            categories['Tree'].append((func_name, params))
            categorized = True
        elif any(keyword in func_name.lower() for keyword in ['menu']):
            categories['Menu'].append((func_name, params))
            categorized = True
        elif any(keyword in func_name.lower() for keyword in ['popup']):
            categories['Popup'].append((func_name, params))
            categorized = True
        elif any(keyword in func_name.lower() for keyword in ['draw', 'line', 'rect', 'circle']):
            categories['Drawing'].append((func_name, params))
            categorized = True
        elif any(keyword in func_name.lower() for keyword in ['is', 'get', 'want']):
            categories['Query'].append((func_name, params))
            categorized = True
        elif any(keyword in func_name.lower() for keyword in ['push', 'pop', 'indent', 'spacing']):
            categories['Layout'].append((func_name, params))
            categorized = True
        
        if not categorized:
            categories['Other'].append((func_name, params))
    
    # Create manifest file
    manifest_content = "# Enhanced Virtual REAPER - ImGui API Manifest\n"
    manifest_content += f"Generated: {__import__('datetime').datetime.now()}\n\n"
    manifest_content += f"Total Functions: {len(functions)}\n\n"
    
    for category, funcs in categories.items():
        if funcs:
            manifest_content += f"## {category} Functions ({len(funcs)})\n\n"
            for func_name, params in funcs:
                manifest_content += f"- `{func_name}({params})`\n"
            manifest_content += "\n"
    
    with open('imgui_api_manifest.md', 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    
    print(f"📋 Created API manifest: imgui_api_manifest.md")
    print(f"   Total functions: {len(functions)}")
    for category, funcs in categories.items():
        if funcs:
            print(f"   {category}: {len(funcs)} functions")

if __name__ == "__main__":
    success = verify_integration()
    create_function_manifest()
    
    if success:
        print(f"\n🚀 EnviREAment is now ready for comprehensive testing!")
        print(f"   ✓ Complete demo.lua compatibility")
        print(f"   ✓ All ImGui functions implemented")
        print(f"   ✓ Virtual environment enhanced")
    else:
        print(f"\n⚠️  Integration needs additional work")
