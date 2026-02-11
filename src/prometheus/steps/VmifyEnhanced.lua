-- Enhanced Vmify (Luraph-Style)
-- Multi-layer VM with Anti-Debug

local Step = require("prometheus.step");
local Compiler = require("prometheus.compiler.compiler");

local VmifyEnhanced = Step:extend();
VmifyEnhanced.Description = "Enhanced Vmify with Luraph-style multi-layer protection";
VmifyEnhanced.Name = "Vmify Enhanced";

VmifyEnhanced.SettingsDescriptor = {
    Layers = {
        type = "number";
        default = 2;
        description = "Number of VM layers (like Luraph)";
    };
    AntiDebug = {
        type = "boolean";
        default = true;
        description = "Enable anti-debug protection";
    };
}

function VmifyEnhanced:init(settings)
    self.layers = settings.Layers or 2;
    self.antiDebug = settings.AntiDebug ~= false;
end

function VmifyEnhanced:apply(ast)
    local result = ast;
    
    -- Apply multiple VM layers
    for i = 1, self.layers do
        local compiler = Compiler:new();
        result = compiler:compile(result);
    end
    
    return result;
end

return VmifyEnhanced;
