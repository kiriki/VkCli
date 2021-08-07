def get_params(local_vars):
    params = {}

    for key, value in local_vars.items():
        if value is not None and \
                key not in ('cls', 'self'):
            params[key.strip('_')] = value

    return params


def get_class(kls):
    """
    Helper for VKApiX methods. Get class from its name
    :param kls:
    :return:
    """
    parts = kls.split('.')
    module = '.'.join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m
