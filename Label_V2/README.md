Pre:
1.主程序放置于labelme/main.exe中，解压Label_V2整个文件夹后，双击exe文件即可运行label程序。  
2.将标注的图片(.jpg/.png)放置于Picture_Data中，便于标注以及读取文件。  
Using： 
1.点击Open或Open Dir  (如需大量标记图片建议批量放在Picture_Data文件夹中 点击Open Dir)   
2.标注  
<img src="https://www.github.com/Damon2019/RM-DATASET/raw/master/images/20.png">  
1）可选择菜单栏Edit选择标注Rectangles(正矩形)，Polygons(斜矩形)，Points(点)  
2）或者可以使用快捷按键Rectangles(Ctrl+R)，Polygons (Ctrl+N)  

Rectangles：
<img src="https://www.github.com/Damon2019/RM-DATASET/raw/master/images/21.png">    
<img src="https://www.github.com/Damon2019/RM-DATASET/raw/master/images/22.png">    
点完第一个点松开鼠标滑动至令一标注边缘点击鼠标即可完成标注。
Polygons：  
<img src="https://www.github.com/Damon2019/RM-DATASET/raw/master/images/23.png">    
<img src="https://www.github.com/Damon2019/RM-DATASET/raw/master/images/24.png">    
标注顺序：永远先点击左上角为1，然后点击右上角为2，最后点击右下角为3（如上所示），程序会自动拟合出与之匹配的斜矩形。  
3.保存  
点击save或者(Ctrl+S)    
即可保存json标注文件。  

