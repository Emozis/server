### Window

Drop and recreate tables

```
$env:DROP_TABLES="true"; $env:ENV="dev"; poetry run uvicorn app.main:app
```

```
$env:ENV="prod"; poetry run uvicorn app.main:app
```