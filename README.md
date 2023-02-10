# xoa-regression-tests

## Install requirements before execute testing
```
pip install tox invoke
```

##  List available testing task
```
inv --list
```


> Available tasks:
>
>   git-china   execute testing with git-requires.txt and china tester
> git-demo    execute testing with git-requires.txt and demo tester
> pip-china   execute testing with pip-requires.txt and china tester
> pip-demo    execute testing with pip-requires.txt and demo tester

## Execute desire testing task
```
invoke pip-china
```

## Testing Result
>   pip-china-tester: OK (68.21=setup[0.02]+cmd[68.18] seconds)
> congratulations :) (68.24 seconds)

It might output alot of content on the console, you can just focus on the last two lines :D.


