import pytest, os, shutil

@pytest.fixture(scope='function')
def tmp_dir():
    """ fixture that sets up and tears down a tmp directory for tests """
    # setup
    file_dir = os.path.dirname(os.path.realpath(__file__))
    tmp_dir = os.path.abspath(os.path.join(file_dir, 'tmp'))
    if not os.path.isdir(tmp_dir):
        os.makedirs(tmp_dir)

    yield tmp_dir

    # teardown
    shutil.rmtree(tmp_dir)
