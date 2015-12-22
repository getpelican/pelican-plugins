# Just Table

Just table is a plugin for Pelican to create easily table. Before this plugin, you can create tables this way or maybe another way.
```
|   |   |   |   |   |
|---|---|---|---|---|
|   |   |   |   |   |
|   |   |   |   |   |
|   |   |   |   |   |
```
It looks easy, but sometimes you want to create basic table. Actually, I hate above way. Now, Just Table's way.

## Usage



*  Basic table



```
[jtable]
Year,Make,Model,Length
1994,Ford,E350,2.34
2000,Mercury,Cougar,2.38
[/jtable]
```



| Year |   Make  |  Model | Length |
|:----:|:-------:|:------:|:------:|
| 1994 |   Ford  |  E350  |  2.34  |
| 2000 | Mercury | Cougar |  2.38  |




*  More complicated


```
[jtable]
Year,Make,Model,Description,Price
1997,Ford,E350,ac,3000.00
1999,Chevy,Venture Extended Edition,,4900.00
1999,Chevy,Venture Extended Edition and Very Large,,5000.00
1996,Jeep,Grand Cherokee,MUST SELL!,4799.00
[/jtable]
```



| Year | Make  | Model                                       | Description   | Price   |
|------|-------|---------------------------------------------|---------------|---------|
| 1997 | Ford  | E350                                        | ac | 3000.00 |
| 1999 | Chevy | Venture Extended Edition                |               | 4900.00 |
| 1999 | Chevy | Venture Extended Edition and Very Large |               | 5000.00 |
| 1996 | Jeep  | Grand Cherokee                              | MUST SELL!    | 4799.00 |


*  Table with no heading



```
[jtable th="0"]
row1col1,row1col2,row1col3
row2col1,row2col2,row2col3
row3col1,row3col2,row3col3
[/jtable]
```



|  |  |  |
|----------|----------|----------|
| row1col1 | row1col2 | row1col3 |
| row2col1 | row2col2 | row2col3 |
| row3col1 | row3col2 | row3col3 |




*  Table with caption without heading



```
[jtable caption="This is caption" th="0"]
row1col1,row1col2,row1col3
row2col1,row2col2,row2col3
row3col1,row3col2,row3col3
[/jtable]
```


||This is caption ||
|----------|----------|----------|
| row1col1 | row1col2 | row1col3 |
| row2col1 | row2col2 | row2col3 |
| row3col1 | row3col2 | row3col3 |


or if you want heading and caption both , you can delete ```th="0"```


*  Table with auto index and It'll start from 1



```
[jtable ai="1"]
head1,head2,head3
row1col1,row1col2,row1col3
row2col1,row2col2,row2col3
row3col1,row3col2,row3col3
row4col1,row4col2,row4col3 
[/jtable]
```


| No. |   head1  |  head2 | head3 |
|:----:|:-------:|:------:|:------:|
| 1 |   row1col1  |  row1col2  |  row1col3  |
| 2 | row2col1 | row2col2 |  row2col3  |
| 3 | row3col1 | row3col2 |  row3col3  |
| 4 | row4col1 | row4col2 |  row4col3  |


### Installation

Add the plugin path to your PLUGINS setting in the pelicanconf.py file.



```PLUGINS = [... , 'just_table' , ... ]```


### Todo's

 - Read from CSV
 


### License
GPL