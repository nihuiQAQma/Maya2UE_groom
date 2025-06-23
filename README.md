maya2025插件：

将maya的曲线转换成UE里面毛发分组的插件，可以将毛发拆解成不同的组来对单独的毛发进行管理，并且可以自己定义用于物理模拟的引导线，最后合并导出成一个完整的Groom毛发资产

重要的事说三遍：把代码复制到maya的脚本编辑器里面，然后运行（记得放到工具架留着下次用）！！！直接拖py文件用不了！！！

Maya 2025 Plugin:

A plugin that converts Maya curves into groom hair groups in Unreal Engine. It allows splitting hair into different groups for individual management, enables custom guide curves for physics simulation, and finally merges and exports them as a complete Groom hair asset.

Important! (x3):
Copy the code into Maya's Script Editor and run it (remember to save it to the shelf for future use)!!! Dragging the .py file directly won't work!!!



## Maya：

<img src="https://github.com/user-attachments/assets/aa4503dc-3c41-4220-9775-7153962af283" alt="画像" width="200px">
<img src="https://github.com/user-attachments/assets/288ed9e8-c6e9-4702-8cfd-177a94c70de7" alt="画像" width="200px">
</a>  

Maya大纲视图，名称和分组都随便你怎么搞，红色的框为毛发，绿色的为用于物理的引导线，蓝色为导入UE后决定分组，这块毛发是属于渲染体还是物理引导线

In Maya's Outliner, name and group them however you want - red boxes are for hair, green for physics guide curves, and blue determines grouping after importing to UE (whether this hair section belongs to renderable geometry or physics guides).

<img src="https://github.com/user-attachments/assets/883d24d3-4049-46c4-ac9a-75a6fe15dcbb" alt="画像" width="1000px">
</a>  

这些是物理引导线，右边的属性也是一样要加

These are physics guide curves, and the same attributes need to be added on the right side.

<img src="https://github.com/user-attachments/assets/161c6ee7-06be-4534-99e1-470566dac592" alt="画像" width="1000px">
</a>  

导出ABC格式的时候需要添加属性（可以直接复制我插件里面写的属性名，选中直接复制就行）

When exporting to ABC format, you need to add attributes (you can directly copy the attribute names from my plugin - just select and copy them).

<img src="https://github.com/user-attachments/assets/9cad8f59-83cb-4082-b3a7-4d69e83c81f7" alt="画像" width="1000px">
</a> 



## UE：

UE里面每个组都能单独调试其属性

Each group's properties can be individually adjusted in UE.

<img src="https://github.com/user-attachments/assets/e286ac5b-1aba-4bc2-8a14-9e421e839318" alt="画像" width="1000px">
</a>  

物理属性自然也可以，并且也可以对其分组进行查看和设置

Physical attributes can also be adjusted naturally, with per-group viewing and configuration capabilities.

<img src="https://github.com/user-attachments/assets/c32e04a6-7aa5-4b19-a3c5-0b807c275e9f" alt="画像" width="1000px">
</a>  
<img src="https://github.com/user-attachments/assets/b95d33a9-8d15-47d0-b335-90e4b4d00ef5" alt="画像" width="1000px">
</a>  

用于模拟物理的导线（那一块我不打算模拟，我少加了一块引导线，所以导致在UE里面后发那一块引导线是系统自己采样的显得比较多）

Guides for physics simulation (I didn't want to simulate that particular section, so I intentionally used fewer guide curves there. As a result, in UE the back hair area ended up with more system-generated sampled guides than desired)

![image](https://github.com/user-attachments/assets/87206976-324e-4b9b-8d13-d2b8b5030c8b)




