### How to get test result
write your nGQL in nGQL.txt file, then execute
```
python3 GetTestResult.py $your_1.0_graph_ip $your_1.0_graph_port
```

then the result will print such as

```
Cmd: GO FROM hash("Tim Duncan") OVER serve YIELD $^.player.name, serve.start_year, $$.team.name  UNION ALL  GO FROM hash("Tony Parker") OVER serve YIELD $^.player.name, serve.start_year, $$.team.name

Result: [["Tim Duncan", 1997, "Spurs"], ["Tony Parker", 1999, "Spurs"], ["Tony Parker", 2018, "Hornets"]]

Cmd: GO FROM hash("NON EXIST VERTEX ID") OVER serve YIELD serve.start_year, $$.team.name  UNION  GO FROM hash("NON EXIST VERTEX ID") OVER serve YIELD serve.start_year, $$.team.name  MINUS  GO FROM hash("NON EXIST VERTEX ID") OVER serve YIELD serve.start_year, $$.team.name  INTERSECT  GO FROM hash("NON EXIST VERTEX ID") OVER serve YIELD serve.start_year, $$.team.name

Result:

Cmd: GO FROM hash("Tim Duncan") OVER like YIELD like._dst AS id | GO FROM $-.id  OVER serve WHERE udf_is_in($-.id, -7579316172763586624, 123)

Result: [[Spurs], [Hornets]]

```
