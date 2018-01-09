import os

import maya.cmds as cmds
from mtoa import core, aovs


def get_scene_aovs():
    """
    Get the aov existing in the maya scene

    :return: list of the scene aovs
    """

    scene_aovs = cmds.ls(type="aiAOV") or None
    
    if scene_aovs is None:
        return []

    scene_aovs = [aov.split("aiAOV_")[-1] for aov in scene_aovs]

    return scene_aovs


def get_grouped_aovs():
    """
    Get the available mtoa aovs grouped under their catergories setup for mtoa

    :return: a dictionary where keys are aov category and values a list of aovs
    """

    aov_groups = sorted(set(aovs.getNodeTypesWithAOVs()))

    aovs_dict = dict()

    for aovGrp in aov_groups:
        group_list = []

        aov_list = [x for x in aovs.getRegisteredAOVs(nodeType=aovGrp) if x]

        for aov in aov_list:
            aov_data = {"ui_Name": aov,
                        "aov_Name": "aiAOV_%s" % aov,
                        "type": aovGrp}

            group_list.append(aov_data)

        aovs_dict[aovGrp] = group_list

    return aovs_dict


def get_layers_aovs():
    """
    Get the aovs enabled for each render layer

    :return: a dictionary where keys are render layers and values the
             render layer enabled aovs
    """

    aov_dict = dict()
    render_layers = [x for x in cmds.ls(type="renderLayer")
                     if "defaultRenderLayer" not in x]

    scn_aovs = cmds.ls(type="aiAOV")

    for render_layer in render_layers:
        aov_dict[render_layer] = ["beauty"]

        for aov in scn_aovs:
            attr = "enabled"
            layer_overrides = cmds.listConnections("%s.%s" % (aov, attr),
                                                   plugs=1)

            # Use attribute value if attribute has no overrides on any layer
            value = cmds.getAttr("%s.%s" % (aov, attr))

            if layer_overrides:
                attribute_plug = False

                # Use default Render Layer Value if attribute
                #  is not overriden for a layer

                for layerOver in layer_overrides:
                    if "defaultRenderLayer" == layerOver.split(".")[0]:
                        attribute_plug = layerOver

                # Query attr Layer Override value
                for layerOver in layer_overrides:
                    if render_layer == layerOver.split(".")[0]:
                        attribute_plug = layerOver

                if not attribute_plug:
                    continue

                values = [False, True]

                value = values[int(cmds.getAttr(attribute_plug
                                                .replace("plug", "value")))]

            if value is True:
                aov_dict[render_layer].append(aov.split("aiAOV_")[-1])

    return aov_dict


def create_new_aov(aov_name, data_type="rgb"):
    """
    Create a new aov

    :param aov_name: the aov name to create as a string
    :param data_type: the data type for the aov to create as a string
    :return: the ai aov name for the created aov as a string
    """

    scene_aovs = [x for x in cmds.ls(type="aiAOV")]

    ai_aov_name = "aiAOV_%s" % aov_name

    if ai_aov_name in scene_aovs:
        print "%s already exists in the scene" % aov_name
        return False

    new_aov = aovs.AOVInterface()
    new_aov.addAOV(aov_name, data_type)

    # Set AOV disabled
    cmds.setAttr("%s.enabled" % ai_aov_name, 0)

    return ai_aov_name


def create_connect_aov_shader(aov_name, attribute_id=False):
    """
    Create an aov and connect a shader to it

    :param aov_name: the name of an aov object as a string
    :param attribute_id: bool used to create or not the id attribute
    :return: the name of the created surface shader as a string
    """

    surface_shader = cmds.shadingNode("surfaceShader",
                                      name="AOV_%s_MAT" % aov_name,
                                      asShader=True)

    # Create a Shading Group so Miasma will publish this shader
    shading_group = cmds.createNode("shadingEngine",
                                    name="AOV_%s_SG" % aov_name)

    cmds.connectAttr("%s.outColor" % surface_shader,
                     "%s.surfaceShader" % shading_group)

    rgb_data = cmds.shadingNode("aiUserDataColor",
                                asShader=True,
                                name="userData_%s" % aov_name)

    cmds.setAttr("%s.colorAttrName" % rgb_data,
                 aov_name,
                 type="string")

    cmds.connectAttr("%s.outColor" % rgb_data,
                     "%s.outColor" % surface_shader,
                     force=True)

    cmds.connectAttr("%s.outColor" % surface_shader,
                     "aiAOV_%s.defaultValue" % aov_name,
                     force=True)

    # Add the attr_id to be identified as an attr id aov type
    if attribute_id:
        cmds.addAttr('aiAOV_%s' % aov_name,
                     ln='attr_id',
                     at='bool',
                     hidden=True)

    return surface_shader


