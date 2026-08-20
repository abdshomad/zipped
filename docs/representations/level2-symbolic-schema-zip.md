# Representation Spec: Level 2 Symbolic Schema Zip

Level 2 compression eliminates structural token overhead (repeated field keys, curly braces, quotes, colons) in tabular JSON and AST payloads.

## Syntax
`§[key1,key2,key3] val1,val2,val3;val4,val5,val6`

## Example
### Input JSON:
```json
[
  {"id": 1, "name": "Alice", "role": "admin"},
  {"id": 2, "name": "Bob", "role": "user"}
]
```

### Compressed Representation:
`§[id,name,role] 1,Alice,admin;2,Bob,user`
