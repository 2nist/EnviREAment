#!/usr/bin/env python3
"""
imgui_api_generator.py
Automated ImGui API Function Generator for EnviREAment
Extracts ALL ImGui functions from demo.lua and generates virtual implementations
"""

import re
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple

class ImGuiAPIGenerator:
    def __init__(self):
        self.patterns = [
            r'ImGui\.(\w+)\s*\(',  # ImGui.FunctionName(
            r'r\.ImGui_(\w+)\s*\(',  # r.ImGui_FunctionName(
            r'ImGui_(\w+)\s*\(',  # ImGui_FunctionName(
            r'ctx\.(\w+)\s*\(',  # ctx.FunctionName(
        ]
        
        self.categories = [
            {'pattern': r'^Begin', 'category': 'container', 'returns': 'boolean'},
            {'pattern': r'^End', 'category': 'container', 'returns': 'nil'},
            {'pattern': r'^Get', 'category': 'getter', 'returns': 'value'},
            {'pattern': r'^Set', 'category': 'setter', 'returns': 'nil'},
            {'pattern': r'^Is', 'category': 'query', 'returns': 'boolean'},
            {'pattern': r'^Push', 'category': 'stack', 'returns': 'nil'},
            {'pattern': r'^Pop', 'category': 'stack', 'returns': 'nil'},
            {'pattern': r'Button$', 'category': 'widget', 'returns': 'boolean'},
            {'pattern': r'Input', 'category': 'input', 'returns': 'boolean, value'},
            {'pattern': r'Slider', 'category': 'input', 'returns': 'boolean, value'},
            {'pattern': r'Drag', 'category': 'input', 'returns': 'boolean, value'},
            {'pattern': r'Color', 'category': 'color', 'returns': 'boolean, value'},
            {'pattern': r'Text', 'category': 'display', 'returns': 'nil'},
            {'pattern': r'Image', 'category': 'display', 'returns': 'nil'},
            {'pattern': r'Tree', 'category': 'tree', 'returns': 'boolean'},
            {'pattern': r'Table', 'category': 'table', 'returns': 'boolean'},
            {'pattern': r'Menu', 'category': 'menu', 'returns': 'boolean'},
            {'pattern': r'Tab', 'category': 'tab', 'returns': 'boolean'},
            {'pattern': r'Popup', 'category': 'popup', 'returns': 'boolean'},
            {'pattern': r'Flags', 'category': 'constant', 'returns': 'number'},
            {'pattern': r'Col_', 'category': 'constant', 'returns': 'number'},
            {'pattern': r'Key_', 'category': 'constant', 'returns': 'number'},
        ]

    def extract_imgui_functions(self, file_path: str) -> Dict[str, Dict]:
        """Extract all ImGui function calls from a lua file."""
        functions = {}
        
        print(f"📁 Extracting ImGui functions from: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            print(f"❌ Error: Could not open file: {file_path}")
            return functions
        
        # Extract function calls using multiple patterns
        for pattern in self.patterns:
            matches = re.findall(pattern, content)
            for func_name in matches:
                if func_name not in functions:
                    functions[func_name] = {
                        'name': func_name,
                        'count': 0,
                        'variations': []
                    }
                functions[func_name]['count'] += 1
        
        # Extract function signatures for parameter analysis
        for func_name in functions:
            sig_pattern = rf'ImGui\.?{re.escape(func_name)}\s*\(([^)]*)'
            signatures = re.findall(sig_pattern, content)
            functions[func_name]['variations'] = signatures
        
        print(f"✅ Extracted {len(functions)} unique ImGui functions")
        return functions

    def analyze_current_implementation(self, virtual_env_path: str) -> Set[str]:
        """Check what functions are already implemented in virtual environment."""
        implemented = set()
        
        print(f"🔍 Analyzing current implementation: {virtual_env_path}")
        
        try:
            with open(virtual_env_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            print(f"❌ Error: Could not open file: {virtual_env_path}")
            return implemented
        
        # Extract currently implemented ImGui functions
        pattern = r'ImGui_(\w+)\s*=\s*function'
        matches = re.findall(pattern, content)
        implemented.update(matches)
        
        print(f"✅ Found {len(implemented)} implemented functions")
        return implemented

    def analyze_function_signature(self, func_name: str, variations: List[str]) -> Dict:
        """Analyze function parameters from usage patterns."""
        signature = {
            'name': func_name,
            'params': ['ctx'],  # All ImGui functions start with context
            'returns': 'nil',  # Default return
            'category': 'unknown'
        }
        
        # Categorize functions by name patterns
        for cat in self.categories:
            if re.search(cat['pattern'], func_name):
                signature['category'] = cat['category']
                signature['returns'] = cat['returns']
                break
        
        # Add common parameters based on function type
        if signature['category'] == 'input':
            signature['params'].extend(['label', 'value'])
        elif signature['category'] == 'display':
            signature['params'].append('text')
        elif signature['category'] == 'widget':
            signature['params'].append('label')
        elif signature['category'] == 'getter':
            pass  # Getters usually just need context
        elif signature['category'] == 'setter':
            signature['params'].append('value')
        
        # Add specific parameters based on function name
        if 'Size' in func_name:
            if signature['category'] != 'getter':
                signature['params'].extend(['width', 'height'])
        
        if 'Pos' in func_name:
            if signature['category'] != 'getter':
                signature['params'].extend(['x', 'y'])
        
        if 'Color' in func_name:
            signature['params'].append('color')
        
        if 'Flags' in func_name or func_name.endswith('Flags'):
            signature['params'].append('flags')
        
        return signature

    def generate_function_implementation(self, signature: Dict) -> str:
        """Generate virtual implementation for a function."""
        code = []
        
        # Function declaration
        params_str = ', '.join(signature['params'])
        code.append(f"  ImGui_{signature['name']} = function({params_str})")
        
        # Logging call
        log_params_str = ', '.join(signature['params'])
        code.append(f'    log_api_call("ImGui_{signature["name"]}", {log_params_str})')
        
        # Category-specific behavior
        category = signature['category']
        
        if category == 'getter':
            code.append("    -- Return mock values for getter functions")
            if 'Size' in signature['name']:
                code.append("    return 100, 50  -- Mock width, height")
            elif 'Pos' in signature['name']:
                code.append("    return 10, 20  -- Mock x, y")
            elif 'Color' in signature['name']:
                code.append("    return 0xFFFFFFFF  -- Mock color")
            else:
                code.append("    return 0  -- Mock value")
                
        elif category == 'query':
            code.append("    -- Return false for query functions in virtual mode")
            code.append("    return false")
            
        elif category == 'input':
            code.append("    -- Return unchanged value for input widgets")
            code.append("    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1")
            code.append("    return false, value or 0")
            
        elif category in ['widget', 'container']:
            code.append("    -- Return false for interactive widgets in virtual mode")
            code.append("    VirtualState.stats.widgets_drawn = VirtualState.stats.widgets_drawn + 1")
            code.append("    return false")
            
        elif category == 'constant':
            code.append("    -- Return mock constant value")
            code.append("    return 0")
            
        else:
            code.append("    -- Default virtual implementation")
            if signature['returns'] != 'nil':
                return_val = 'false' if 'boolean' in signature['returns'] else '0'
                code.append(f"    return {return_val}")
        
        code.append("  end,")
        code.append("")
        
        return '\n'.join(code)

    def generate_missing_functions(self, demo_path: str, virtual_env_path: str, output_path: str):
        """Generate missing ImGui functions."""
        print("🚀 Starting ImGui API Generation Process")
        print("=" * 50)
        
        # Step 1: Extract functions from demo
        demo_functions = self.extract_imgui_functions(demo_path)
        
        # Step 2: Analyze current implementation
        implemented = self.analyze_current_implementation(virtual_env_path)
        
        # Step 3: Find missing functions
        missing = {name: data for name, data in demo_functions.items() 
                  if name not in implemented}
        
        print(f"\n📊 Analysis Results:")
        print(f"   • Functions in demo.lua: {len(demo_functions)}")
        print(f"   • Currently implemented: {len(implemented)}")
        print(f"   • Missing functions: {len(missing)}")
        
        if not missing:
            print("✅ All functions are already implemented!")
            return
        
        # Step 4: Generate implementations
        print("\n🔧 Generating missing function implementations...")
        
        generated_code = [
            "  -- ==================== AUTO-GENERATED IMGUI FUNCTIONS ====================",
            "  -- Generated by imgui_api_generator.py",
            f"  -- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ]
        
        # Sort functions by name for organized output
        sorted_functions = sorted(missing.keys())
        
        for func_name in sorted_functions:
            func_data = missing[func_name]
            print(f"   • Generating: ImGui_{func_name} (used {func_data['count']} times)")
            
            signature = self.analyze_function_signature(func_name, func_data['variations'])
            implementation = self.generate_function_implementation(signature)
            generated_code.append(implementation)
        
        # Step 5: Write output
        print(f"\n💾 Writing generated code to: {output_path}")
        
        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(generated_code))
        except IOError:
            print(f"❌ Error: Could not create output file: {output_path}")
            return
        
        print("✅ Generation complete!")
        print(f"📄 Generated {len(missing)} function implementations")
        
        # Step 6: Generate integration instructions
        self.generate_integration_instructions(output_path, len(missing))
        
        # Step 7: Create validation script
        self.create_validation_script(output_path)

    def generate_integration_instructions(self, output_path: str, count: int):
        """Generate instructions for integrating the new functions."""
        instructions_path = output_path.replace('.lua', '_integration_instructions.txt')
        
        instructions = [
            "INTEGRATION INSTRUCTIONS FOR AUTO-GENERATED IMGUI FUNCTIONS",
            "=" * 60,
            "",
            f"Generated {count} missing ImGui function implementations.",
            "",
            "To integrate these functions into enhanced_virtual_reaper.lua:",
            "",
            "1. Open enhanced_virtual_reaper.lua",
            "2. Locate the end of the existing ImGui function definitions",
            f"3. Insert the generated code from: {os.path.basename(output_path)}",
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
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ]
        
        try:
            with open(instructions_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(instructions))
            print(f"📋 Integration instructions written to: {os.path.basename(instructions_path)}")
        except IOError:
            print(f"❌ Error: Could not create instructions file: {instructions_path}")

    def create_validation_script(self, output_path: str):
        """Create a test script to validate the virtual environment."""
        test_path = output_path.replace('.lua', '_validation_test.lua')
        
        test_code = [
            "#!/usr/bin/env lua",
            "-- validation_test.lua",
            "-- Test script for EnviREAment ImGui virtual environment",
            "",
            "-- Load the enhanced virtual environment",
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
        ]
        
        try:
            with open(test_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(test_code))
            print(f"🧪 Validation test script created: {os.path.basename(test_path)}")
        except IOError:
            print(f"❌ Error: Could not create test file: {test_path}")

    def run(self):
        """Main function to run the generator."""
        demo_path = r"c:\Users\CraftAuto-Sales\Downloads\reaimgui-master-git\reaimgui-master\examples\demo.lua"
        virtual_env_path = r"c:\Users\CraftAuto-Sales\AppData\Roaming\REAPER\Scripts\EnviREAment\EnviREAment\enhanced_virtual_reaper.lua"
        output_path = r"c:\Users\CraftAuto-Sales\AppData\Roaming\REAPER\Scripts\EnviREAment\EnviREAment\generated_imgui_functions.lua"
        
        # Verify input files exist
        if not Path(demo_path).exists():
            print(f"❌ Error: Demo file not found: {demo_path}")
            print("Please ensure the reaimgui demo.lua file is available.")
            return
        
        if not Path(virtual_env_path).exists():
            print(f"❌ Error: Virtual environment file not found: {virtual_env_path}")
            return
        
        # Run the generation process
        self.generate_missing_functions(demo_path, virtual_env_path, output_path)
        
        print("\n🎉 ImGui API Generation Process Complete!")
        print("Next steps:")
        print("1. Review generated functions in: generated_imgui_functions.lua")
        print("2. Integrate them into enhanced_virtual_reaper.lua")
        print("3. Run validation test: generated_imgui_functions_validation_test.lua")

if __name__ == "__main__":
    generator = ImGuiAPIGenerator()
    generator.run()
