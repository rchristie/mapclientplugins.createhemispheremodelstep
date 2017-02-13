#!/usr/bin/python
"""

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import math
from opencmiss.zinc.context import Context as ZincContext
from opencmiss.zinc.status import OK as ZINC_OK
from opencmiss.zinc.element import Element, Elementbasis
from opencmiss.zinc.field import Field
from opencmiss.zinc.logger import Loggernotifier
from opencmiss.zinc.node import Node

def loggerCallback(loggerEvent):
    print(loggerEvent.getMessageText())

def writehemispheremodel(filenameOut, config):
    """
    :param filenameOut:
    :param config:
    :return: None
    """
    nElementsAround = config['elements around']
    nElementsUp = config['elements up']
    nElementsExtra = config['elements along stem']
    #radius = config['radius']
    #stemLength = config['stem length']

    context = ZincContext('hemisphere')
    logger = context.getLogger()

    ln = logger.createLoggernotifier()
    ln.setCallback(loggerCallback)

    region = context.getDefaultRegion()
    fm = region.getFieldmodule()

    coordinates = fm.createFieldFiniteElement(3)
    coordinates.setName('coordinates')
    coordinates.setManaged(True)
    coordinates.setTypeCoordinate(True)
    coordinates.setCoordinateSystemType(Field.COORDINATE_SYSTEM_TYPE_RECTANGULAR_CARTESIAN)
    coordinates.setComponentName(1, 'x')
    coordinates.setComponentName(2, 'y')
    coordinates.setComponentName(3, 'z')

    nodes = fm.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
    nodetemplate = nodes.createNodetemplate()
    nodetemplate.defineField(coordinates)
    nodetemplate.setValueNumberOfVersions(coordinates, -1, Node.VALUE_LABEL_VALUE, 1)
    nodetemplate.setValueNumberOfVersions(coordinates, -1, Node.VALUE_LABEL_D_DS1, 1)
    nodetemplate.setValueNumberOfVersions(coordinates, -1, Node.VALUE_LABEL_D_DS2, 1)
    nodetemplate.setValueNumberOfVersions(coordinates, -1, Node.VALUE_LABEL_D2_DS1DS2, 1)

    mesh = fm.findMeshByDimension(2)
    elementtemplate = mesh.createElementtemplate()
    elementtemplate.setElementShapeType(Element.SHAPE_TYPE_SQUARE)
    elementtemplate.setNumberOfNodes(4)
    nodeIndexes = [1, 2, 3, 4]
    bicubicHermiteBasis = fm.createElementbasis(2, Elementbasis.FUNCTION_TYPE_CUBIC_HERMITE)
    elementtemplate.defineFieldSimpleNodal(coordinates, -1, bicubicHermiteBasis, nodeIndexes)

    cache = fm.createFieldcache()
    allComponents = -1
    version = 1

    # create nodes
    nodeIdentifier = 1
    radiansPerElementAround = 2.0 * math.pi / nElementsAround
    d2x_ds1ds2 = [0.0, 0.0, 0.0]

    # first row
    nNodesFirstRow = nElementsAround // 2 - 1
    nNodesFirstRow_2 = nNodesFirstRow // 2
    radiansPerElementUp = math.pi / 2.0 / nElementsUp
    firstRowFraction = 0.75
    radiansPerFirstRowNode = 4.0 * firstRowFraction * radiansPerElementUp / nElementsAround
    radiansPerFirstRowNodeScaled = radiansPerFirstRowNode * (1.0 + nNodesFirstRow) / nNodesFirstRow / firstRowFraction
    for na in range(nNodesFirstRow):
        f1 = math.fabs(na - nNodesFirstRow_2) / nNodesFirstRow_2
        f2 = 1.0 - f1
        radiansX = (na - nNodesFirstRow_2) * radiansPerFirstRowNode
        sinRadiansX = math.sin(radiansX)
        cosRadiansX = math.cos(radiansX)
        x = [sinRadiansX, 0.0, -cosRadiansX]
        dx_ds1 = [radiansPerFirstRowNode*cosRadiansX, 0.0, radiansPerFirstRowNode*sinRadiansX]
        dx_ds2 = [0.0, -(f1 * radiansPerFirstRowNodeScaled + f2 * radiansPerElementUp), 0.0]
        node = nodes.createNode(nodeIdentifier, nodetemplate)
        nodeIdentifier = nodeIdentifier + 1
        cache.setNode(node)
        coordinates.setNodeParameters(cache, allComponents, Node.VALUE_LABEL_VALUE, version, x)
        coordinates.setNodeParameters(cache, allComponents, Node.VALUE_LABEL_D_DS1, version, dx_ds1)
        coordinates.setNodeParameters(cache, allComponents, Node.VALUE_LABEL_D_DS2, version, dx_ds2)
        coordinates.setNodeParameters(cache, allComponents, Node.VALUE_LABEL_D2_DS1DS2, version, d2x_ds1ds2)

    # remaining rows on hemisphere
    for nu in range(nElementsUp):
        radiansUp = (nu + 1) * radiansPerElementUp
        cosRadiansUp = math.cos(radiansUp)
        sinRadiansUp = math.sin(radiansUp)
        for na in range(nElementsAround):
            radiansAround = na * radiansPerElementAround
            cosRadiansAround = math.cos(radiansAround)
            sinRadiansAround = math.sin(radiansAround)
            x = [-cosRadiansAround * sinRadiansUp, -sinRadiansAround * sinRadiansUp, -cosRadiansUp]
            dx_ds1 = [sinRadiansAround * sinRadiansUp * radiansPerElementAround, \
                      -cosRadiansAround * sinRadiansUp * radiansPerElementAround,
                      0.0]
            dx_ds2 = [-cosRadiansAround * cosRadiansUp * radiansPerElementUp, \
                      -sinRadiansAround * cosRadiansUp * radiansPerElementUp, \
                      sinRadiansUp * radiansPerElementUp]
            node = nodes.createNode(nodeIdentifier, nodetemplate)
            nodeIdentifier = nodeIdentifier + 1
            cache.setNode(node)
            coordinates.setNodeParameters(cache, allComponents, Node.VALUE_LABEL_VALUE, version, x)
            coordinates.setNodeParameters(cache, allComponents, Node.VALUE_LABEL_D_DS1, version, dx_ds1)
            coordinates.setNodeParameters(cache, allComponents, Node.VALUE_LABEL_D_DS2, version, dx_ds2)
            coordinates.setNodeParameters(cache, allComponents, Node.VALUE_LABEL_D2_DS1DS2, version, d2x_ds1ds2)

    # remaining extra rows on the straight
    for ne in range(nElementsExtra):
        for na in range(nElementsAround):
            radiansAround = na * radiansPerElementAround
            cosRadiansAround = math.cos(radiansAround)
            sinRadiansAround = math.sin(radiansAround)
            x = [-cosRadiansAround, -sinRadiansAround, (ne + 1) * radiansPerElementUp]
            dx_ds1 = [sinRadiansAround * radiansPerElementAround, -cosRadiansAround * radiansPerElementAround, 0.0]
            dx_ds2 = [0.0, 0.0, radiansPerElementUp]
            node = nodes.createNode(nodeIdentifier, nodetemplate)
            nodeIdentifier += 1
            cache.setNode(node)
            coordinates.setNodeParameters(cache, allComponents, Node.VALUE_LABEL_VALUE, version, x)
            coordinates.setNodeParameters(cache, allComponents, Node.VALUE_LABEL_D_DS1, version, dx_ds1)
            coordinates.setNodeParameters(cache, allComponents, Node.VALUE_LABEL_D_DS2, version, dx_ds2)
            coordinates.setNodeParameters(cache, allComponents, Node.VALUE_LABEL_D2_DS1DS2, version, d2x_ds1ds2)

    # create elements
    elementIdentifier = 1

    # first row
    elementtemplate.setNode(1, nodes.findNodeByIdentifier(1))
    elementtemplate.setNode(2, nodes.findNodeByIdentifier(1))
    elementtemplate.setNode(3, nodes.findNodeByIdentifier(nNodesFirstRow + 1))
    elementtemplate.setNode(4, nodes.findNodeByIdentifier(nNodesFirstRow + 2))
    mesh.defineElement(elementIdentifier, elementtemplate)
    elementIdentifier += 1
    for ea in range(1, nNodesFirstRow):
        elementtemplate.setNode(1, nodes.findNodeByIdentifier(ea))
        elementtemplate.setNode(2, nodes.findNodeByIdentifier(ea + 1))
        elementtemplate.setNode(3, nodes.findNodeByIdentifier(nNodesFirstRow + ea + 1))
        elementtemplate.setNode(4, nodes.findNodeByIdentifier(nNodesFirstRow + ea + 2))
        mesh.defineElement(elementIdentifier, elementtemplate)
        elementIdentifier += 1
    elementtemplate.setNode(1, nodes.findNodeByIdentifier(nNodesFirstRow))
    elementtemplate.setNode(2, nodes.findNodeByIdentifier(nNodesFirstRow))
    elementtemplate.setNode(3, nodes.findNodeByIdentifier(nNodesFirstRow + nNodesFirstRow + 1))
    elementtemplate.setNode(4, nodes.findNodeByIdentifier(nNodesFirstRow + nNodesFirstRow + 2))
    mesh.defineElement(elementIdentifier, elementtemplate)
    elementIdentifier += 1
    elementtemplate.setNode(1, nodes.findNodeByIdentifier(nNodesFirstRow))
    elementtemplate.setNode(2, nodes.findNodeByIdentifier(nNodesFirstRow))
    elementtemplate.setNode(3, nodes.findNodeByIdentifier(nNodesFirstRow + nNodesFirstRow + 2))
    elementtemplate.setNode(4, nodes.findNodeByIdentifier(nNodesFirstRow + nNodesFirstRow + 3))
    mesh.defineElement(elementIdentifier, elementtemplate)
    elementIdentifier += 1
    for ea in range(1, nNodesFirstRow):
        elementtemplate.setNode(1, nodes.findNodeByIdentifier(nNodesFirstRow - ea + 1))
        elementtemplate.setNode(2, nodes.findNodeByIdentifier(nNodesFirstRow - ea))
        elementtemplate.setNode(3, nodes.findNodeByIdentifier(nNodesFirstRow*2 + ea + 2))
        elementtemplate.setNode(4, nodes.findNodeByIdentifier(nNodesFirstRow*2 + ea + 3))
        mesh.defineElement(elementIdentifier, elementtemplate)
        elementIdentifier += 1
    elementtemplate.setNode(1, nodes.findNodeByIdentifier(1))
    elementtemplate.setNode(2, nodes.findNodeByIdentifier(1))
    elementtemplate.setNode(3, nodes.findNodeByIdentifier(nNodesFirstRow + nElementsAround))
    elementtemplate.setNode(4, nodes.findNodeByIdentifier(nNodesFirstRow + 1))
    mesh.defineElement(elementIdentifier, elementtemplate)
    elementIdentifier += 1


    # remaining regular rows
    nElementsRegular = nElementsUp - 1 + nElementsExtra
    for er in range(nElementsRegular):
        baseNodeIdentifier = 1 + nNodesFirstRow + er*nElementsAround
        for ea in range(nElementsAround):
            ea2 = (ea + 1) % nElementsAround
            elementtemplate.setNode(1, nodes.findNodeByIdentifier(baseNodeIdentifier + ea))
            elementtemplate.setNode(2, nodes.findNodeByIdentifier(baseNodeIdentifier + ea2))
            elementtemplate.setNode(3, nodes.findNodeByIdentifier(baseNodeIdentifier + nElementsAround + ea))
            elementtemplate.setNode(4, nodes.findNodeByIdentifier(baseNodeIdentifier + nElementsAround + ea2))
            mesh.defineElement(elementIdentifier, elementtemplate)
            elementIdentifier += 1

    fm.defineAllFaces()

    sir = region.createStreaminformationRegion()
    srm = sir.createStreamresourceMemory()
    result = region.write(sir)
    print("region.write: " + str(result))
    result, buffer = srm.getBuffer()
    print("srm.getBuffer: " + str(result))

    elements2dLoc = buffer.find(" Shape. Dimension=2")

    outfile = open(filenameOut, 'w')
    headerLoc = buffer.find(" #Scale factor sets", elements2dLoc)
    outfile.write(buffer[0:headerLoc])
    elementLoc = buffer.find(" Element:",headerLoc)
    headerNormal = buffer[headerLoc:elementLoc]

    headerReverse = headerNormal.replace(" #Scale factor sets=0\n", \
        " #Scale factor sets=1\n   c.Hermite*c.Hermite, #Scale factors=1\n")

    headerReverse = headerReverse.replace("""
   #Nodes=4
   1. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   2. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   3. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   4. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0""","""
   #Nodes=4
   1. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 1 1 0
   2. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 1 1 0
   3. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   4. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0""")

    header1 = headerNormal.replace(" #Scale factor sets=0\n", \
        " #Scale factor sets=1\n   c.Hermite*c.Hermite, #Scale factors=1\n")

    header1 = header1.replace("""
   #Nodes=4
   1. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   2. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   3. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   4. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0""","""
   #Nodes=4
   1. #Values=4
     Value labels: value zero d/ds1 zero
     Scale factor indices: 0 0 1 0
   2. #Values=4
     Value labels: value zero d/ds2 zero
     Scale factor indices: 0 0 0 0
   3. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   4. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0""")

    header2 = headerNormal.replace(" #Scale factor sets=0\n", \
        " #Scale factor sets=1\n   c.Hermite*c.Hermite, #Scale factors=1\n")

    header2 = header2.replace("""
   #Nodes=4
   1. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   2. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   3. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   4. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0""","""
   #Nodes=4
   1. #Values=4
     Value labels: value zero d/ds2 zero
     Scale factor indices: 0 0 0 0
   2. #Values=4
     Value labels: value zero d/ds1 zero
     Scale factor indices: 0 0 0 0
   3. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   4. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0""")

    header3 = headerNormal.replace(" #Scale factor sets=0\n", \
        " #Scale factor sets=1\n   c.Hermite*c.Hermite, #Scale factors=1\n")

    header3 = header3.replace("""
   #Nodes=4
   1. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   2. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   3. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   4. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0""","""
   #Nodes=4
   1. #Values=4
     Value labels: value zero d/ds1 zero
     Scale factor indices: 0 0 0 0
   2. #Values=4
     Value labels: value zero d/ds2 zero
     Scale factor indices: 0 0 1 0
   3. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   4. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0""")

    header4 = headerNormal.replace(" #Scale factor sets=0\n", \
        " #Scale factor sets=1\n   c.Hermite*c.Hermite, #Scale factors=1\n")

    header4 = header4.replace("""
   #Nodes=4
   1. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   2. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   3. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   4. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0""","""
   #Nodes=4
   1. #Values=4
     Value labels: value zero d/ds2 zero
     Scale factor indices: 0 0 1 0
   2. #Values=4
     Value labels: value zero d/ds1 zero
     Scale factor indices: 0 0 1 0
   3. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0
   4. #Values=4
     Value labels: value d/ds1 d/ds2 d2/ds1ds2
     Scale factor indices: 0 0 0 0""")

    outfile.write(header1)
    elementLoc2 = buffer.find(" Element:", elementLoc + 1)
    outfile.write(buffer[elementLoc:elementLoc2])
    outfile.write("Scale factors:\n-1\n")
    elementLoc = elementLoc2

    outfile.write(headerNormal)
    for i in range(nElementsAround // 2 - 2):
        elementLoc2 = buffer.find(" Element:", elementLoc + 1)
        outfile.write(buffer[elementLoc:elementLoc2])
        elementLoc = elementLoc2

    outfile.write(header2)
    elementLoc2 = buffer.find(" Element:", elementLoc + 1)
    outfile.write(buffer[elementLoc:elementLoc2])
    outfile.write("Scale factors:\n-1\n")
    elementLoc = elementLoc2

    outfile.write(header3)
    elementLoc2 = buffer.find(" Element:", elementLoc + 1)
    outfile.write(buffer[elementLoc:elementLoc2])
    outfile.write("Scale factors:\n-1\n")
    elementLoc = elementLoc2

    outfile.write(headerReverse)
    for i in range(nElementsAround // 2 - 2):
        elementLoc2 = buffer.find(" Element:", elementLoc + 1)
        outfile.write(buffer[elementLoc:elementLoc2])
        outfile.write("Scale factors:\n-1\n")
        elementLoc = elementLoc2

    outfile.write(header4)
    elementLoc2 = buffer.find(" Element:", elementLoc + 1)
    outfile.write(buffer[elementLoc:elementLoc2])
    outfile.write("Scale factors:\n-1\n")
    elementLoc = elementLoc2

    outfile.write(headerNormal)
    outfile.write(buffer[elementLoc:])
    outfile.close()
