# -*- coding: utf-8 -*-

import maya.cmds as cmds

class CombinedGroomToolUI:
    """
    �ռ������һ���ߣ�Groom Alembic Prep Tool
    - ʹ�ñ�ǩҳ (Tabs) ���л� "Group ID" �� "Guide Tagger" ���ܡ�
    - �ṩ�����б�Ҫ�Ĺ�����ΪUE��Groomϵͳ׼��Alembic���ԡ�(����ӽ�ע)
    """
    
    def __init__(self):
        self.window_name = "CombinedGroomToolWindow"
        self.window_title = "�����߼�����UE��ë����������"
        
        self.group_id_attr = "groom_group_id"
        self.guide_attr = "groom_guide"
        
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name, window=True)
            
        self.window = cmds.window(
            self.window_name,
            title=self.window_title,
            widthHeight=(350, 450), # ������
            sizeable=True
        )
        
        self.build_ui()
        cmds.showWindow(self.window)

    def build_ui(self):
        base_layout = cmds.frameLayout(labelVisible=False, borderVisible=False, marginWidth=5, marginHeight=5)
        self.tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5, parent=base_layout)
        
        tab1_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10)
        self.populate_group_id_tab()
        cmds.setParent('..')

        tab2_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10)
        self.populate_guide_tagger_tab()
        cmds.setParent('..')

        cmds.tabLayout(
            self.tabs,
            edit=True,
            tabLabel=((tab1_layout, "Group ID Tool"), (tab2_layout, "Guide Tagger"))
        )

    def populate_group_id_tab(self):
        """��� 'Group ID Tool' ��ǩҳ��UIԪ�ء�"""
        cmds.text(
            label="1. ѡ��ë�����߻������顣\n2. ������ID (����: 0, 1, 2...)\n3. ��� 'Apply' ��ť��",
            align='left'
        )
        cmds.separator(height=10, style='in')
        
        self.group_id_field = cmds.intFieldGrp(
            label='Group ID:', numberOfFields=1, value1=0, columnWidth2=[80, 200]
        )
        cmds.button(
            label="Apply Group ID to Selection", command=self.apply_group_id, height=40,
            backgroundColor=(0.2, 0.5, 0.2)
        )
        cmds.separator(height=20, style='in')
        cmds.text(label="����Alembicʱ, ���������������:", align='left')
        cmds.textFieldGrp(
            label="Attribute Name:", text=self.group_id_attr, editable=False, columnWidth2=[80, 200]
        )
        
        # ==========================================================
        #  ���� ��ע ����
        # ==========================================================
        cmds.separator(height=20, style='in')
        cmds.text(label="��è��������Ƥ", align='center')
        # ==========================================================

    def populate_guide_tagger_tab(self):
        """��� 'Guide Tagger' ��ǩҳ��UIԪ�ء�"""
        cmds.text(
            label="1. ѡ������ (��Ⱦë��������ë��)��\n2. �������Ķ�Ӧ��ť���б�ǡ�",
            align='left'
        )
        cmds.separator(height=15, style='in')
        cmds.button(
            label="���Ϊ: ��Ⱦë�� (guide=0)", command=lambda *args: self.apply_guide_id(0),
            height=40, backgroundColor=(0.2, 0.4, 0.6)
        )
        cmds.button(
            label="���Ϊ: ����ë�� (guide=1)", command=lambda *args: self.apply_guide_id(1),
            height=40, backgroundColor=(0.2, 0.7, 0)
        )
        cmds.separator(height=15, style='in')
        cmds.text(label="����Alembicʱ, �ǵ���������������:")
        cmds.textFieldGrp(
            label="Attribute Name:", text=self.guide_attr, editable=False, columnWidth2=[80, 200]
        )
        
        # ==========================================================
        #  ���� ��ע ����
        # ==========================================================
        cmds.separator(height=20, style='in')
        cmds.text(label="��è��������Ƥ", align='center')
        # ==========================================================


    def apply_group_id(self, *args):
        group_id = cmds.intFieldGrp(self.group_id_field, query=True, value1=True)
        self._add_attribute_logic(self.group_id_attr, group_id, "Group ID")

    def apply_guide_id(self, guide_id):
        type_str = "����" if guide_id == 1 else "��Ⱦ"
        self._add_attribute_logic(self.guide_attr, guide_id, f"{type_str}ë��")

    def _add_attribute_logic(self, attr_name, attr_value, ui_message_type):
        selection = cmds.ls(selection=True, long=True)
        if not selection:
            cmds.warning("û��ѡ���κ����壡����ѡ�����ߡ�")
            return
        curves_processed = 0
        all_shapes = []
        for obj in selection:
            if cmds.nodeType(obj) == 'transform':
                descendent_shapes = cmds.listRelatives(obj, allDescendents=True, type='nurbsCurve', fullPath=True) or []
                all_shapes.extend(descendent_shapes)
            elif cmds.nodeType(obj) == 'nurbsCurve':
                 all_shapes.append(obj)
        if not all_shapes:
            cmds.warning("�����ѡ����û���ҵ��κ����ߣ�")
            return
        for shape in set(all_shapes):
            if not cmds.attributeQuery(attr_name, node=shape, exists=True):
                cmds.addAttr(shape, longName=attr_name, attributeType='long', keyable=True)
            try:
                cmds.setAttr(f"{shape}.{attr_name}", attr_value)
                curves_processed += 1
            except Exception as e:
                print(f"�޷�Ϊ {shape} ��������: {e}")
        message = f"�ɹ�Ϊ {curves_processed} �����߱��Ϊ <hl>{ui_message_type}</hl> (ֵΪ {attr_value})��"
        if ui_message_type == "Group ID":
             message = f"�ɹ�Ϊ {curves_processed} ���������� <hl>{ui_message_type}</hl> Ϊ <hl>{attr_value}</hl>��"
        print(message.replace("<hl>","").replace("</hl>",""))
        cmds.inViewMessage(amg=message, pos='midCenter', fade=True)

# --- ���нű� ---
if __name__ == "__main__":
    CombinedGroomToolUI()