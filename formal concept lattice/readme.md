#### 0 作用

​	依据形式背景，输出经典概念格中的所有概念



#### 1 使用

​	使用 vscode 或 pycharm 等软件打开



#### 2 输入

​	创建一个大小为N*M的一个二维数组，内容为随机生成的0或1，其中1占50%

```python
	N = 5
    M = 5
    a = get_two_dimensional_array(N, M) 
```

​	修改N、M的值可控制二维数组大小

​	可以在**out_two_dimensional_array()** 中调整0.5的大小，控制形式背景中1和0的比例

```python
	if random() < 0.5
    	a[i][j] = 1
```

​	也可以选择手动输入，需注意：

```python
    #  ↓  注释这一行  ↓
    # a = get_two_dimensional_array(N, M)
    #  ↓  解除注释  ↓
     a = [[0, 1, 0, 1, 0, 0, 0],
          [0, 1, 1, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 0, 1],
          [1, 1, 0, 1, 1, 0, 0],
          [1, 1, 1, 0, 1, 1, 0],
          [1, 0, 1, 0, 0, 0, 1],
          [0, 0, 1, 0, 0, 0, 0]]
     N = len(a)
     M = len(a[0])
```

​	至于上面的N、M的第一次赋值，会被新的N、M覆盖，注释/不注释均可



#### 3 输出

​	使用：**out_concept_in_list** 输出序列list下的所有概念

```python
	out_concept_in_list(list)
```



​	