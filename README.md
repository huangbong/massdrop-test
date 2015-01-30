# massdrop-test

> Create a job queue whose workers fetch data from a URL and store the results in a database.  The job queue should expose a REST API for adding jobs and checking their status / results.

Here is my implimentation using Python.

This app uses Redis and the [rq](http://python-rq.org/) (Redis Queue), Flask, and Requests Python libraries. It stores the job queue objects in Redis and also stores the job results in Redis using the key rq:[id]:result.

## Dependencies

```
System requirements:

* python3
* python-pip
* redis

Install:

brew install python3 python-pip redis

sudo apt-get install python3 python-pip redis

Python module requirements:

* redis
* rq
* requests
* flask

Install:

pip install -r requirements.txt

You will need to use sudo if your python3 install base is in /usr/* or whatever.
```

## Running the app

Start Redis:

```
redis-server
```

Start a worker:

```
rqworker &
```

Start the app:

```
python3 app.py
```

If everything works out you should see the Flask respond:

```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Done! Now you can start playing with the app.

## Add a new URL fetch job

Example POST request:

```
curl -H "Content-Type: application/json" \
     -X POST \
     -d '{"url":"https://mitchellhuang.net/test.txt"}' \
     http://localhost:5000/api/new
```

Example reponse:

```
{
  "id": 1,
  "job_id": "60510cc9-f482-4e00-bc88-6985f3dac514"
}
```

## View the status of a job by job_id

Example GET request:

```
curl http://localhost:5000/api/status/60510cc9-f482-4e00-bc88-6985f3dac514
```

Example response:

```
{
  "job_id": "3f1290e2-af56-49e6-bc00-489870f42727",
  "status": "running"
}
```

## View the result of a job by id

```
curl http://localhost:5000/api/view/1
```

Example response:

```
{
  "id": 1,
  "result": "this is a test file\n",
  "status": "finished"
}
```