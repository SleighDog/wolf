from wolf.http.datastructures import Accept


def test_accept():
    accept = Accept.from_string(
        "text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8"
    )
    assert len(accept) == 4
    assert accept == (
        "text/html", "application/xhtml+xml", "application/xml", "*/*"
    )

    accept = Accept.from_string("text/*, text/html")
    assert len(accept) == 2
    assert accept == ("text/html", "text/*")

    accept = Accept.from_string(
        "application/json;q=0.8, text/html;q=0.7, text/*;q=0.5")
    assert accept.negociate(('application/json', 'text/html')) == (
        'application/json'
    )
    assert accept.negociate(('text/plain',)) == 'text/plain'
    assert accept.negociate(('image/jpg',)) is None
