### How to get test result
write your nGQL in nGQL.txt file, then execute
```
python3 GetTestResult.py $your_1.0_graph_ip $your_1.0_graph_port
```

then the succeeded result will print such as

```
Cmd: GO FROM hash("Tim Duncan") OVER serve YIELD $^.player.name, serve.start_year, $$.team.name  UNION ALL  GO FROM hash("Tony Parker") OVER serve YIELD $^.player.name, serve.start_year, $$.team.name

Result colNames: ["$^.player.name", "serve.start_year", "$$.team.name"]

Result data: [["Tim Duncan", 1997, "Spurs"], ["Tony Parker", 1999, "Spurs"], ["Tony Parker", 2018, "Hornets"]]

Cmd: GO FROM hash("NON EXIST VERTEX ID") OVER serve YIELD serve.start_year, $$.team.name  UNION  GO FROM hash("NON EXIST VERTEX ID") OVER serve YIELD serve.start_year, $$.team.name  MINUS  GO FROM hash("NON EXIST VERTEX ID") OVER serve YIELD serve.start_year, $$.team.name  INTERSECT  GO FROM hash("NON EXIST VERTEX ID") OVER serve YIELD serve.start_year, $$.team.name

Result colNames: ["serve.start_year", "$$.team.name"]

Result data:

Cmd: GO FROM hash("Boris Diaw") OVER serve WHERE udf_is_in($$.team.name, "Hawks", "Suns")  YIELD $^.player.name, serve.start_year, serve.end_year, $$.team.name

Result colNames: ["$^.player.name", "serve.start_year", "serve.end_year", "$$.team.name"]

Result data: [["Boris Diaw", 2005, 2008, "Suns"], ["Boris Diaw", 2003, 2005, "Hawks"]]

Cmd: GO FROM hash("Tim Duncan") OVER like YIELD like._dst AS id | GO FROM $-.id  OVER serve WHERE udf_is_in($-.id, -7579316172763586624, 123)

Result colNames: ["serve._dst"]

Result data: [["Spurs"], ["Hornets"]]

```

the failed result

```
Execute `GO FROM hash("Tim Duncan") OVER serve YIELD $^.player.name, serve.start_year, $$.team.name  UNION ALL  FROM hash("Tony Parker") OVER serve YIELD $^.player.name, serve.start_year, $$.team.name ' failed: error_msg: SyntaxError: syntax error near `FROM'

```
