from flask import Flask, Response, render_template, jsonify
import psutil, multiprocessing

app   = Flask(__name__)
procs = []

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
  return Response(status = 200)

@app.route('/stats')
def stats():
  cpu = psutil.cpu_percent()
  mem = psutil.virtual_memory().percent

  return jsonify({"mem": mem, "cpu": cpu})

@app.route('/startLoad', methods=['POST'])
def startLoad():
  if len(procs) > 0:
    return Response(status = 200, response="running")

  cpu_count = multiprocessing.cpu_count()
  for i in range(0,cpu_count):
    p = multiprocessing.Process(target=task, args=())
    p.start()
    procs.append(p)

  return Response(status = 200, response="started")

@app.route('/stopLoad', methods=['POST'])
def stopLoad():
  if len(procs) <= 0:
    return Response(status = 200, response="not running")

  for proc in procs:
    if proc != None:
        proc.terminate()
  
  procs.clear()

  return Response(status = 200, response="stopped")

def task():
  i = 2
  while True:
    i *= i



if __name__ == '__main__': 
  app.run(host='0.0.0.0', port=8080)