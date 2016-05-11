import copy
import yaml
import json


def load_yaml(yaml_file_path):
    """Loads a YAML file"""
    with open(yaml_file_path, 'r') as f:
        data = yaml.load(f)

    return data


def load_blueprint(blueprint_file_path):
    """Loads a TOSCA YAML blueprint"""
    return load_yaml(blueprint_file_path)


def load_options(options_file_path):
    """Loads a Configuration optimization YAML file"""
    in_opts = load_yaml(options_file_path)
    vars = {int(k[3:]): v for k, v in in_opts.items() if k.startswith('var')}
    options = []
    for i in range(1, len(vars) + 1):
        options.append({
            'paramname': vars[i]['paramname'],
            'node': vars[i]['node'],
        })
    return options


def load_configuration_matlab(configuration_file_path):
    """
    Loads a matlab text dump of the configuration numerical values
    and stores them in a Python array.
    """
    config = [ ]
    with open(configuration_file_path, 'r') as f:
        for line in f.readlines():
            v = float(line)
            if v.is_integer():
                v = int(v)
            config += [ v ]

    return config


def load_configuration_json(configuration_file_path):
    """
    Loads a json representation of the configuration and stores it in 
    a Python array.
    """
    with open(configuration_file_path, 'r') as f:
        data = json.load(f)

    return data['config']


def set_configuration_value(node, paramname, value):
    props = node.get('properties', {})
    conf = props.get('configuration', {})
    conf[paramname] = value
    props['configuration'] = conf
    node['properties'] = props


def update_blueprint(input_blueprint, options, config):
    """
    Updates the input TOSCA blueprint with the new configuration values and
    produces an updated TOSCA blueprint.

    `input_blueprint`: the blueprint to update
    `options`: a dictionary with the Configuration Optimization options
    `config`: the configuration values to be updated.
    """
    import types

    updated_blueprint = copy.deepcopy(input_blueprint)

    assert(len(options) == len(config))

    for option, value in zip(options, config):
        paramname = option['paramname']
        nodes = option['node']
        nodes = [nodes] if isinstance(nodes, basestring) else nodes
        for node in nodes:
            node_template = updated_blueprint['node_templates'][node]
            set_configuration_value(node_template, paramname, value)

    return updated_blueprint