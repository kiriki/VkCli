import importlib


def get_params(local_vars):
    params = {}

    for key, value in local_vars.items():
        if value is not None and \
                key not in ('cls', 'self'):
            params[key.strip('_')] = value

    return params


def get_model_class(cls_str):
    """
    Helper for VKApiX methods. Get class from its name
    :param cls_str:
    :return:
    """
    models_package = '.models'

    cls_name = cls_str.rpartition('.')[-1]
    mod_name = cls_str.rpartition('.')[0]

    parent_package = __package__.partition('.')[0]  # vk_cli

    module = importlib.import_module(mod_name or models_package, package=parent_package)

    return getattr(module, cls_name)
