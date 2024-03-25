class Node:

    @classmethod
    @property
    def items(cls):
        return [getattr(cls, k) for k in cls.__dict__ if not k.startswith('_') and not k in ('items', 'self')]

    @classmethod
    @property
    def items_map(cls):
        return {k: getattr(cls, k) for k in cls.__dict__ if not k.startswith('_') and not k in ('items', 'self')}

    @classmethod
    @property
    def item_names(cls):
        return [k for k in cls.__dict__.keys() if not k.startswith('_') and not k in ('items', 'self')]

    @classmethod
    def item_name(cls, selector):
        for c in cls, *cls.items:
            for k, v in c.items_map.items():
                if selector == v:
                    return k
    @classmethod
    def get_item_by_name(cls, name):
        return cls.items_map[name]
    
    