# latticeBuild 简单介绍：

这是形式概念分析中计算概念的相关代码，各文件夹大致内容如下。

-----------------

**formal concept lattice** 经典概念格，采用渐进式构造，理论源自【概念格的渐进式构造与维护】（博士论文）；

**three-way concept lattice** 三支概念格，基于经典概念格的扩展，代码与经典基本一致；

**three value concept lattice** 三值概念格，与经典类似，只是多了一部分；

**object-oriented concept** 面向对象概念，应该是对的（吧；

**fuzzy concept lattice** 模糊概念格；

**approximate three-way concept lattice** 三支近似概念格，该模型来自于论文：【three-way concept analysis for incomplete formal contexts】；

**new approximate three-way concept lattice** 由我反向优化的三支近似概念格，尽管各项效果不如前面的三支近似概念模型，但，有总比没有强。



以上内容都是“对象导出”概念。相关代码仅计算概念，不建立格结构，即使声明【建立XX概念格】，也只是计算了所有的XX概念，并未建立Hasse图。