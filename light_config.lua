return {
    LuaVersion = "Lua51";
    VarNamePrefix = "";
    NameGenerator = "MangledShuffled";
    PrettyPrint = false;
    Seed = 12345;
    
    Steps = {
        {Name = "EncryptStrings"; Settings = {};};
        {Name = "Vmify"; Settings = {};};
        {Name = "ConstantArray"; Settings = {};};
        {Name = "WrapInFunction"; Settings = {};};
    };
}
