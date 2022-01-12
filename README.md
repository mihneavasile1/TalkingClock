# TalkingClock

### To set up the right permissions run: 
```
chmod +x scripts/init.sh
./scripts/init.sh
```

### To run the Talking Clock: Covers task one and two
```
./TalkingClock/TalkClock.py
```

#### You can pass an arbitrary numeric time parameter as input using the `-t` flag - e.g.:

```
./TalkingClock/TalkClock.py -t 13:42
```

#### If you want the friendly time to be returned as JSON simply set the `-j` flag:

```
./TalkingClock/TalkClock.py -t 13:42 -j on
```
or
```
./TalkingClock/TalkClock.py -j on
```

You can use any string other than the empty string to set the `-j` flag (e.g. `-j on`, `-j true`)

### To start the REST service run: Covers task three 

```
./TalkingClock/REST_service.py
```

This will start a server on `http://127.0.0.1:5000/`, so you can make requests such as:
```
 curl http://127.0.0.1:5000/
```

This will return something like:
```
{
    "Human Friendly Time": <Current time>
}
```


If you enounter `ModuleNotFoundError` run:
`export PYTHONPATH="${PYTHONPATH}:~/TalkingClockLloyds/TalkingClock/"`