def add_aov_to_render_layer(ui_name,
                            node_name,
                            render_layer,
                            aov_type,
                            data_type="rgb"):

    """
    Enabled an aov on a render layer. Created first if it doesn't exist.

    :param ui_name:
    :param node_name:
    :param render_layer:
    :param aov_type:
    :param data_type:
    :return:
    """

    # Create AOV if it doesn't exist
    new_aov = create_new_aov(ui_name, data_type=data_type)
    aov_shader = "AOV_%s_MAT" % ui_name

    if new_aov and aov_type != "<builtin>":
        # Bring shader to the scene
        if aov_type == "<attrId>":
            create_connect_aov_shader(ui_name, attribute_id=True)

        elif aov_type != "<builtin>":
            if not cmds.objExists(aov_shader):
                import_aov_preset_shader(ui_name)

            # Add Default shader to Aov
            if cmds.objExists(aov_shader):
                cmds.connectAttr("%s.outColor" % aov_shader,
                                 "aiAOV_%s.defaultValue" % ui_name,
                                 force=True)

    # Set AOV layer overrides
    if render_layer != "masterLayer":
        set_layer_overrides("%s.enabled" % node_name, {render_layer: True})

    return


def get_master_layer_value(aov_name):
    """
    Get the aov enabled state of an aov on the master render layer

    :param aov_name: the aov name as a string
    :return: the enabled value as a bool
    """

    current_layer = cmds.editRenderLayerGlobals(currentRenderLayer=True,
                                                query=True)

    # If we are in the master layer return the current value
    if current_layer == "defaultRenderLayer":
        return cmds.getAttr("%s.enabled" % aov_name)

    # If we are not in the master layer check if the layer has an override
    layer_overrides = cmds.listConnections('%s.enabled' % aov_name) or []

    # If there is not an override for this layer return the curr value
    if current_layer not in layer_overrides:
        return cmds.getAttr("%s.enabled" % aov_name)

    # If the layer has  an override
    # Query the override value
    layer_value = cmds.getAttr("%s.enabled" % aov_name)

    # Remove the override
    cmds.editRenderLayerAdjustment("%s.enabled" % aov_name,
                                   layer=current_layer,
                                   remove=True)

    # Get the master value
    master_value = cmds.getAttr("%s.enabled" % aov_name)

    # Reinstate the override
    cmds.editRenderLayerAdjustment("%s.enabled" % aov_name,
                                   layer=current_layer)

    # Set the override value
    cmds.setAttr("%s.enabled" % aov_name, layer_value)

    return master_value


def get_render_layer_accepted_objects():
    """
    Get a list of render accepted objects

    :return: a list of the object types accepted as render objects
    """

    accepted_objects = ["mesh",
                        "xgmDescription",
                        "pgYetiMaya",
                        "aiStandIn",
                        "pgYetiGroom",
                        "aiVolume"]

    return accepted_objects


def get_object_primary_visibility(node):
    """

    :param node: the name of a transform node as a string
    :return: a bool for the node primary visibility value
    """

    override = "primaryVisibility"

    if cmds.nodeType(node) == "mesh":
        shape_node = node
    else:
        shape_node = get_object_shape_node(node)

    if shape_node is False:
        return False

    if not cmds.attributeQuery(override, node=shape_node, exists=True):
        return False

    if cmds.getAttr("%s.%s" % (shape_node, override)) is False:
        return False

    object_sets = cmds.listSets(object=node) or False

    if not object_sets:
        return True

    for object_set in object_sets:
        if not cmds.attributeQuery(override, node=object_set, exists=True):
            continue

        if cmds.getAttr("%s.%s" % (object_set, override)) is False:
            return False

    return True


