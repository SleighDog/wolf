import pytest
from webtest.app import TestRequest
from wolf.http.datastructures import Query, Data, ContentType, Cookies
from wolf.wsgi.request import WSGIRequest


def test_request():
    environ = TestRequest.blank('/?key=1', method='GET').environ
    request = WSGIRequest(environ)
    assert isinstance(request, WSGIRequest)

    assert request.path == '/'
    assert request.method == 'GET'
    assert request.body.read() == b''
    assert request.query == Query({'key': ('1',)})
    assert request.root_path == ''
    assert request.cookies == Cookies('')
    assert request.content_type == ContentType('')
    assert request.data == Data()
    assert request.application_uri == 'http://localhost'
    assert request.uri() == 'http://localhost/?key%3D1'
    assert request.uri(include_query=False) == 'http://localhost/'


def test_request_immutability():
    environ = TestRequest.blank('/?key=1', method='GET').environ
    request = WSGIRequest(environ)
    assert request.path == '/'

    with pytest.raises(AttributeError):
        request.path = '/test'

    del request.path
    request.environ['PATH_INFO'] = '/test'
    assert request.path == '/test'
