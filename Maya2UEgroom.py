# -*- coding: utf-8 -*-

import maya.cmds as cmds

class CombinedGroomToolUI:
    """
    终极版二合一工具：Groom Alembic Prep Tool
    - 使用标签页 (Tabs) 来切换 "Group ID" 和 "Guide Tagger" 功能。
    - 提供了所有必要的功能来为UE的Groom系统准备Alembic属性。(已添加脚注)
    """
    
    def __init__(self):
        self.window_name = "CombinedGroomToolWindow"
        self.window_title = "《超高级导入UE的毛发处理插件》"
        
        self.group_id_attr = "groom_group_id"
        self.guide_attr = "groom_guide"
        
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name, window=True)
            
        self.window = cmds.window(
            self.window_name,
            title=self.window_title,
            widthHeight=(350, 450), # 调窗口
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
        """填充 'Group ID Tool' 标签页的UI元素。"""
        cmds.text(
            label="1. 选择毛发曲线或曲线组。\n2. 输入组ID (例如: 0, 1, 2...)\n3. 点击 'Apply' 按钮。",
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
        cmds.text(label="导出Alembic时, 复制下面的属性名:", align='left')
        cmds.textFieldGrp(
            label="Attribute Name:", text=self.group_id_attr, editable=False, columnWidth2=[80, 200]
        )
        
        # ==========================================================
        #  ★★★ 脚注 ★★★
        # ==========================================================
        cmds.separator(height=20, style='in')
        cmds.text(label="橘猫不吃橘子皮", align='center')
        # ==========================================================

    def populate_guide_tagger_tab(self):
        """填充 'Guide Tagger' 标签页的UI元素。"""
        cmds.text(
            label="1. 选择曲线 (渲染毛发或引导毛发)。\n2. 点击下面的对应按钮进行标记。",
            align='left'
        )
        cmds.separator(height=15, style='in')
        cmds.button(
            label="标记为: 渲染毛发 (guide=0)", command=lambda *args: self.apply_guide_id(0),
            height=40, backgroundColor=(0.2, 0.4, 0.6)
        )
        cmds.button(
            label="标记为: 引导毛发 (guide=1)", command=lambda *args: self.apply_guide_id(1),
            height=40, backgroundColor=(0.2, 0.7, 0)
        )
        cmds.separator(height=15, style='in')
        cmds.text(label="导出Alembic时, 记得添加下面的属性名:")
        cmds.textFieldGrp(
            label="Attribute Name:", text=self.guide_attr, editable=False, columnWidth2=[80, 200]
        )
        
        # ==========================================================
        #  ★★★ 脚注 ★★★
        # ==========================================================
        cmds.separator(height=20, style='in')
        cmds.text(label="橘猫不吃橘子皮", align='center')
        # ==========================================================


    def apply_group_id(self, *args):
        group_id = cmds.intFieldGrp(self.group_id_field, query=True, value1=True)
        self._add_attribute_logic(self.group_id_attr, group_id, "Group ID")

    def apply_guide_id(self, guide_id):
        type_str = "引导" if guide_id == 1 else "渲染"
        self._add_attribute_logic(self.guide_attr, guide_id, f"{type_str}毛发")

    def _add_attribute_logic(self, attr_name, attr_value, ui_message_type):
        selection = cmds.ls(selection=True, long=True)
        if not selection:
            cmds.warning("没有选中任何物体！请先选择曲线。")
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
            cmds.warning("在你的选择中没有找到任何曲线！")
            return
        for shape in set(all_shapes):
            if not cmds.attributeQuery(attr_name, node=shape, exists=True):
                cmds.addAttr(shape, longName=attr_name, attributeType='long', keyable=True)
            try:
                cmds.setAttr(f"{shape}.{attr_name}", attr_value)
                curves_processed += 1
            except Exception as e:
                print(f"无法为 {shape} 设置属性: {e}")
        message = f"成功为 {curves_processed} 条曲线标记为 <hl>{ui_message_type}</hl> (值为 {attr_value})。"
        if ui_message_type == "Group ID":
             message = f"成功为 {curves_processed} 条曲线设置 <hl>{ui_message_type}</hl> 为 <hl>{attr_value}</hl>。"
        print(message.replace("<hl>","").replace("</hl>",""))
        cmds.inViewMessage(amg=message, pos='midCenter', fade=True)

# --- 运行脚本 ---
if __name__ == "__main__":
    CombinedGroomToolUI()