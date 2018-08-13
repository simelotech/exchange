
"""Default test suite for the Skycoin Lykke integration.
"""

import docker, docker.errors
import logging
import os
import time
import uuid
import socket, errno
from tempfile import gettempdir

service_prefix = 'lykke_sky'
services_started = dict()

logging.basicConfig()
log = logging.getLogger(service_prefix)

TestSetupError = RuntimeError

def setup():
    """Setup integration tests
    """
    try:
        tmp = os.path.join(gettempdir(), '.{}'.format(hash(os.times())))
        os.makedirs(tmp)
        current_path = os.path.dirname(os.path.realpath(__file__))
        skycoin_params = "-enable-wallet-api=true"
        #skycoin_params += " -db-path=./data/.skycoin/data/skycoin/blockchain-180.db"
        skycoin_params += " -download-peerlist=false"
        skycoin_params += " -rpc-interface=true"
        #skycoin_params += " -db-read-only=true"
        skycoin_params += " -disable-networking=true"
        skycoin_params += " -data-dir=" + tmp
        skycoin_params += " -wallet-dir=" + tmp + "/wallets"
        skycoin_params += " -web-interface-port=6420"
        
        testservice_name = testrun_service_name()
        testsuite_id = str(uuid.uuid1()).replace('-', '')
        log.info('Starting test run %s' % (testservice_name,))
        services_started[testservice_name] = (testsuite_id, False)
        log.info('Initializing service : mongo')
        init_service('mongo',           '3.6.4-jessie', 27017)
        log.info('Initializing service : redis')
        init_service('redis',           '3.0.7-alpine', 6379)
        log.info('Initializing service : skycoin')
        init_service('skycoin/skycoin', 'develop',      6420, command=skycoin_params, 
            volumes={current_path: {'bind':'/data/.skycoin', 'mode' : 'rw'}})
        #init_service('skycoin/skycoin', 'develop',      6420, command=skycoin_params)
    except:
        log.error('Error found in test suite setup')
        raise
    finally:
        wait_for_all(services_started)

def teardown():
    """Unload launched services if no test suite is running.
    """
    testservice_name = testrun_service_name()
    log.info('Clean up after test run %s' % (testservice_name,))
    for service_id, (_, launched) in services_started.items():
        if service_id.startswith('_'.join((service_prefix, testrun_id()))) and launched:
            docker_dispose(service_id)
    del services_started[testservice_name]

def testrun_service_name():
    """Name to register this test run as a service.
    
    Depends on operating-system process ID.
    """
    return '%s_%d' % (service_prefix, os.getpid())

def testrun_id():
    """Global identifier of this test run.
    """
    return services_started[testrun_service_name()][0]

def init_service(service_name, version, default_port, command=None, volumes = None):
    """Ensure service is running. If not available run it with Docker.

    service_name : The name of the official Docker image used to run
                   the target service.
    default_port : Default service port. Usually matches the value
                   EXPOSE'd in Dockerfile.
    """
    try:
        port = int(os.getenv('PORT_' + service_name.upper(), default_port))
    except ValueError:
        port = default_port

    launched = False
    service_id = docker_service_name(service_name)
    if not is_listening_at(port):
        docker_run(service_name, tag=version,
                name=service_id ,
                ports={'%s/tcp' % (default_port,): port},
                command=command,
                volumes=volumes)
        launched = True
    services_started[service_id] = (port, launched)

def docker_service_name(service_name):
    """Name of the container running a service used by this test run, if any.
    """
    return '_'.join((service_prefix, testrun_id(), service_name.replace('/', '_')))

def docker_run(service_name, name, **docker_options):
    """Run service in a Docker container.
    """
    client = docker.from_env()

    image_tag = docker_options.get('tag', 'latest')
    volumes = docker_options.get('volumes', {})
#    try:
#        image = client.images.get(service_name)
#        log.info('Image %s:%s available locally' % (service_name, image_tag))
#    except:
#        log.warning('Image %s:%s not found locally ... pulling' % (service_name, image_tag))
#        client.images.pull(service_name, image_tag)
    client.containers.run('%s:%s' % (service_name, image_tag), detach=True, name=name,
            ports=docker_options.get('ports', dict()), command=docker_options.get('command'),
            volumes=volumes)
    time.sleep(1.0)

def docker_dispose(service_id):
    """Remove container used to run service
    """
    client = docker.from_env()
    log.debug('Stopping Docker container ... ' + service_id)
    container = client.containers.get(service_id)
    container.stop()
    container.wait()
    container.remove()

def wait_for_all(services_started, max_retries=5):
    """Wait for all services to be available.
    """
    log.info('Waiting for services started: %s',
            ', '.join(key
                for key, (_, launched) in services_started.items()
                if launched))
    step = max_retries
    pending = services_started.keys()
    timeout = 3.0
    time.sleep(timeout)
    # FIXME: Signal instead of busy wait
    while step > 0 and len(pending) > 0:
        time.sleep(timeout)
        pending = [(service_name, port)
                for service_name, (port, launched) in services_started.items()
                if launched and not is_listening_at(port)]
        timeout = 3
        step -= 1
    if len(pending) > 0:
        log.warning('Some services could not be started: %s',
                ', '.join('%s at %s' % entry for entry in pending))
        return False
    log.info('All services started')
    return True

def is_listening_at(port):
    """Check whether there's a service listening at given port.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            log.info("Listening ")
        else:
            # something else raised the socket.error exception
            print(e)
    s.close()


