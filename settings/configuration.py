from configobj import ConfigObj


class Configuration:

    def __init__(self):
        self.__properties = dict()
        properties = self._init_properties()
        for property_, value, transform_fn in properties:
            if transform_fn is not None:
                value = transform_fn(value)
            setattr(self, property_, value)
            self.__properties[property_] = {
                'default-value': value,
                'transform_fn': transform_fn
            }

    def _init_properties(self):
        # [[name, default-value, transform_fn]]
        return []

    # TODO: hierachical config
    def load(self, path):
        config = ConfigObj(path, encoding='UTF-8')
        for property_, value in config.items():
            transform_fn = self.__properties[property_]['transform_fn']
            if transform_fn is not None:
                value = transform_fn(value)
            setattr(self, property_, value)
