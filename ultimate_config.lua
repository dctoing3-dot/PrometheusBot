return {
    LuaVersion = "Lua51";
    VarNamePrefix = "";
    NameGenerator = "MangledShuffled";
    PrettyPrint = false;
    Seed = 12345;
    
    Steps = {
        {Name = "EncryptStrings"; Settings = {};};
        {Name = "Vmify"; Settings = {};};
        {Name = "AntiTamper"; Settings = {};};
        {Name = "Vmify"; Settings = {};};
        {Name = "ConstantArray"; Settings = {};};
        {Name = "Vmify"; Settings = {};};
        {Name = "ProxifyLocals"; Settings = {};};
        {Name = "NumbersToExpressions"; Settings = {};};
        {Name = "WrapInFunction"; Settings = {};};
    };
}
