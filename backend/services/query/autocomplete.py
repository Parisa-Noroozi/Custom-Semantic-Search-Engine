def autocomplete(prefix, index):
    prefix = prefix.lower()
    if prefix in index:
        return sorted(index[prefix])
    return []