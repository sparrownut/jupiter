def setPrefixAndSuffix(filename: str, prefix="domain=", suffix="&&(title!=404)"):
    ret = ''
    with open(filename, 'r') as f:
        for it in f.readlines():
            it = it.replace('\n','')
            ret += "%s%s%s\n" % (prefix, it, suffix)
    with open(filename, 'w') as f:
        f.write(ret)
