from flask import Flask
from flask import request
from jaeger_client import Config
import logging
from opentracing.ext import tags
from opentracing.propagation import Format

def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )
    # this call also sets opentracing.tracer
    return config.initialize_tracer()


app = Flask(__name__)
tracer = init_tracer('formatter') 
 
@app.route("/format")
def format():
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
    with tracer.start_active_span('format', child_of=span_ctx, tags=span_tags):
        hello_to = request.args.get('helloTo')
        return 'Hello, %s!' % hello_to

if __name__ == "__main__":
    app.run(port=8881)