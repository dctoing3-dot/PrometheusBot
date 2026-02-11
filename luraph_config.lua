-- Luraph-Style Configuration for Prometheus
return {
    -- Base Settings
    LuaVersion = "Lua51";
    VarNamePrefix = "";
    NameGenerator = "MangledShuffled";
    PrettyPrint = false;
    Seed = 12345; -- Fixed seed instead of os.time()
    
    -- Steps to apply
    Steps = {
        {
            Name = "Vmify";
            Settings = {
                UseDebugLibrary = false;
            };
        };
        {
            Name = "EncryptStrings";
            Settings = {
                StringsEncryptionPercentage = 1.0;
            };
        };
        {
            Name = "AntiTamper";
            Settings = {
                UseDebugLibrary = true;
            };
        };
        {
            Name = "Vmify";
            Settings = {
                UseDebugLibrary = false;
            };
        };
        {
            Name = "ConstantArray";
            Settings = {
                Shuffle = true;
                Encrypt = true;
            };
        };
        {
            Name = "ProxifyLocals";
            Settings = {};
        };
        {
            Name = "NumbersToExpressions";
            Settings = {};
        };
        {
            Name = "WrapInFunction";
            Settings = {};
        };
    };
}
