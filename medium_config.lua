return {
    LuaVersion = "Lua51";
    VarNamePrefix = "";
    NameGenerator = "MangledShuffled";
    PrettyPrint = false;
    Seed = 12345;
    
    Minify = true;
    
    Steps = {
        {Name = "EncryptStrings"; Settings = {};};
        {Name = "Vmify"; Settings = {};};
        {Name = "ConstantArray"; Settings = {};};
        {Name = "NumbersToExpressions"; Settings = {};};
        {Name = "WrapInFunction"; Settings = {};};
    };
}
