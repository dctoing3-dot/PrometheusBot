return {
    LuaVersion = "Lua51";
    VarNamePrefix = "";
    NameGenerator = "MangledShuffled";
    PrettyPrint = false;
    Seed = 12345;
    
    -- Pengaturan agar output padat
    Minify = true;
    
    Steps = {
        {Name = "EncryptStrings"; Settings = {};};
        {Name = "Vmify"; Settings = {};};
        {Name = "ConstantArray"; Settings = {};};
        {Name = "WrapInFunction"; Settings = {};};
    };
}