def get_object_shape_node(node):
    """
    Get the shape node of a transform node

    :param node: the name of a node as a string
    :return: the name of the shape node as a string
    """

    shape_nodes = cmds.listRelatives(node,
                                     allDescendents=True,
                                     fullPath=True,
                                     shapes=True) or []

    if not len(shape_nodes):
        return False

    shape_node = shape_nodes[0]

    return shape_node


def get_render_layer_objects(render_layer):
    """
    Get the transform nodes added to a render layer

    :param render_layer: the name a render layer as a string
    :return: a list of the render layers transform nodes
    """

    layer_objects = list(set(cmds.editRenderLayerMembers(render_layer,
                                                         q=True,
                                                         fullNames=True)
                         or [])) or None

    if layer_objects is None:
        return False

    layer_transform_nodes = []

    for node in layer_objects:
        if cmds.nodeType(node) != "transform":
            transform_node = cmds.listRelatives(node,
                                                parent=True,
                                                fullPath=True)

            transform_is_valid = (transform_node[0]
                                  not in layer_transform_nodes)

            if transform_node and transform_is_valid:
                layer_transform_nodes.append(transform_node[0])
        else:
            if node not in layer_transform_nodes:
                layer_transform_nodes.append(node)

    return layer_transform_nodes


def set_layer_overrides(node_attribute, override_data):
    """
    Set layer values overrides for a node attribute from the given per layer
    override data

    :param node_attribute: a node's attribute name as a string
    :param override_data: dictionary data where keys are render layer
    and values the layer's override value
    :return:
    """

    current_layer = cmds.editRenderLayerGlobals(query=True, crl=True)

    # Query the existing layerOverride Values
    layer_values = gather_attribute_override_data(node_attribute) or {}

    # Remove all layer overrides
    for render_layer in layer_values.keys():
        cmds.editRenderLayerAdjustment(node_attribute,
                                       layer=render_layer,
                                       remove=True)

    # Merge user layer Override and pre-existing override values
    for render_layer, value in override_data.iteritems():
        layer_values[render_layer] = value

    # Query the master layer value
    master_value = cmds.getAttr(node_attribute)

    render_layers = [x for x in cmds.ls(type='renderLayer')
                     if x != 'defaultRenderLayer']

    # Set override value per layer
    for render_layer in render_layers:
        if render_layer == current_layer:
            continue

        value = layer_values.get(render_layer, False)

        cmds.setAttr(node_attribute, value)
        cmds.editRenderLayerAdjustment(node_attribute,
                                       layer=render_layer)

    cmds.setAttr(node_attribute, master_value)

    current_layer_valid = current_layer in layer_values.keys()

    if "defaultRenderLayer" not in current_layer and current_layer_valid:
        cmds.editRenderLayerAdjustment(node_attribute, layer=current_layer)
        cmds.setAttr(node_attribute, layer_values[current_layer])

    return


def gather_attribute_override_data(node_attribute):
    """

    :param node_attribute: attribute name as a string
    :return: dictionary where keys are render layers and value is the attribute
    override state for the render layer
    """

    override_data = dict()

    layer_overrides = cmds.listConnections(node_attribute,
                                           plugs=1,
                                           type="renderLayer")

    if layer_overrides is None:
        return False

    render_layers = [x for x in cmds.ls(type='renderLayer')
                     if x != 'defaultRenderLayer']

    for layerOver in layer_overrides:
        render_layer = layerOver.split(".")[0]

        if render_layer not in render_layers:
            continue

        attribute_plug = layerOver
        value = (cmds.getAttr(attribute_plug.replace("plug", "value")))

        override_data[render_layer] = value

    return override_data


def import_aov_preset_shader(aov_name):
    """
    Import the shader preset for a given aov name

    :param aov_name: the aov name as a string
    :return: the imported nodes
    """

    import_folder = os.path.dirname(os.path.abspath(__file__))
    import_file = os.path.join(import_folder,
                               "shaders", "AOV_%s.mb" % aov_name)

    if not os.path.exists(import_file):
        return False

    import_nodes = cmds.file(import_file,
                             force=True,
                             options="v=0",
                             typ="mayaBinary",
                             pr=True,
                             i=True,
                             gr=True,
                             dns=True,
                             rnn=True)

    return import_nodes


def create_arnold_options():
    """
    Create the arnold render options

    :return:
    """

    core.createOptions()

    return
