# -*- coding: utf-8 -*-

import json


class NodeInfo:
    def __init__(self, node_info):
        self._node_info = node_info

        self._status_map = {}
        for k, v in node_info.status.items():
            self._status_map[k] = v
            setattr(self, "status_{}".format(k), v)

        self._config_map = {}
        for k, v in node_info.config.items():
            if k not in self._config_map:
                self._config_map[k] = {}
            for k2, v2 in v.props.items():
                self._config_map[k][k2] = v2
                setattr(self, "config_{}_{}".format(k, k2), v2)

    def json(self):
        ret = {
            "status": {},
            "config": {},
        }

        for k, v in self._status_map.items():
            ret['status'][k] = v
        for k, v in self._config_map.items():
            ret['config'][k] = v

        return ret

    def __str__(self):
        return json.dumps(self.json(), indent=2)