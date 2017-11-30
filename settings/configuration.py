from configobj import ConfigObj


class Configuration:

    def __init__(self):
        self.__properties = dict()
        properties = self._init_properties()
        for property_, value, type_ in properties:
            setattr(self, property_, value)
            self.__properties[property_] = {
                'default-value': value,
                'type': type_
            }

    def _init_properties(self):
        # [[name, default-value, transform_fn]]
        return []

    # TODO: hierachical config
    def load(self, path):
        config = ConfigObj(path, encoding='UTF-8')
        for property_, value in config.items():
            transform_fn = self.__properties[property_]['type']
            if transform_fn is not None:
                setattr(self, property_, transform_fn(value))
            else:
                setattr(self, property_, value)
