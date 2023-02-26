import sys
import importlib
import maya.cmds as cmds
import bsControlsData as bsCon
import re

from maya import OpenMayaUI as omui
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

importlib.reload(bsCon)

bsData = bsCon.BSControlsData()

def maya_main_window():
    '''
    Return the Maya main window widget as a Python object
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()

    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class AutoRigOLolo(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(AutoRigOLolo, self).__init__(parent)
        self.qtSignal = QtCore.Signal()
        #################################################################

        self.setWindowTitle('Auto Rig-o-Lolo v0.1')
        self.setWindowFlags(QtCore.Qt.Tool)
        self.resize(300, 150)  # re-size the window

        self.dark = QtGui.QColor(45, 45, 45)
        self.bg = QtGui.QColor(75, 75, 75)
        self.light = QtGui.QColor(100, 100, 100)
        self.light2 = QtGui.QColor(125, 125, 130)

        self.menubar = QtWidgets.QMenuBar()
        self.editMenu = QtWidgets.QMenu('Edit')
        self.helpMenu = QtWidgets.QMenu('Help')
        self.menubar.addMenu(self.editMenu)
        self.menubar.addMenu(self.helpMenu)
        button_action = QtWidgets.QAction('Blendshape Connect', self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.openBsConnect)
        self.editMenu.addAction(button_action)

        self.typejointLabel = QtWidgets.QLabel("Search for :")
        self.typejoint = self.createQline('sk')
        self.typectrlLabel = QtWidgets.QLabel("Replace by :")
        self.typectrl = self.createQline('ctrl')

        ## Top1
        self.topLabel1 = QtWidgets.QLabel("Group 1 :")
        self.topGrp1 = self.createQline('inf')

        ## Top2
        self.topLabel2 = QtWidgets.QLabel("   Group 2 :")
        self.topGrp2 = self.createQline('pose')

        self.titleConst = QtWidgets.QLabel("Constraint Type :")
        self.constType = self.createCombo()
        self.constType.addItem("Orient Constraint", userData=0)
        self.constType.addItem("Parent Constraint", userData=1)
        self.constType.addItem("Point Constraint", userData=2)

        self.splitter = QtWidgets.QLabel("--------------------------------------------------------------------")
        self.splitter1 = QtWidgets.QLabel("--------------------------------------------------------------------")
        self.splitter3 = QtWidgets.QLabel("--------------------------------------------------------------------")

        self.cShape_ctrl = self.comboBoxCurves()
        self.titleCtrlBase = QtWidgets.QLabel("Base ctrl:")
        self.cShape_ctrlBase = self.comboBoxCurves()
        self.titleCtrlPoleVector = QtWidgets.QLabel("Pole ctrl:")
        self.cShape_ctrlPoleVector = self.comboBoxCurves()
        self.titleCtrlEnd = QtWidgets.QLabel("End ctrl :")
        self.cShape_ctrlEnd = self.comboBoxCurves()

        self.fkChains = QtWidgets.QCheckBox("Apply on children")

        self.createCtrl = self.createButton("Create Control")

        self.addgGroup_prefix_title = QtWidgets.QLabel("Prefix :")
        self.addgGroup_prefix = self.createQline('')
        self.addgGroup_fix_title = QtWidgets.QLabel("Fix :")
        self.addgGroup_fix = QtWidgets.QLabel('Controler Name')
        self.addgGroup_suffix_title = QtWidgets.QLabel("Suffix :")
        self.addgGroup_suffix = self.createQline('_Cup')
        self.addGrp_button = self.createButton("Add Group")
        self.createFollow_button = self.createButton("Create Follow")

        self.createIkLimb_button = self.createButton("Create Ik Limb")
        self.createSwitcher_button = self.createButton("Create Switcher")

        self.createReverseFootLoc_button = self.createButton("Create Locators")
        self.MirrorLoc_button = self.createButton("Mirror Locators")
        self.createReverseFoot_button = self.createButton("Create Reverse Foot")
        self.createSpine_button = self.createButton("Create Spine")

        self.createParentSpace_Label = QtWidgets.QLabel("Mode :")
        self.createParentSpace_Mode = self.createCombo()
        self.createParentSpace_Mode.addItem("Custom", userData=0)
        self.createParentSpace_Mode.addItem("Hand", userData=1)
        self.createParentSpace_Mode.addItem("Foot", userData=2)
        self.createParentSpace_Mode.addItem("Look at", userData=3)
        self.createParentSpace_Mode.addItem("Head", userData=4)
        self.createParentSpace_Qline = self.createQline('')
        self.createParentSpace_button = self.createButton("Create Parent Space")
        self.createOrienttSpace_button = self.createButton("Create Orient Space")

        self.replaceShape_button = self.createButton("Replace Shape")
        self.cShape_replaceCtrl = self.comboBoxCurves()

        self.createStrech_button = self.createButton("Create Stretch")
        self.createRolls_button = self.createButton("Create Rolls")
        self.createStickyRibbon_button = self.createButton("Create Sticky")

        self.titleTweaks = QtWidgets.QLabel("Tweak nbr :")
        self.nbrTweaks = QtWidgets.QSpinBox()
        self.nbrTweaks.setValue(4)
        self.nbrTweaks.setRange(0, 12)
        self.createRibbons_button = self.createButton("Create Ribbons")

        self.widgetRibbons = QtWidgets.QWidget(self)
        self.widgetRibbons_layout = QtWidgets.QVBoxLayout(self.widgetRibbons)
        self.widgetTweaks = self.twoColumn(self.titleTweaks, self.nbrTweaks)
        self.widgetRibbons_layout.addWidget(self.widgetTweaks)
        self.widgetRibbons_layout.addWidget(self.createRibbons_button)
        self.widgetRibbons.setStyleSheet("QWidget { background-color: %s }" % self.bg.name())
        self.nbrTweaks.setStyleSheet("QWidget { background-color: %s }" % self.dark.name())

        self.createLookAt_button = self.createButton("Create Look at")

        self.createUnstick_button = self.createButton("Create unstick")

        # Layout
        #
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        ## Group1
        self.widgetGrp1 = self.twoColumn(self.topLabel1, self.topGrp1)

        ## Group2
        self.widgetGrp2 = self.twoColumn(self.topLabel2, self.topGrp2)

        ## Constraint
        self.top_widget3 = QtWidgets.QWidget(self)
        self.top_widget3_layout = QtWidgets.QHBoxLayout(self.top_widget3)
        self.top_widget3_layout.addWidget(self.titleConst)
        self.top_widget3_layout.addWidget(self.constType)

        ## Create Control
        self.createCtrl_label = QtWidgets.QLabel(' Create Controller')
        self.createCtrl_label.setScaledContents(True)
        self.createCtrl_label.setAlignment(QtCore.Qt.AlignCenter)
        self.createCtrl_label.setStyleSheet("QWidget { background-color: %s }" % self.light2.name())
        self.createCtrl_label.setMargin(15)
        self.widgetCreateControl = QtWidgets.QWidget(self)
        self.widgetCreateControl_layout = QtWidgets.QVBoxLayout(self.widgetCreateControl)
        self.widgetCreateControl_layout.addWidget(self.typejointLabel)
        self.widgetCreateControl_layout.addWidget(self.typejoint)
        self.widgetCreateControl_layout.addWidget(self.typectrlLabel)
        self.widgetCreateControl_layout.addWidget(self.typectrl)
        self.widgetCreateControl_layout.addWidget(self.splitter3)

        self.widgetCreateControl_layout.addWidget(self.widgetGrp1)
        self.widgetCreateControl_layout.addWidget(self.widgetGrp2)
        self.widgetCreateControl_layout.addWidget(self.cShape_ctrl)

        self.widgetCreateControl_layout.addWidget(self.splitter1)

        self.widgetCreateControl_layout.addWidget(self.top_widget3)

        self.widgetCreateControl_layout.addWidget(self.splitter)

        self.widgetCreateControl_layout.addWidget(self.fkChains)
        self.widgetCreateControl_layout.addWidget(self.createCtrl)

        self.widgetCreateControl.setStyleSheet("QWidget { background-color: %s }" % self.bg.name())

        ## Add group

        self.addgroup_widget_column1 = QtWidgets.QWidget(self)
        self.addgroup_layout_column1 = QtWidgets.QVBoxLayout(self.addgroup_widget_column1)
        self.addgroup_layout_column1.addWidget(self.addgGroup_prefix_title)
        self.addgroup_layout_column1.addWidget(self.addgGroup_prefix)

        self.addgroup_widget_column2 = QtWidgets.QWidget(self)
        self.addgroup_layout_column2 = QtWidgets.QVBoxLayout(self.addgroup_widget_column2)
        self.addgroup_layout_column2.addWidget(self.addgGroup_fix_title)
        self.addgroup_layout_column2.addWidget(self.addgGroup_fix)

        self.addgroup_widget_column3 = QtWidgets.QWidget(self)
        self.addgroup_layout_column3 = QtWidgets.QVBoxLayout(self.addgroup_widget_column3)
        self.addgroup_layout_column3.addWidget(self.addgGroup_suffix_title)
        self.addgroup_layout_column3.addWidget(self.addgGroup_suffix)

        self.addgroup_widget = QtWidgets.QWidget(self)
        self.addgroup_layout = QtWidgets.QHBoxLayout(self.addgroup_widget)
        self.addgroup_layout.addWidget(self.addgroup_widget_column1)
        self.addgroup_layout.addWidget(self.addgroup_widget_column2)
        self.addgroup_layout.addWidget(self.addgroup_widget_column3)

        self.addgroup_widgetf = QtWidgets.QWidget(self)
        self.addgroup_widgetf_layout = QtWidgets.QVBoxLayout(self.addgroup_widgetf)
        self.addgroup_widgetf_layout.addWidget(self.addgroup_widget)
        self.addgroup_widgetf_layout.addWidget(self.addGrp_button)

        self.addgroup_widgetf.setStyleSheet("QWidget { background-color: %s }" % self.bg.name())

        # Control curveShape of the Limb tool
        self.widgetCtrlBase = self.twoColumn(self.titleCtrlBase, self.cShape_ctrlBase)
        self.widgetCtrlPoleVector = self.twoColumn(self.titleCtrlPoleVector, self.cShape_ctrlPoleVector)
        self.widgetCtrlEnd = self.twoColumn(self.titleCtrlEnd, self.cShape_ctrlEnd)

        # Create ParentSpace
        self.widgetCreateParentSpace = QtWidgets.QWidget(self)
        self.widgetCreateParentSpace.setStyleSheet("QWidget { background-color: %s }" % self.bg.name())

        self.widgetCreateParentSpace_layout = QtWidgets.QVBoxLayout(self.widgetCreateParentSpace)

        self.widgetModeSpace = QtWidgets.QWidget(self)
        widgetModeSpace_layout = QtWidgets.QHBoxLayout(self.widgetModeSpace)
        widgetModeSpace_layout.addWidget(self.createParentSpace_Label)
        widgetModeSpace_layout.addWidget(self.createParentSpace_Mode)
        self.t = QtWidgets.QLabel('                                     ')
        widgetModeSpace_layout.addWidget(self.t)
        self.widgetCreateParentSpace_layout.addWidget(self.widgetModeSpace)

        self.widgetCreateParentSpace_layout.addWidget(self.createParentSpace_Qline)

        self.createSpacebtn = self.twoColumn(self.createParentSpace_button, self.createOrienttSpace_button)
        self.widgetCreateParentSpace_layout.addWidget(self.createSpacebtn)

        # Replace Shape
        self.widgetReplaceShape = QtWidgets.QWidget(self)
        self.widgetReplaceShape.setStyleSheet("QWidget { background-color: %s }" % self.bg.name())
        self.widgetReplaceShape_layout = QtWidgets.QVBoxLayout(self.widgetReplaceShape)
        self.cShape_replaceCtrl_Label = QtWidgets.QLabel("New Shape :")
        t = self.twoColumn(self.cShape_replaceCtrl_Label,self.cShape_replaceCtrl)
        self.widgetReplaceShape_layout.addWidget(t)
        self.widgetReplaceShape_layout.addWidget(self.replaceShape_button)

        # Create IK
        self.createIk_label = QtWidgets.QLabel(' Create IK')
        self.createIk_label.setAlignment(QtCore.Qt.AlignCenter)
        self.createIk_label.setScaledContents(False)
        self.createIk_label.setAlignment(QtCore.Qt.AlignCenter)
        self.createIk_label.setStyleSheet(
            f"background-color: {self.light2.name()};"
            f"text-align: right")
        self.createIk_label.setFixedSize(QtCore.QSize(250, 50))
        self.widgetCreateIk = QtWidgets.QWidget(self)
        self.widgetCreateIk_layout = QtWidgets.QVBoxLayout(self.widgetCreateIk)
        self.widgetCreateIk_layout.addWidget(self.widgetCtrlBase)
        self.widgetCreateIk_layout.addWidget(self.widgetCtrlPoleVector)
        self.widgetCreateIk_layout.addWidget(self.widgetCtrlEnd)
        self.widgetCreateIk_layout.addWidget(self.createIkLimb_button)
        self.widgetCreateIk_layout.addWidget(self.createSwitcher_button)

        self.widgetCreateIk.setStyleSheet("QWidget { background-color: %s }" % self.bg.name())

        # Create Reverse Foot
        self.reverseFoot_label = QtWidgets.QLabel(' Reverse Foot')
        self.reverseFoot_label.setAlignment(QtCore.Qt.AlignCenter)
        self.reverseFoot_label.setScaledContents(False)
        self.reverseFoot_label.setStyleSheet("QWidget { background-color: %s }" % self.light2.name())
        self.reverseFoot_label.setMargin(15)

        self.widgetCreateRF = QtWidgets.QWidget(self)
        self.widgetCreateRF_layout = QtWidgets.QVBoxLayout(self.widgetCreateRF)

        self.widgetLocCreateMirror = self.twoColumn(self.createReverseFootLoc_button, self.MirrorLoc_button)
        self.widgetCreateRF_layout.addWidget(self.widgetLocCreateMirror)
        self.widgetCreateRF_layout.addWidget(self.createReverseFoot_button)
        self.widgetCreateRF.setStyleSheet("QWidget { background-color: %s }" % self.bg.name())

        # Add to column 1 Layout
        #
        self.column1 = QtWidgets.QWidget(self)
        self.column1_layout = QtWidgets.QVBoxLayout(self.column1)

        self.column1_layout.addWidget(self.createCtrl_label)
        self.column1_layout.addWidget(self.widgetCreateControl)

        self.additions_label = QtWidgets.QLabel(' Additions')
        self.additions_label.setAlignment(QtCore.Qt.AlignCenter)
        self.additions_label.setScaledContents(False)
        self.additions_label.setStyleSheet("QWidget { background-color: %s }" % self.light2.name())
        self.additions_label.setMargin(15)
        self.column1_layout.addWidget(self.additions_label)
        self.column1_layout.addWidget(self.createLookAt_button)
        self.column1_layout.addWidget(self.createUnstick_button)
        self.column1_layout.addWidget(self.createFollow_button)
        self.column1_layout.addWidget(self.addgroup_widgetf)
        self.column1_layout.addWidget(self.widgetCreateParentSpace)
        self.column1_layout.addWidget(self.widgetReplaceShape)

        # Add to column 2 Layout
        #
        self.column2 = QtWidgets.QWidget(self)
        self.column2_layout = QtWidgets.QVBoxLayout(self.column2)
        self.column2_layout.addWidget(self.createIk_label)
        self.column2_layout.addWidget(self.widgetCreateIk)
        self.column2_layout.addWidget(self.reverseFoot_label)
        self.column2_layout.addWidget(self.widgetCreateRF)

        self.column2_layout.addWidget(self.createSpine_button)
        self.column2_layout.addWidget(self.createStrech_button)
        self.column2_layout.addWidget(self.widgetRibbons)
        self.column2_layout.addWidget(self.createRolls_button)
        self.column2_layout.addWidget(self.createStickyRibbon_button)

        self.splittertemp2 = QtWidgets.QLabel()
        self.splittertemp2.setMargin(125)
        self.column2_layout.addWidget(self.splittertemp2)

        # Add to main Layout
        self.mainLayout.addWidget(self.menubar)
        self.widgett = self.twoColumn(self.column1, self.column2)
        self.mainLayout.addWidget(self.widgett)
        self.mainLayout.setContentsMargins(3, 0, 3, 3)

        # ♥ Connect Button
        self.createCtrl.clicked.connect(self.createFkChain)
        self.addGrp_button.clicked.connect(self.addGroup)
        self.createFollow_button.clicked.connect(self.createFollow)
        self.createIkLimb_button.clicked.connect(self.createIkLimb)
        self.createSwitcher_button.clicked.connect(self.createSwitcher)
        self.createReverseFootLoc_button.clicked.connect(self.createReverseFootLoc)
        self.MirrorLoc_button.clicked.connect(self.mirrorLocators)
        self.createReverseFoot_button.clicked.connect(self.createReverseFoot)
        self.createSpine_button.clicked.connect(self.createSpine)
        self.createParentSpace_button.clicked.connect(self.createParentSpace)
        self.createOrienttSpace_button.clicked.connect(self.createOrientSpace)
        self.createStrech_button.clicked.connect(self.createStrech)
        self.createParentSpace_Mode.activated.connect(self.updateQlineSpace)
        self.replaceShape_button.clicked.connect(self.shapeChange)
        self.createRibbons_button.clicked.connect(self.createRibbons)
        self.createLookAt_button.clicked.connect(self.createLookAt)
        self.createUnstick_button.clicked.connect(self.createUnstick)
        self.createRolls_button.clicked.connect(self.createRolls)
        self.createStickyRibbon_button.clicked.connect(self.createStickyRibbon)
    #
    # Functions
    #

    # Ui functions
    #
    def createButton(self, name):
        """ Create a Button with light theme color

        """
        btn = QtWidgets.QPushButton(name)
        btn.setStyleSheet("QWidget { background-color: %s }" % self.light.name())

        return btn

    def createQline(self, text):
        """ Create a Qline with dark theme color

        """
        line = QtWidgets.QLineEdit(text)
        line.setStyleSheet("QWidget { background-color: %s }" % self.dark.name())

        return line

    def createCombo(self):
        """ Create a Combobox with light theme color

        """
        combo = QtWidgets.QComboBox()
        combo.setStyleSheet("QWidget { background-color: %s }" % self.light.name())

        return combo

    def comboBoxCurves(self):
        """ Create a QComboBox with all the curves

        """
        x = self.createCombo()
        for index, item in enumerate(bsData.controlNames):
            x.addItem(item, userData=index)

        return x

    def twoColumn(self, widget1, widget2):
        """ Create a two column layout H

        """
        widget = QtWidgets.QWidget(self)
        widget_layout = QtWidgets.QHBoxLayout(widget)
        widget_layout.addWidget(widget1)
        widget_layout.addWidget(widget2)
        widget_layout.setMargin(0)

        return widget

    def openBsConnect(self):

        import Blendshape_to_ctrl
        importlib.reload(Blendshape_to_ctrl)

        try:
            BlendshapeUI.deleteLater()
        except:
            pass
        BlendshapeUI = Blendshape_to_ctrl.BlendshapeConnect()

        try:
            BlendshapeUI.show()
        except:
            BlendshapeUI.deleteLater()

    # Auto Rig functions
    #
    def getSide(self, s):
        """ Get side based of a joint or ctrl

                Return : the current side
        """
        if '_L' in s:
            side = 'L'
        elif '_R' in s:
            side = 'R'
        else:
            side = ''
            cmds.warning('No side were found')

        return side

    def getLimb(self, s):
        """ Get limb based of a joint or ctrl

                Return : the current limb
        """
        limb = ''
        for tag in ['arm', 'hand']:
            if tag in s:
                limb = 'arm'

        for tag in ['leg', "foot"]:
            if tag in s:
                limb = 'leg'

        if limb is '':
            cmds.error(
                'No limb were found in the name of the joint. Please check the name. Expected a arm or leg in the name')

        return limb

    def shapeChange(self):
        sel = cmds.ls(sl=True)
        curveShape = self.cShape_replaceCtrl.currentText()

        new_ctrl = cmds.curve(d=1, p=bsData.cvTuples[curveShape], n='new_ctrl')
        old_ctrls = sel

        for old_ctrl in old_ctrls:
            dup = cmds.duplicate(new_ctrl, rc=True)
            cmds.delete(cmds.parentConstraint(old_ctrl, dup))
            cmds.parent(dup, old_ctrl)
            cmds.makeIdentity(dup, apply=True)
            old_shapes = cmds.listRelatives(old_ctrl, type="shape", f=True)
            ctrl_shapes = cmds.listRelatives(dup, type="shape", f=True)
            color = cmds.getAttr(old_shapes[0] + ".overrideColor")

            for ctrl_shape in ctrl_shapes:
                cmds.setAttr(ctrl_shape + ".overrideEnabled", 1)
                cmds.setAttr(ctrl_shape + ".overrideColor", color)
                ren = cmds.rename(ctrl_shape, old_ctrl + "Shape#")
                cmds.parent(ren, old_ctrl, relative=True, shape=True)

            to_connect = cmds.listConnections(old_shapes, c=1, p=1, et=1)
            if to_connect:
                attr = to_connect[0].split('.')[-1]
                cmds.connectAttr(to_connect[1], f"{ren}.{attr}")

            cmds.delete(dup)
            cmds.delete(old_shapes)

        cmds.delete(new_ctrl)
        cmds.select(clear=True)

    def createFkChain(self):
        """ Create a Controller for the selected joints and link them to their parent

                Input: Any Maya object
        """
        rootGroup = self.topGrp1.text()
        type_joint = self.typejoint.text()
        type_ctrl = self.typectrl.text()
        curveShape = self.cShape_ctrl.currentText()
        jointlist = []
        constType = self.constType.currentData()

        sl = cmds.ls(sl=1)

        # Define the joints to create a ctrl
        if not sl:
            cmds.error('No selection found. Please select any object to use the Create Control')

        if self.fkChains.isChecked():
            jointlist = cmds.listRelatives(allDescendents=True, type='joint')
            jointlist.append(sl[0])
            jointlist.reverse()
        else:
            jointlist = sl

        # Create the Controls
        for index, j in enumerate(jointlist):
            if not type_joint in j:
                ctrlName = j + '_' + type_ctrl
            else:
                ctrlName = j.replace(type_joint, type_ctrl)
            # Check if a ctrl already exist
            if not cmds.objExists(ctrlName):
                # Create the ctrl curve n groups
                ctrl = self.createCurveCtrl(ctrlName, curveShape, j, args_rot=False)[0]

                # Check the constraint to apply to the joint
                if constType == 0:
                    cmds.orientConstraint(ctrl, j, mo=1)
                elif constType == 1:
                    cmds.parentConstraint(ctrl, j, mo=1)
                elif constType == 2:
                    cmds.pointConstraint(ctrl, j, mo=1)

                if index == 0:
                    continue
                elif index == -1:
                    break
                else:
                    cmds.parentConstraint(jointlist[index - 1].replace(type_joint, type_ctrl), ctrl + '_' + rootGroup,
                                          mo=1)
                if self.fkChains.isChecked():
                    # Parent the current joint to its parent
                    parent_j = cmds.listRelatives(j, p=True, type='joint')
                    child_j = cmds.listRelatives(j, c=True, type='joint')

                    if parent_j:
                        try:
                            cmds.parentConstraint(parent_j[0].replace(type_joint, type_ctrl), ctrl + '_' + rootGroup, mo=1)
                        except:
                            cmds.warning(f'The controler of the parent joint {parent_j} is missing or was renamed ')
                    elif not parent_j:
                        cmds.warning(f'No Controler was found for the joint {j} . His inf group is without a constraint')
                    elif child_j is None or index == -1:
                        break
                    else:
                        continue


            else:
                cmds.warning(f'Conflict names. The joint {j} seems like it already has a controler matching his name')

        cmds.select(clear=True)

    def createFollow(self):
        """ Create a group on top of the selected object

                Input: joint
        """

        infGroup = self.topGrp2.text()

        sl = cmds.ls(sl=1, type='joint')
        if not sl:
            cmds.error('No selection found. Please select a joint to use the Create Follow')

        for s in sl:
            if 'parentConstraint' in s:
                cmds.error(
                    f'The joint {s} is link by a constraint Parent. Please use the follow on a orient constrained joint.')
                break
            ctrl = s.replace(self.typejoint.text(), self.typectrl.text())
            inf_const = ctrl + '_' + infGroup
            pose = cmds.group(ctrl, n=ctrl + "_followGrp")

            cmds.pointConstraint(s, pose, mo=True)

            cmds.addAttr(ctrl, at='double', ln='Follow', dv=0, min=0, max=1, keyable=True)
            const = cmds.listAttr('{}_parentConstraint1'.format(inf_const))[-1]
            cmds.connectAttr('{}.Follow'.format(ctrl), '{}_parentConstraint1.{}'.format(inf_const, const))

        cmds.select(clear=True)

    def addGroup(self):
        """ Create a group on top of the selected object

                Input: Any Maya object
        """

        sl = cmds.ls(sl=1)
        if not sl:
            cmds.warning('No selection found')
        prefix = self.addgGroup_prefix.text()
        suffix = self.addgGroup_suffix.text()

        for s in sl:
            composed_name = [prefix, s, suffix]
            print(composed_name)
            if prefix == '':
                composed_name.remove(prefix)
            elif suffix == '':
                composed_name.remove(suffix)
            name = '_'.join(composed_name)

            cmds.group(s, n=name)

        cmds.select(clear=True)

    def createCurveCtrl(self, ctrlName, curveShape, toMatch, args_rot=True):
        """ Create a Curve within a 2 groups hierarchy

            Args:
                ctrlName (str): name of the controller
                toMatch (mayaObj) : any maya object
                args_rot (bool): match orientation

            Returns:
                ctrl (MayaNode): The controller
                offset (str): Offset Group
                inf (str): Pose Group
        """

        rootGroup = self.topGrp1.text()
        infGroup = self.topGrp2.text()

        if curveShape == 'Circle':
            ctrl = cmds.circle(nr=(0, 1, 0), r=5, n=ctrlName)[0]
        else:
            ctrl = cmds.curve(d=1, p=bsData.cvTuples[curveShape], n=ctrlName)

        shape = cmds.listRelatives(ctrl, shapes=True)
        cmds.rename(shape, f'{ctrlName}Shape')

        inf = cmds.group(ctrl, n=ctrl + '_' + infGroup)
        offset = cmds.group(inf, n=ctrl + '_' + rootGroup)

        if toMatch is not None:
            cmds.matchTransform(offset, toMatch, rot=args_rot)

        return ctrl, offset, inf

    def overrideColor(self):

        crvs = cmds.ls(typ='nurbsCurve', ni=True, o=True, r=True)
        for crv in crvs:
            # Set Override Color
            if '_L' in crv:
                color = 13
            elif '_R' in crv:
                color = 6
            if 'hair' or 'switcher' in crv:
                color = 16
            else:
                color = 17

            cmds.setAttr(crv + '.overrideEnabled', 1)
            cmds.setAttr(crv + '.overrideColor', color)

    def createIkLimb(self):
        """ Create an Ik limb with its controller
            Support Biped limbs only

                Input: Take the first joint of the limb you want to rig

        """
        limb = None
        curveShape_ctrlEnd = self.cShape_ctrlEnd.currentText()
        curveShape_ctrlBase = self.cShape_ctrlBase.currentText()
        curveShape_ctrlPoleVector = self.cShape_ctrlPoleVector.currentText()
        s = cmds.ls(sl=1)[0]

        # get side
        side = self.getSide(s)

        # get limb
        limb = self.getLimb(s)

        cmds.duplicate(s, name=s.replace('sk', 'ik'), rc=True)

        # Update selection
        s = cmds.ls(sl=1)[0]

        # Rename sk to ik onto the duplicate joint chain
        duplicated = cmds.listRelatives(s, ad=True, type='joint')
        duplicated.append(s)

        if limb == 'arm':
            ikjoints = duplicated[-4:]
        elif limb == 'leg':
            ikjoints = duplicated

        for j in duplicated:
            if j in ikjoints:
                # Clean constraint applied to original joints
                const = cmds.listRelatives(j, ad=True, type='constraint')
                if const is not None:
                    cmds.delete(const)

                new_name = j.replace('sk1', 'ik')
                if 'end' in j:
                    new_name = j.replace('end', 'ikEnd')

                # Update ikjoint list with the new name
                cmds.rename(j, new_name)
                ikjoints = list(map(lambda x: x.replace(j, new_name), ikjoints))

            else:
                cmds.delete(j, hi='below')

        # Reverse to use a more logical order :
        # ['arm_L_ik', 'forearm_L_ik', 'wrist_L_ik', 'hand_L_ik']
        ikjoints.reverse()

        # Create Ctrl End
        ctrlName = ikjoints[3].replace('ik', 'ikctrl')
        ctrl = self.createCurveCtrl(ctrlName, curveShape_ctrlEnd, ikjoints[3], args_rot=False)[0]

        # Create ik rotatePlane Solver
        if limb == 'arm':
            ikname = f'arm_{side}_ikh'
        if limb == 'leg':
            ikname = f'leg_{side}_ikh'

        cmds.ikHandle(n=ikname, sj=ikjoints[0], ee=ikjoints[2])
        ikgrp = cmds.group(em=True, name=ikname + '_grp')
        cmds.matchTransform(ikgrp, ikname)
        cmds.parent(ikname, ikgrp)
        cmds.parent(ikgrp, ctrl)

        # Joint end
        if limb == 'arm':
            cmds.select(ikjoints[3])
            end = cmds.joint(name=ikjoints[3] + 'end')
            # How to define the distance to move the end joint
            #    use the distance tool on the meta of a finger to get the Ypos
            #
            if side == 'L':
                cmds.move(3, 0, 0, relative=True)
            if side == 'R':
                cmds.move(-3, 0, 0, relative=True)

        # Create ik singleChain Solver
        if limb == 'arm':
            ikHand = cmds.ikHandle(n=ikjoints[3] + 'h', sj=ikjoints[3], ee=end, sol='ikSCsolver')
            ikHandgrp = cmds.group(em=True, name=ikjoints[3] + 'h' + '_grp')
            cmds.matchTransform(ikHandgrp, ikjoints[3] + 'h')
            cmds.parent(ikjoints[3] + 'h', ikHandgrp)
            cmds.parent(ikHandgrp, ctrl)
        if limb == 'leg':
            ikFoot = cmds.ikHandle(n=ikjoints[3] + 'h', sj=ikjoints[3], ee=ikjoints[4], sol='ikSCsolver')
            ikFootgrp = cmds.group(em=True, name=ikjoints[3] + 'h' + '_grp')
            cmds.matchTransform(ikFootgrp, ikjoints[3] + 'h')
            cmds.parent(ikjoints[3] + 'h', ikFootgrp)
            cmds.parent(ikFootgrp, ctrl)

            ikToes = cmds.ikHandle(n=ikjoints[4] + 'h', sj=ikjoints[4], ee=ikjoints[5], sol='ikSCsolver')
            ikToesgrp = cmds.group(em=True, name=ikjoints[4] + 'h' + '_grp')
            cmds.matchTransform(ikToesgrp, ikjoints[4] + 'h')
            cmds.parent(ikjoints[4] + 'h', ikToesgrp)
            cmds.parent(ikToesgrp, ctrl)

        # Create Ctrl Base
        ctrlName = ikjoints[0].replace('ik', 'ikctrl')
        ctrl = self.createCurveCtrl(ctrlName, curveShape_ctrlBase, ikjoints[0], args_rot=False)[0]

        cmds.parent(ikjoints[0], ctrl)

        # Create PoleVector
        ctrlName = ikjoints[0].replace('ik', 'pvctrl')
        ctrl = self.createCurveCtrl(ctrlName, curveShape_ctrlPoleVector, ikjoints[1], args_rot=False)
        cmds.select(ctrl[1])
        if limb == 'arm':
            # How to define the distance to move the end joint
            #    use the distance tool on the meta of a finger to get the Ypos
            #
            cmds.move(0, 0, -10, relative=True)
        if limb == 'leg':
            cmds.move(0, 0, 10, relative=True)
        cmds.rotate(90, 0, 0)

        cmds.poleVectorConstraint(ctrl[0], ikname)

        cmds.select(clear=True)

    def mirrorLocators(self):
        """ Create locators used to build the reverse foot

                Input: None

        """
        if cmds.objExists('heel_L_loc'):
            side = '_L'
            newside = '_R'
        if cmds.objExists('heel_R_loc'):
            side = '_R'
            newside = '_L'
        if not cmds.objExists('heel_L_loc') and not cmds.objExists('heel_R_loc'):
            cmds.error('No locators were found to mirror. Please create and place them first')
        if cmds.objExists('heel_R_loc') and cmds.objExists('heel_L_loc'):
            cmds.error('Locators seems to already exist in the scene')

        loclist = [f'heel{side}_loc',
                   f'tiltOut{side}_loc',
                   f'tiltIn{side}_loc',
                   f'footTip{side}_loc',
                   f'toes{side}_loc',
                   f'ankle{side}_loc']

        for loc in loclist:
            locname = loc.replace(side, newside)
            cmds.spaceLocator(n=locname)

            cmds.matchTransform(locname, loc)
            locPos = cmds.getAttr(locname + '.translate')
            newPos = locPos[0]
            cmds.move(-newPos[0], newPos[1], newPos[2], locname)

            cmds.setAttr(locname + '.overrideEnabled', 1)
            cmds.setAttr(locname + '.overrideColor', 17)

    def createReverseFootLoc(self):
        """ Create locators used to build the reverse foot

                Input: The foot controller

        """
        ctrl = cmds.ls(sl=1)[0]

        side = self.getSide(ctrl)

        # Create the locator for the User to place
        loclist = [f'heel_{side}_loc',
                   f'tiltOut_{side}_loc',
                   f'tiltIn_{side}_loc',
                   f'footTip_{side}_loc',
                   f'toes_{side}_loc',
                   f'ankle_{side}_loc']

        for index, loc in enumerate(loclist):
            cmds.spaceLocator(n=loc)
            cmds.move(0, 0, 0 + index, loc)
            cmds.setAttr(loc + '.overrideEnabled', 1)
            cmds.setAttr(loc + '.overrideColor', 17)
        for loc in loclist[-2:]:
            cmds.matchTransform(loc, f'toes_{side}_sk')

    def createReverseFoot(self):
        """ Create a reverse Foot setup

                Input: The foot controller

        """
        ctrl = cmds.ls(sl=1)[0]
        side = self.getSide(ctrl)

        # Create the locator hierarchy
        loclist = [f'heel_{side}_loc',
                   f'tiltOut_{side}_loc',
                   f'tiltIn_{side}_loc',
                   f'footTip_{side}_loc',
                   f'toes_{side}_loc',
                   f'ankle_{side}_loc']

        # Check if all the locator needed exist
        for loc in loclist:
            if not cmds.objExists(loc):
                cmds.error('One or multiple locators are missing. Please create and place them before using the '
                           'Create Reverse Foot')

        for index, loc in enumerate(loclist[1:]):
            if loc in loclist[-2:]:
                cmds.parent(loc, f'footTip_{side}_loc')
            else:
                cmds.parent(loc, loclist[index])

        # Parent ikHandles to corresponding locator
        cmds.parent(f'toes_{side}_ikh_grp', f'toes_{side}_loc')
        cmds.parent(f'foot_{side}_ikh_grp', f'ankle_{side}_loc')
        cmds.parent(f'leg_{side}_ikh_grp', f'ankle_{side}_loc')
        cmds.parent(f'heel_{side}_loc', ctrl)

        #
        # Create the Attribute on the controller
        #
        attr1 = ['heelPivot', 'ballPivot', 'toesPivot', 'footTilt', 'toes']
        attr2 = ['footRoll', 'toesRoll']

        for i in attr1 + attr2:
            minAttr = 0
            if i in attr1:
                minAttr = -10
            cmds.addAttr(ctrl, at='double', ln=i, min=minAttr, max=10, dv=0, keyable=True)

        #   # Dict of the attribute and corresponding value to connect
        #   ['locator', 'axe', ctrlMin_Value, ctrlMax_Value, locMin_Value, locMax_Value]
        attdict = {
            'heelPivot': [f'heel_{side}_loc', 'Y', -10, 10, -90, 90],
            'ballPivot': [f'ankle_{side}_loc', 'Y', -10, 10, -90, 90],
            'toesPivot': [f'footTip_{side}_loc', 'Y', -10, 10, -90, 90],

            'footRoll': [f'ankle_{side}_loc', 'X', 0, 10, 0, 90],
            'toesRoll ': [f'footTip_{side}_loc', 'X', 0, 10, 0, 90],
            'toes': [f'toes_{side}_loc', 'X', -10, 10, -90, 90],
        }

        for attr in attdict:
            # Get the data from the dict
            # N store them into more explicit variables
            loc = attdict[attr][0]
            axe = attdict[attr][1]
            ctrlMin_Value = attdict[attr][2]
            ctrlMax_Value = attdict[attr][3]
            locMin_Value = attdict[attr][4]
            locMax_Value = attdict[attr][5]

            # Set Driven Keys to connect the attributes
            cmds.setDrivenKeyframe(f'{loc}', v=locMin_Value, at='rotate' + axe, cd=f'{ctrl}.{attr}', itt="linear",
                                   ott='linear', dv=ctrlMin_Value)

            cmds.setDrivenKeyframe(f'{loc}', v=locMax_Value, at='rotate' + axe, cd=f'{ctrl}.{attr}', itt="linear",
                                   ott='linear', dv=ctrlMax_Value)

        # ballPivot to Toes too
        cmds.connectAttr(f'ankle_{side}_loc_rotateY.output', f'toes_{side}_loc.rotateY')
        cmds.rename(f'ankle_{side}_loc_rotateY', f'ankleAndToes_{side}_loc_rY')

        # footTil Set Driven Keys
        if side == 'L':
            footTiltAttr = {
                f'tiltIn_{side}_loc': [90, 0, 0],
                f'tiltOut_{side}_loc': [0, 0, -90],
                'driver': [-10, 0, 10],
            }
        if side == 'R':
            footTiltAttr = {
                f'tiltIn_{side}_loc': [0, 0, -90],
                f'tiltOut_{side}_loc': [90, 0, 0],
                'driver': [-10, 0, 10],
            }

        for i in range(len(footTiltAttr)):
            cmds.setAttr(f'tiltIn_{side}_loc.rotateZ', footTiltAttr[f'tiltIn_{side}_loc'][i])
            cmds.setDrivenKeyframe(f'tiltIn_{side}_loc', at='rotateZ', cd=f'{ctrl}.footTilt', itt="linear",
                                   ott='linear', dv=footTiltAttr['driver'][i])
            cmds.setAttr(f'tiltOut_{side}_loc.rotateZ', footTiltAttr[f'tiltOut_{side}_loc'][i])
            cmds.setDrivenKeyframe(f'tiltOut_{side}_loc', at='rotateZ', cd=f'{ctrl}.footTilt', itt="linear",
                                   ott='linear', dv=footTiltAttr['driver'][i])

        for attr in attr1 + attr2:
            cmds.setAttr(f'{ctrl}.{attr}', 5)
            cmds.setAttr(f'{ctrl}.{attr}', 0)

    def createSwitcher(self):
        """ Create a reverse Foot setup

                Input: sk and ik chains

                    to show into the input
                cmds.addAttr(s, at='bool', ln='inMessage',dv=0, h=True)
                cmds.connectAttr('leg_R_options.message ', f'{s}.inMessage')
        """
        type_ctrl = self.typectrl.text()
        limb = None
        sel = cmds.ls(sl=1)
        s = sel[0]
        jointsk = s

        # get side
        side = self.getSide(s)

        # get limb
        limb = self.getLimb(s)

        skjoints = cmds.listRelatives(jointsk, ad=True, type='joint')
        skjoints.append(jointsk)

        Toe = skjoints[-5]

        skjoints = skjoints[-4:]
        skjoints.reverse()

        if limb == 'leg':
            skjoints.append(Toe)

        options_node = cmds.createNode('Unknow', n=f'{limb}_{side}_options')
        cmds.addAttr(options_node, at='float', ln='switchIk', min=0, max=1, dv=0, keyable=True)
        cmds.addAttr(options_node, at='float', ln='switchFk', min=0, max=1, dv=0, keyable=True, h=True)

        reverse_node = cmds.createNode('reverse', n=f'{limb}_{side}_reverseSwitchIk')
        cmds.connectAttr(f'{options_node}.switchIk', f'{reverse_node}.inputX')
        cmds.connectAttr(f'{reverse_node}.outputX', f'{options_node}.switchFk')

        for index, j in enumerate(skjoints):
            const = cmds.listRelatives(j, type='constraint')
            if const is not None:
                cmds.delete(const)

            if index == 2:
                child = [j.replace('sk', 'ik'), skjoints[3].replace('sk', type_ctrl)]
            else:
                child = [j.replace('sk', 'ik'), j.replace('sk', type_ctrl)]

            if index == 2:
                cmds.pointConstraint(child, j, mo=True)
            else:
                cmds.parentConstraint(child, j, mo=True)
            if index == 2:
                cmds.connectAttr(f'{options_node}.switchIk', f'{j}_pointConstraint1.{child[0]}W0')
                cmds.connectAttr(f'{options_node}.switchFk', f'{j}_pointConstraint1.{child[1]}W1')
            else:
                cmds.connectAttr(f'{options_node}.switchIk', f'{j}_parentConstraint1.{child[0]}W0')
                cmds.connectAttr(f'{options_node}.switchFk', f'{j}_parentConstraint1.{child[1]}W1')

            # Shape visibility
            if index == 1:
                pivotCtrl = skjoints[0].replace('sk', 'pvctrl')
                cmds.connectAttr(f'{options_node}.switchIk', f'{pivotCtrl}Shape.visibility')
                cmds.connectAttr(f'{options_node}.switchFk', f'{child[1]}Shape.visibility')

                # To clean
                cmds.addAttr(f'{pivotCtrl}', at='bool', ln='inMessage', dv=0, h=True)
                cmds.connectAttr(f'{options_node}.message', f'{pivotCtrl}.inMessage')
                cmds.addAttr(f'{child[1]}', at='bool', ln='inMessage', dv=0, h=True)
                cmds.connectAttr(f'{options_node}.message', f'{child[1]}.inMessage')

            elif index == 2:
                continue
            else:
                if cmds.objExists(f'{child[0]}ctrlShape'):
                    cmds.connectAttr(f'{options_node}.switchIk', f'{child[0]}ctrlShape.visibility')
                    # To clean
                    cmds.addAttr(f'{child[0]}', at='bool', ln='inMessage', dv=0, h=True)
                    cmds.connectAttr(f'{options_node}.message', f'{child[0]}.inMessage')
                cmds.connectAttr(f'{options_node}.switchFk', f'{child[1]}Shape.visibility')

                #To clean
                cmds.addAttr(f'{child[1]}', at='bool', ln='inMessage', dv=0, h=True)
                cmds.connectAttr(f'{options_node}.message', f'{child[1]}.inMessage')

        # Connect fingers
        if limb == 'arm':
            fingerlist = ['thumb', 'index', 'middle', 'ring', 'pinky']

            for finger in fingerlist:
                inf = f'{finger}_meta_{side}_ctrl_inf'
                target = [f"hand_{side}_ik", f"hand_{side}_ctrl"]
                cmds.parentConstraint(target, inf, mo=True)

                cmds.connectAttr(f'{options_node}.switchIk', f'{inf}_parentConstraint1.hand_{side}_ikW0')
                cmds.connectAttr(f'{options_node}.switchFk', f'{inf}_parentConstraint1.hand_{side}_ctrlW1')

    def moveNurbsVert(self, v, nurbs, jnt):
        """ Move the row of vertex of the designated nurbs to a jnt

                Args:
                V (int): row of the nurbs
                nurbs (nurbs) : nurbs object
                jnt (str): target transform

        """
        jntpos = cmds.xform(jnt, q=True, t=True, ws=True)

        posx = 0
        posy = 0
        posz = 0

        for i in range(2):
            x = f'{nurbs}.cv[{i}][{v}]'
            posx += cmds.xform(x, q=True, t=True, ws=True)[0]
            posy += cmds.xform(x, q=True, t=True, ws=True)[1]
            posz += cmds.xform(x, q=True, t=True, ws=True)[2]

        posx = posx / 2
        posy = posy / 2
        posz = posz / 2

        cmds.move(jntpos[0] - posx, jntpos[1] - posy, jntpos[2] - posz, f'{nurbs}.cv[0:1][{v}]', r=1)

    def moveNurbsVertU(self, u, nurbs, jnt):
        """ Move the row of vertex of the designated nurbs to a jnt

                Args:
                V (int): row of the nurbs
                nurbs (nurbs) : nurbs object
                jnt (str): target transform

        """
        jntpos = cmds.xform(jnt, q=True, t=True, ws=True)

        posx = 0
        posy = 0
        posz = 0

        for i in range(2):
            x = f'{nurbs}.cv[{u}][{i}]'
            posx += cmds.xform(x, q=True, t=True, ws=True)[0]
            posy += cmds.xform(x, q=True, t=True, ws=True)[1]
            posz += cmds.xform(x, q=True, t=True, ws=True)[2]

        posx = posx / 2
        posy = posy / 2
        posz = posz / 2

        cmds.move(jntpos[0] - posx, jntpos[1] - posy, jntpos[2] - posz, f'{nurbs}.cv[{u}][0:1]', r=1)

    def createSpine(self):
        """ Create the Spine

                Args: sel 1 = base joint
                      sel 2 = end joint

        """
        rootGroup = self.topGrp1.text()
        sel = cmds.ls(sl=1)
        jntBase = sel[0]
        jntEnd = sel[1]

        jntNb = int(re.findall(r'\d+', jntEnd)[0])

        # Create the nurbs surface
        cmds.nurbsPlane(ch=False, d=1, n='spine_surface', ax=[0, 1, 0])
        cmds.rebuildSurface(su=1, sv=jntNb - 1, dv=1, du=1)

        # Place the nurbs surface
        for i in range(jntNb):
            self.moveNurbsVert(i, 'spine_surface', f'spine0{i + 1}_sk')

        cmds.rebuildSurface('spine_surface', su=1, sv=(jntNb - 1), dv=3, du=1)

        for i in range(jntNb):
            x = i
            i = jntNb - i

            ctrlTweak = self.createCurveCtrl(f'spine0{i}_tweak_ctrl', 'Circle', f'spine0{i}_sk')

            # Loc Joint
            cmds.spaceLocator(n=f'spine0{i}_loc')

            # Loc Joint
            cmds.createNode('pointOnSurfaceInfo', n=f'spine0{i}_pointSurfaceInfo')
            cmds.connectAttr(f'spine_surfaceShape.worldSpace[0]', f'spine0{i}_pointSurfaceInfo.inputSurface')
            cmds.connectAttr(f'spine0{i}_pointSurfaceInfo.position', f'spine0{i}_loc.translate')
            cmds.setAttr(f'spine0{i}_pointSurfaceInfo' + '.parameterU', 0.5)
            cmds.setAttr(f'spine0{i}_pointSurfaceInfo' + '.parameterV', (100 - (x * 100) / (jntNb - 1)) * .01)

            # skip last jnt
            if i != jntNb:
                # Loc Up Vector
                cmds.spaceLocator(n=f'spine0{i}_upVector_loc')

                cmds.createNode('pointOnSurfaceInfo', n=f'spine0{i}_pointSurfaceInfo_upVector')
                cmds.connectAttr(f'spine_surfaceShape.worldSpace[0]',
                                 f'spine0{i}_pointSurfaceInfo_upVector.inputSurface')
                cmds.connectAttr(f'spine0{i}_pointSurfaceInfo_upVector.position', f'spine0{i}_upVector_loc.translate')
                cmds.setAttr(f'spine0{i}_pointSurfaceInfo_upVector' + '.parameterU', 1)
                cmds.setAttr(f'spine0{i}_pointSurfaceInfo_upVector' + '.parameterV',
                             (100 - (x * 100) / (jntNb - 1)) * .01)

                cmds.aimConstraint(f'spine0{i + 1}_loc', f'spine0{i}_loc', mo=False, aim=[0, 1, 0], u=[1, 0, 0],
                                   worldUpType="object", wuo=f'spine0{i}_upVector_loc')

            cmds.parentConstraint(f'spine0{i}_loc', ctrlTweak[1], mo=False)
            cmds.parentConstraint(ctrlTweak[0], f'spine0{i}_sk', mo=True)

        ik = {
            'hips': ['pelvis_sk'],
            'midSpine': ['spine03_sk'],
            'chest': ['spine05_sk'],
        }

        jntik = []
        for i in ik:
            ctrlIk = self.createCurveCtrl(f'{i}_ikctrl', 'Square', ik[i], args_rot=False)
            newjnt = cmds.joint(n=f'{i}_ik')
            cmds.parent(f'{i}_ik', ctrlIk[0])

            jntik.append(newjnt)

        cmds.skinCluster(jntik, 'spine_surface', tsb=True)

        cmds.orientConstraint('chest_ikctrl', f'spine0{jntNb}_loc', mo=True)
        cmds.parentConstraint('hips_ikctrl ', 'pelvis_sk', mo=False)

        fk = {
            0: ['bottomSpine_ctrl', 'spine01_sk '],
            1: ['midSpine_ctrl ', 'spine03_sk'],
            2: ['chest_ctrl', 'spine05_sk'],
        }

        for i in fk:
            ctrlfk = self.createCurveCtrl(fk[i][0], 'Circle', fk[i][1], args_rot=False)
            if i == 0:
                continue
            elif i == -1:
                break
            else:
                cmds.parentConstraint(fk[i - 1][0], ctrlfk[0] + '_' + rootGroup, mo=1)

        cmds.parentConstraint('midSpine_ctrl', 'midSpine_ikctrl' + '_' + rootGroup, mo=1)
        cmds.parentConstraint('chest_ctrl', 'chest_ikctrl' + '_' + rootGroup, mo=1)

        ctrlhips = self.createCurveCtrl('hips_ctrl', 'Circle', 'pelvis_sk', args_rot=False)
        cmds.parentConstraint('hips_ctrl', 'bottomSpine_ctrl' + '_' + rootGroup, mo=1)
        cmds.parentConstraint('hips_ctrl', 'hips_ikctrl' + '_' + rootGroup, mo=1)

    def updateQlineSpace(self):
        mode = self.createParentSpace_Mode.currentData()

        # Define Controler of parent space
        if mode == 0:
            # Custom
            ctrl_parent = []
        if mode == 1:
            # Hand
            ctrl_parent = ['WORLD', 'TRAJ', 'FLY', 'hips_ikctrl', 'chest_ikctrl', 'head_ctrl']
        if mode == 2:
            # Foot
            ctrl_parent = ['WORLD', 'TRAJ', 'FLY']
        if mode == 3:
            # Look at
            ctrl_parent = ['head_ctrl', 'FLY', 'TRAJ', 'WORLD']
        if mode == 4:
            # Head Orient
            ctrl_parent = ['chest_ikctrl', 'hips_ctrl', 'FLY', 'TRAJ', 'WORLD']

        ctrl_parent_str = ' '.join(ctrl_parent)
        self.createParentSpace_Qline.setText(ctrl_parent_str)
        self.createParentSpace_Qline.update()

    def createParentSpace(self):
        """
            Create Parent Space on selected controller

        """
        ctrl_base = cmds.ls(sl=True)[0]

        ctrl_parent = self.createParentSpace_Qline.text()
        ctrl_parent = ctrl_parent.split(" ")

        parent_space_list = []

        for ctrl in ctrl_parent:
            parent_space = ctrl.partition('_')[0]
            parent_space_list.append(parent_space)

        cmds.parentConstraint(ctrl_parent, ctrl_base + '_inf', mo=True)

        # add attr enum list
        enumName = ":".join(parent_space_list)
        cmds.addAttr(ctrl_base, ln="Parent_Space", at='enum', en=enumName, dv=0, keyable=True)

        # check condition based on index of parentspace list
        for index, attr in enumerate(parent_space_list):
            cond = cmds.createNode('condition', n=f'{ctrl_base}_cond')
            cmds.setAttr(cond + '.secondTerm', index)
            cmds.setAttr(cond + '.colorIfTrueR', 1)
            cmds.setAttr(cond + '.colorIfFalseR', 0)

            cmds.connectAttr(f'{ctrl_base}.Parent_Space', f'{cond}.firstTerm')
            cmds.connectAttr(f'{cond}.outColorR', f'{ctrl_base}_inf_parentConstraint1.{ctrl_parent[index]}W{index}')

    def createOrientSpace(self):
        """
            Create Orient Space on selected controller

        """
        ctrl_base = cmds.ls(sl=True)[0]

        ctrl_parent = self.createParentSpace_Qline.text()
        ctrl_parent = ctrl_parent.split(" ")

        parent_space_list = ['None']

        for ctrl in ctrl_parent:
            parent_space = ctrl.partition('_')[0]
            parent_space_list.append(parent_space)

        cmds.orientConstraint(ctrl_parent, ctrl_base + '_pose', mo=True)

        # add attr enum list
        enumName = ":".join(parent_space_list)
        cmds.addAttr(ctrl_base, ln="Orient_Space", at='enum', en=enumName, dv=0, keyable=True)

        # check condition based on index of parentspace list
        for index, attr in enumerate(parent_space_list[1:]):
            cond = cmds.createNode('condition', n=f'{ctrl_base}_cond')
            cmds.setAttr(cond + '.secondTerm', index + 1)
            cmds.setAttr(cond + '.colorIfTrueR', 1)
            cmds.setAttr(cond + '.colorIfFalseR', 0)

            cmds.connectAttr(f'{ctrl_base}.Orient_Space', f'{cond}.firstTerm')
            cmds.connectAttr(f'{cond}.outColorR', f'{ctrl_base}_pose_orientConstraint1.{ctrl_parent[index]}W{index}')

    def createStrech(self):
        """
            Create Stretch n Squash set up

                Input : select the base joint of the limb

        """
        s = cmds.ls(sl=1)[0]
        sel = cmds.listRelatives(s, ad=True, type='joint')
        sel.append(s)
        sel.reverse()

        jnts = sel[:4]

        # Set up name variables
        name0 = jnts[0].partition('_')[0]
        name1 = jnts[1].partition('_')[0]
        name2 = jnts[2].partition('_')[0]
        name3 = jnts[3].partition('_')[0]
        limb = jnts[0].replace('_sk', "")
        ikBase = jnts[0].replace('sk', "ikctrl")
        ikEnd = jnts[3].replace('sk', "ikctrl")
        loc_list = []

        # Create distance locators
        for jnt in jnts[:3]:
            locname = jnt.replace('sk', 'loc_stretch')
            cmds.spaceLocator(n=locname)
            cmds.matchTransform(locname, jnt)
            loc_list.append(locname)

        # parent t he loc
        cmds.parent(loc_list[1], loc_list[0])
        cmds.setAttr(loc_list[1] + '.rotateY', 0)
        cmds.setAttr(loc_list[1] + '.rotateZ', 0)
        cmds.parent(loc_list[2], loc_list[1])

        # loc distance
        # loc_list[0] n loc_list[2]
        locDist = cmds.createNode('distanceBetween', n=f'{name0}To{name2}_distanceBetween')
        cmds.connectAttr(f'{loc_list[0]}.worldMatrix[0]', f'{locDist}.inMatrix1')
        cmds.connectAttr(f'{loc_list[2]}.worldMatrix[0]', f'{locDist}.inMatrix2')
        # ctrl distance transform
        # arm_L_ikctrl n hand_L_ikctrl    Transform
        ctrlDist = cmds.createNode('distanceBetween', n=f'{name0}CtrlTo{name3}Ctrl_distanceBetween')
        cmds.connectAttr(f'{ikBase}.worldMatrix[0]', f'{ctrlDist}.inMatrix1')
        cmds.connectAttr(f'{ikEnd}.worldMatrix[0]', f'{ctrlDist}.inMatrix2')

        # Divide
        divide = cmds.createNode('multiplyDivide', n=f'{limb}_stretchSquashFactor_multiplyDivide')
        cmds.setAttr(divide + '.operation', 2)

        # Add Attribute to the option node
        arm_options = jnts[0].replace('sk', "options")
        arm_options = arm_options.replace('upleg', "leg")
        cmds.addAttr(arm_options, at='float', ln='squash', min=0, max=1, dv=0, keyable=True)
        cmds.addAttr(arm_options, at='float', ln='stretch', min=0, max=4, dv=0, keyable=True)

        # Clamp
        clamp = cmds.createNode('clamp', n=f'{limb}_clampFactor_clamp')
        cmds.connectAttr(f'{divide}.outputX', f'{clamp}.inputR')
        cmds.connectAttr(f'{ctrlDist}.distance', f'{divide}.input1X')
        cmds.connectAttr(f'{locDist}.distance', f'{divide}.input2X')

        # Reverse node
        reverse = cmds.createNode('reverse', n=f'{limb}_reverseSquashValue_Reverse')
        cmds.connectAttr(f'{arm_options}.squash', f'{reverse}.inputX')
        cmds.connectAttr(f'{reverse}.outputX', f'{clamp}.minR')

        # Offset node
        off = cmds.createNode('addDoubleLinear', n=f'{limb}_offsetStretchValue_addDoubleLinear')
        cmds.connectAttr(f'{arm_options}.stretch', f'{off}.input1')
        cmds.connectAttr(f'{off}.output', f'{clamp}.maxR')
        cmds.setAttr(off + '.input2', 1)

        #
        # Connect to ik jnts

        ikjnt1 = jnts[1].replace('sk', "ik")
        mult1 = cmds.createNode('multDoubleLinear', n=f'{limb}_{name1}_x_factor_multDoublelinear')
        cmds.connectAttr(f'{loc_list[1]}.translateY', f'{mult1}.input1')
        cmds.connectAttr(f'{clamp}.outputR', f'{mult1}.input2')
        cmds.connectAttr(f'{mult1}.output', f'{ikjnt1}.translateY')

        ikjnt2 = jnts[2].replace('sk', "ik")
        mult2 = cmds.createNode('multDoubleLinear', n=f'{limb}_{name2}_x_factor_multDoublelinear')
        cmds.connectAttr(f'{loc_list[2]}.translateY', f'{mult2}.input1')
        cmds.connectAttr(f'{clamp}.outputR', f'{mult2}.input2')
        cmds.connectAttr(f'{mult2}.output', f'{ikjnt2}.translateY')


    def placeSurface(self, surf, jntbase, jntend, limb):
        loc_list = []
        for i in range(4):
            x = 1
            loc1 = cmds.spaceLocator(n=f'loc_temp{i}')[0]
            cmds.parent(loc1, jntbase, relative=True)
            if i % 2:
                x = -1
            if limb == 'leg':
                cmds.setAttr(f"{loc1}.translateX", x)
            if limb == 'arm':
                cmds.setAttr(f"{loc1}.translateZ", x)
            loc_list.append(loc1)

        y = cmds.xform(jntend, q=True, t=True, r=True)
        cmds.move(y[0], y[1], y[2], loc_list[2], r=True, os=True)
        cmds.move(y[0], y[1], y[2], loc_list[3], r=True, os=True)

        x = cmds.xform(loc_list[1], q=True, t=True, ws=True)
        cmds.move(x[0], x[1], x[2], f'{surf}.cv[0][0]')
        x = cmds.xform(loc_list[0], q=True, t=True, ws=True)
        cmds.move(x[0], x[1], x[2], f'{surf}.cv[1][0]')
        x = cmds.xform(loc_list[3], q=True, t=True, ws=True)
        cmds.move(x[0], x[1], x[2], f'{surf}.cv[0][1]')
        x = cmds.xform(loc_list[2], q=True, t=True, ws=True)
        cmds.move(x[0], x[1], x[2], f'{surf}.cv[1][1]')

        cmds.delete(loc_list)

    def createRibbons(self):
        """
            Create Ribbons set up

                Input : select the base joint of the limb

        """
        jntNb = self.nbrTweaks.value()
        rootGroup = self.topGrp1.text()
        infGroup = self.topGrp2.text()

        s = cmds.ls(sl=True)
        if not s:
            cmds.error('No selection found. Please select any object to use the Create Control')

        s = s[0]

        sel = cmds.listRelatives(s, ad=True, type='joint')
        sel.append(s)
        sel.reverse()
        jnts = sel[:4]

        # ['arm_L_sk', 'forearm_L_sk', 'wrist_L_sk', 'hand_L_sk']
        name0 = jnts[0].partition('_')[0]
        name1 = jnts[1].partition('_')[0]
        name2 = jnts[2].partition('_')[0]
        name3 = jnts[3].partition('_')[0]

        side = self.getSide(s)

        limb = self.getLimb(s)

        # Create the nurbs surface
        surf1 = cmds.nurbsPlane(ch=False, d=1, n=f'{limb}_{side}_surface', ax=[0, 1, 0])
        surf2 = cmds.nurbsPlane(ch=False, d=1, n=f'{name1}_{side}_surface', ax=[0, 1, 0])

        # Place the nurbs surface
        self.placeSurface(f'{limb}_{side}_surface', jnts[0], jnts[1], limb)
        self.placeSurface(f'{name1}_{side}_surface', jnts[1], jnts[2], limb)

        # Rebuild the nurbs surface
        cmds.rebuildSurface(f'{limb}_{side}_surface', su=1, sv=4, du=1, dv=3)
        cmds.rebuildSurface(f'{name1}_{side}_surface', su=1, sv=4, du=1, dv=3)

        # Create Ctrl
        rotjnt = 'elbow'
        if limb == 'leg':
            rotjnt = 'knee'
        armmid_ctrl = self.createCurveCtrl(f"{limb}Mid_{side}_ctrl", "Circle", None, args_rot=False)
        elb_ctrl = self.createCurveCtrl(f"{rotjnt}_{side}_ctrl", "Circle", jnts[1], args_rot=False)
        foremid_ctrl = self.createCurveCtrl(f"{name1}Mid_{side}_ctrl", "Circle", None, args_rot=False)

        options = f"{limb}_{side}_options"
        cmds.addAttr(options, at='bool', ln='deformersVisibility', dv=1, keyable=True)
        cmds.addAttr(options, at='bool', ln='tweakersVisibility', dv=1, keyable=True)
        cmds.connectAttr(f'{options}.deformersVisibility', f'{armmid_ctrl[0]}Shape.visibility')
        cmds.connectAttr(f'{options}.deformersVisibility', f'{elb_ctrl[0]}Shape.visibility')
        cmds.connectAttr(f'{options}.deformersVisibility', f'{foremid_ctrl[0]}Shape.visibility')

        for i in [armmid_ctrl, elb_ctrl, foremid_ctrl]:
            cmds.addAttr(i[0], at='bool', ln='inMessage', dv=0, h=True)
            cmds.connectAttr(f'{options}.message ', f'{i[0]}.inMessage')

        armmid_jnt = armmid_ctrl[0].replace('_ctrl', '_jnt')
        cmds.joint(n=armmid_jnt)
        cmds.parent(armmid_jnt, armmid_ctrl[0])
        foremid_jnt = foremid_ctrl[0].replace('_ctrl', '_jnt')
        cmds.joint(n=foremid_jnt)
        cmds.parent(foremid_jnt, foremid_ctrl[0])

        for i in [f'{limb}Base_{side}_jnt', f'{limb}Tip_{side}_jnt', f'{name1}Base_{side}_jnt',
                  f'{name1}Tip_{side}_jnt']:
            cmds.select(clear=True)
            jnt = cmds.joint(n=i)
            inf = cmds.group(jnt, n=i.replace('jnt', infGroup))
            offset = cmds.group(inf, n=i.replace('jnt', rootGroup))

        # Point Constraints
        # To dict
        #
        cmds.pointConstraint(jnts[0], f'{limb}Base_{side}_{rootGroup}', mo=False)
        cmds.pointConstraint(jnts[0], elb_ctrl[0], armmid_ctrl[1], mo=False)
        cmds.pointConstraint(elb_ctrl[0], f'{limb}Tip_{side}_{rootGroup}', mo=False)
        cmds.pointConstraint(elb_ctrl[0], f'{name1}Base_{side}_{rootGroup}', mo=False)
        cmds.pointConstraint(elb_ctrl[0], jnts[2], foremid_ctrl[1], mo=False)
        cmds.pointConstraint(jnts[2], f'{name1}Tip_{side}_{rootGroup}', mo=False)

        cmds.pointConstraint(jnts[1], elb_ctrl[1], mo=False)

        # Aim Constraints
        #   [target   obj   aim   worldUpObject]
        attdict = {
            1: [armmid_ctrl[0], f'{limb}Base_{side}_{rootGroup}', [0, 1, 0], jnts[0]],
            2: [elb_ctrl[0], armmid_ctrl[1], [0, 1, 0], jnts[0]],
            3: [armmid_ctrl[0], f'{limb}Tip_{side}_{rootGroup}', [0, -1, 0], jnts[0]],

            4: [foremid_ctrl[0], f'{name1}Base_{side}_{rootGroup}', [0, 1, 0], jnts[1]],
            5: [elb_ctrl[0], foremid_ctrl[1], [0, -1, 0], jnts[1]],
            6: [foremid_ctrl[0], f'{name1}Tip_{side}_{rootGroup}', [0, -1, 0], jnts[1]],
        }

        for attr in attdict:
            # Get the data from the dict
            target = attdict[attr][0]
            obj = attdict[attr][1]
            aimdir = attdict[attr][2]
            UpObject = attdict[attr][3]

            cmds.aimConstraint(target, obj, mo=False, aim=aimdir, upVector=[0, 0, 1], worldUpType="objectrotation",
                               worldUpObject=UpObject, worldUpVector=[0, 0, 1])

        cmds.orientConstraint(jnts[0], jnts[1], elb_ctrl[1], mo=False)
        cmds.setAttr(f"{elb_ctrl[1]}_orientConstraint1.interpType", 2)

        # Skin ribbon
        list_jnt1 = []
        list_jnt2 = []

        for i in ['Base', 'Mid', 'Tip']:
            list_jnt1.append(f'{limb}{i}_{side}_jnt')
            list_jnt2.append(f'{name1}{i}_{side}_jnt')

        cmds.skinCluster(list_jnt1, f'{limb}_{side}_surface', tsb=True)
        cmds.skinCluster(list_jnt2, f'{name1}_{side}_surface', tsb=True)

        # Tweaks
        for index, limb in enumerate([limb, name1]):
            temp = limb
            if limb == 'leg':
                temp = name0

            off = (100 / jntNb)
            c = 100 - off
            for i in range(jntNb):
                x = i
                i = jntNb - i
                paramu = ((c - (x * c) / (jntNb - 1)) * .01) + (off / 2) * 0.01

                follicleshape = cmds.createNode("follicle", n=f'{limb}_{side}_tweaker0{i}_follicleShape')
                follicletrans = f'{limb}_{side}_tweaker0{i}_follicle'

                cmds.connectAttr(f'{limb}_{side}_surface.worldSpace[0]', f'{follicleshape}.inputSurface')
                cmds.connectAttr(f'{follicleshape}.outTranslate', f'{follicletrans}.translate')
                cmds.connectAttr(f'{follicleshape}.outRotate', f'{follicletrans}.rotate')

                cmds.setAttr(f'{follicleshape}.parameterV', paramu)
                cmds.setAttr(f'{follicleshape}.parameterU', 0.5)

                name = follicleshape.replace('_follicleShape', '_ctrl')
                ctrl = self.createCurveCtrl(name, "Circle", f'{temp}_{side}_sk', args_rot=False)
                cmds.parentConstraint(follicletrans, ctrl[1], mo=True)

                cmds.setAttr(f'{ctrl[1]}_parentConstraint1.target[0].targetOffsetTranslateX', 0)
                cmds.setAttr(f'{ctrl[1]}_parentConstraint1.target[0].targetOffsetTranslateY', 0)
                cmds.setAttr(f'{ctrl[1]}_parentConstraint1.target[0].targetOffsetTranslateZ', 0)

                cmds.select(f'{temp}_{side}_sk')
                jnttweak = cmds.joint(n=f'{limb}_{side}_tweaker0{i}_sk')
                cmds.parentConstraint(ctrl[0], jnttweak, mo=False)

                cmds.connectAttr(f'{options}.tweakersVisibility', f'{ctrl[0]}Shape.visibility')

        # Pin
        #
        ctrl = self.createCurveCtrl(f'{self.getLimb(jnts[0])}_{side}_pinctrl', 'Box', jnts[1], args_rot=False)
        cmds.addAttr(ctrl[0], at='bool', ln='inMessage', dv=0, h=True)
        cmds.connectAttr(f'{options}.message ', f'{ctrl[0]}.inMessage')
        cmds.pointConstraint(ctrl[0], elb_ctrl[2])

        self.createPairblend(elb_ctrl[2], 'point', ['Translate'], options, 'pin', createAttr=True)

        cmds.connectAttr(f'{options}.deformersVisibility', f'{ctrl[0]}Shape.visibility')

    def createPairblend(self, ctrl, constraint, types, options, attr, createAttr: bool):
        """
            Create a pair blend on specified ctrl n constraint

        """
        pair = cmds.createNode('pairBlend', n=f'{ctrl}_{constraint}Constraint_pairBlend')

        for type in types:
            typelow = type.lower()
            type = typelow.capitalize()

            for i in ["X", "Y", "Z"]:
                cmds.connectAttr(f'{ctrl}_{constraint}Constraint1.constraint{type}.constraint{type}{i}',
                                 f'{pair}.in{type}2.in{type}{i}2')

                cmds.connectAttr(f'{pair}.out{type}.out{type}{i}', f'{ctrl}.{typelow}.{typelow}{i}', f=True)

        if createAttr is True:
            if not cmds.attributeQuery(attr, ex=True, n=options):
                cmds.addAttr(options, at='float', ln=attr, min=0, max=1, dv=0, keyable=True)
            cmds.connectAttr(f'{options}.{attr}', f'{pair}.weight')

        return pair

    def createUnstick(self):
        """


        """
        s = cmds.ls(sl=True)
        if not s:
            cmds.error('No selection found. Please select any object to use')

        sel = cmds.listRelatives(s[1], ad=True, type='joint')
        sel.append(s[1])
        sel.reverse()

        jnts = sel[:-1]
        jntNb = len(jnts)

        if not cmds.attributeQuery('unstickTongue', ex=True, n=s[0]):
            cmds.addAttr(s[0], at='float', ln='unstickTongue', min=0, max=1, dv=0, keyable=True)

        int = (1 / jntNb)
        for index, jnt in enumerate(jnts):
            if index == 0:
                cmds.parentConstraint('head_ctrl ', jnt.replace('_sk', '_ctrl_pose'), mo=True)
                pair = self.createPairblend(jnt.replace('_sk', '_ctrl_pose'), 'parent', ['Rotate', 'Translate'], s[0],
                                            'unstickTongue', createAttr=False)
            else:
                cmds.orientConstraint('head_ctrl ', jnt.replace('_sk', '_ctrl_pose'), mo=True)

                pair = self.createPairblend(jnt.replace('_sk', '_ctrl_pose'), 'orient', ['Rotate'], s[0],
                                            'unstickTongue', createAttr=False)

            new_pair = f"unstickTongue0{index + 1}_pairBlend"
            cmds.rename(pair, new_pair)

            intervalUp = index * int
            intervalDown = intervalUp + int

            cmds.setDrivenKeyframe(f'{new_pair}', v=0, at='weight', cd=f'{s[0]}.unstickTongue', itt="linear",
                                   ott='linear', dv=1 - intervalDown)

            cmds.setDrivenKeyframe(f'{new_pair}', v=1, at='weight', cd=f'{s[0]}.unstickTongue', itt="linear",
                                   ott='linear', dv=1 - intervalUp)

    def createLookAt(self):
        """


        """
        ctrl_L = self.createCurveCtrl("lookAt_L_ctrl", "Circle", "eye_L_sk", args_rot=False)
        ctrl_R = self.createCurveCtrl("lookAt_R_ctrl", "Circle", "eye_R_sk", args_rot=False)
        ctrl = self.createCurveCtrl("lookAt_ctrl", "Circle", "eye_R_sk", args_rot=False)
        cmds.setAttr(f"{ctrl[1]}.translateX", 0)
        cmds.setAttr(f"{ctrl[1]}.rotateY", 0)
        cmds.setAttr(f"{ctrl[1]}.rotateZ", 0)

        for i in [ctrl_L[1], ctrl_R[1]]:
            cmds.move(0, 5, 0, i, relative=True, os=True)
        cmds.move(0, 0, 5, ctrl[1], relative=True, ws=True)

        for i in ['L', 'R']:
            cmds.parent(f'lookAt_{i}_ctrl_inf', ctrl[0])

            loc = cmds.spaceLocator(n=f'eye_{i}_upVector_loc')
            cmds.parent(loc, 'head_sk', relative=True)
            cmds.matchTransform(loc, f'eye_{i}_sk')
            cmds.move(0, 0, 2, loc, relative=True, os=True)

            cmds.aimConstraint(f'lookAt_{i}_ctrl', f'eye_{i}_ctrl_pose', mo=False, aim=[0, 1, 0], u=[0, 0, 1],
                               worldUpType="object", wuo=f'eye_{i}_upVector_loc')

        options_node = cmds.createNode('Unknow', n=f'eyes_options')
        cmds.addAttr(options_node, at='float', ln='lookAt', min=0, max=1, dv=1, keyable=True)

        for i in [ctrl_L[0], ctrl_R[0], ctrl[0]]:
            cmds.connectAttr(f'{options_node}.lookAt', f'{i}Shape.visibility')
            cmds.addAttr(i, at='bool', ln='inMessage', dv=0, h=True)
            cmds.connectAttr(f'{options_node}.message ', f'{i}.inMessage')

        for i in ['L', 'R']:
            self.createPairblend(f'eye_{i}_ctrl_pose', 'aim', ['Rotate'], options_node, 'pin', createAttr=True)


    def createRolls(self):
        """
            sel = hand

        """
        s = cmds.ls(sl=True)
        if not s:
            cmds.error('No selection found. Please select any object to use the Rolls')
        cmds.select(clear=True)

        side = self.getSide(s[0])
        limb = self.getLimb(s[0])

        name = s[0].split('_')[0]

        upperlimb = False
        if limb is 'arm':
            tip = 'forearm'
        if limb is 'leg':
            tip = 'dnleg'
        if name in ['arm', 'upleg']:
            upperlimb = True
            tip = limb

        jnt = cmds.joint(n=f'{name}_{side}_twist_jnt')
        jntEnd = cmds.joint(n=f'{name}_{side}_twist_end')

        cmds.setAttr(f"{jnt}.rotateOrder", 1)

        if side == 'L':
            cmds.setAttr(f"{jntEnd}.translateY", 5)
        else:
            cmds.setAttr(f"{jntEnd}.translateY", -5)

        grp = cmds.group(jnt, n=f'{name}_{side}_twist_inf')

        cmds.matchTransform(grp, s[0])
        parent = cmds.listRelatives(s[0], ap=True)[0]
        cmds.parentConstraint(f'{parent}', grp, mo=True)


        ikChain = cmds.ikHandle(n=f'{name}_{side}_twist_ikh', sj=jnt, ee=jntEnd, sol='ikSCsolver')
        ikChaingrp = cmds.group(em=True, name=f'{name}_{side}_twist_ikh' + '_grp')
        cmds.matchTransform(ikChaingrp, f'{name}_{side}_twist_ikh')
        cmds.parent(f'{name}_{side}_twist_ikh', ikChaingrp)
        cmds.parent(ikChaingrp, grp)
        cmds.orientConstraint(s[0], f'{name}_{side}_twist_ikh', mo=False)

        # Pair Blend


        pair = cmds.createNode('pairBlend', n=f'{name}_{side}_HalfTwist_pairBlend')

        if upperlimb is True:
            mult = cmds.createNode('multDoubleLinear', n=f'{name}TwistInverse_{side}_mutlDoubleLinear')
            if side == 'L':
                cmds.setAttr(f"{mult}.input2", -1)
            else:
                cmds.setAttr(f"{mult}.input2", 1)
            cmds.connectAttr(f"{jnt}.rotateY", f"{mult}.input1")
            cmds.connectAttr(f"{mult}.output", f'{tip}Base_{side}_jnt.rotateY')
            cmds.connectAttr(f"{mult}.output", f"{pair}.inRotateY2")
            cmds.connectAttr(f"{pair}.outRotateY", f'{name}Mid_{side}_jnt.rotateY')
        else:
            cmds.connectAttr(f"{jnt}.rotateY", f"{pair}.inRotateY2")
            cmds.connectAttr(f"{jnt}.rotateY", f"{tip}Tip_{side}_jnt.rotateY")
            cmds.connectAttr(f"{pair}.outRotateY", f'{tip}Mid_{side}_jnt.rotateY')

        cmds.setAttr(f"{pair}.weight", 0.5)
        cmds.setAttr(f"{pair}.rotInterpolation", 1)

    def createStickyRibbon(self):
        """
            sel = surface
                n joints

        """
        s = cmds.ls(sl=True)
        if not s:
            cmds.error('No selection found. Please select any object to use the Rolls')
        cmds.select(clear=True)

        surface = s[0]
        joints = s[1:]
        for joint in joints:
            ctrlName = joint.replace('sk', 'ctrl')
            ctrl = self.createCurveCtrl(ctrlName, 'Circle', joint, args_rot=False)
            inf = ctrl[1]
            ctrl = ctrl[0]
            cmds.parentConstraint(ctrl, joint, mo=1)

            follicleshape = cmds.createNode("follicle", n=joint.replace('sk', 'follicleShape'))
            follicletrans = joint.replace('sk', 'follicle')

            cmds.connectAttr(f'{surface}.worldSpace[0]', f'{follicleshape}.inputSurface')
            cmds.connectAttr(f'{follicleshape}.outTranslate', f'{follicletrans}.translate')
            cmds.connectAttr(f'{follicleshape}.outRotate', f'{follicletrans}.rotate')

            closestPoint = cmds.createNode("closestPointOnSurface", n=joint.replace('sk', '_closestPointOnSurface'))
            cmds.connectAttr(f'{surface}.worldSpace[0]', f'{closestPoint}.inputSurface')
            posx = cmds.xform(joint, q=True, t=True, ws=True)[0]
            posy = cmds.xform(joint, q=True, t=True, ws=True)[1]
            posz = cmds.xform(joint, q=True, t=True, ws=True)[2]
            cmds.setAttr(f'{closestPoint}.inPositionX', posx)
            cmds.setAttr(f'{closestPoint}.inPositionY', posy)
            cmds.setAttr(f'{closestPoint}.inPositionZ', posz)

            paramU = cmds.getAttr(f'{closestPoint}.result.parameterU')
            paramV = cmds.getAttr(f'{closestPoint}.result.parameterV')
            maxU = cmds.getAttr(f'{surface}.minMaxRangeU')[0][1]
            maxV = cmds.getAttr(f'{surface}.minMaxRangeV')[0][1]
            cmds.setAttr(f'{follicleshape}.parameterU', paramU/maxU)
            cmds.setAttr(f'{follicleshape}.parameterV', paramV/maxV)

            cmds.parentConstraint(follicletrans, inf, mo=True)
