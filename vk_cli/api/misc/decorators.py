import logging

log = logging.getLogger(__name__)  # 'vk_tools.api.vkrequest'


def unimplemented(fn):
    def new(*args):
        print('Sorry! This method is not implemented yet.')
        raise NotImplementedError
        # return fn(*args)

    return new


def timer(f):
    import time

    def tmp(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        log.info(f'done in {time.time() - t:f} sec')
        return res

    return tmp
