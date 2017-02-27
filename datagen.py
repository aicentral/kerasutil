# from http://stackoverflow.com/questions/36986815/in-keras-model-fit-generator-method-what-is-the-generator-queue-controlled-pa
# another multi-generator https://gist.github.com/tdeboissiere/195dde7fddfcf622a82a895b90d2c800
import lmdb
import caffe
def gen():
	lmdb_env = lmdb.open('directory_containing_mdb')
	lmdb_txn = lmdb_env.begin()
	lmdb_cursor = lmdb_txn.cursor()
	datum = caffe.proto.caffe_pb2.Datum()

	for key, value in lmdb_cursor:
		datum.ParseFromString(value)
		label = datum.label
		data = caffe.io.datum_to_array(datum)
		for l, d in zip(label, data):
				yield d, y

def generator_queue(generator, max_q_size=10,
                    wait_time=0.05, nb_worker=1):
    '''Builds a threading queue out of a data generator.
    Used in `fit_generator`, `evaluate_generator`, `predict_generator`.
    '''
    q = queue.Queue()
    _stop = threading.Event()

    def data_generator_task():
        while not _stop.is_set():
            try:
                if q.qsize() < max_q_size:
                    try:
                        generator_output = next(generator)
                    except ValueError:
                        continue
                    q.put(generator_output)
                else:
                    time.sleep(wait_time)
            except Exception:
                _stop.set()
                raise

    generator_threads = [threading.Thread(target=data_generator_task)
                         for _ in range(nb_worker)]

    for thread in generator_threads:
        thread.daemon = True
        thread.start()

    return q, _stop