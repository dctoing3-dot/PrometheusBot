return {
    LuaVersion = "Lua51";
    VarNamePrefix = "";
    NameGenerator = "MangledShuffled";
    PrettyPrint = false;  -- Ini sudah minify otomatis
    Seed = 12345;
    
    Steps = {
        {Name = "EncryptStrings"; Settings = {};};
        {Name = "Vmify"; Settings = {};};
        {Name = "ConstantArray"; Settings = {};};
        {Name = "WrapInFunction"; Settings = {};};
    };
}
