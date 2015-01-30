#!/usr/bin/env python3

import redis
import rq
from flask import Flask, request, jsonify
from tasks import store_url_contents

app = Flask(__name__)

r = redis.Redis()

q = rq.Queue(connection=r)

@app.route('/api/new', methods=['POST'])
def new():
    """ Add a new job. {'url':<url>} parameter. """

    id = r.incr('id') # id increments (from 1) for every new job

    url = request.json['url']
    job = q.enqueue(store_url_contents, args=(id, url))

    return jsonify({'id': id, 'job_id': job.id})

@app.route('/api/status/<job_id>')
def status(job_id):
    """ View the status of a job by job_id. """

    try:
        job = rq.job.Job.fetch(job_id, connection=r)
    except rq.exceptions.NoSuchJobError:
        return jsonify({'job_id': job_id, 'status': 'does not exist'})

    if job.is_finished:
        status = 'finished'
    elif job.is_queued:
        status = 'in-queue'
    elif job.is_started:
        status = 'running'
    elif job.is_failed:
        status = 'failed'
        
    return jsonify({'job_id': job_id, 'status': status})

@app.route('/api/view/<int:id>')
def view(id):
    """ View the result of a job by id. """

    result = r.get('rq:%s:result' % id)
    if result != None:
        result = result.decode(encoding='UTF-8')
        return jsonify({'id': id, 'status': 'finished', 'result': result})

    return jsonify({'id': id, 'status': 'does not exist'})

if __name__ == '__main__':
    app.run(debug=True)

