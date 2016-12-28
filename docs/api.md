# API for bovine-inventory

## Hosts

### List all

```
/api/host/list
```

Example results:

```json
{
  "hosts": [
    "host1",
    "host2",
    "host9",
    "host10"
  ]
}
```

### Search for specific host

```
/api/host/search?key=hostname
```

Example results:

```json
{
  "hosts": [
    "host1",
    "host10"
  ]
}
```

## Groups

List all:
```
/api/group/list
```

## Specify api version

Currently, only v2.0 of this api is available.  
As new versions come out, we will strive for backward compatibility, and will always "attempt" to support previous versions of the api. 

List all with api version:
```
/api/group/list?api_version=2.0
```
