from typing import Iterable
from sleigh.http.response import Response
from sleigh.wsgi.types import WSGIEnviron, StartResponse, Finisher


class WSGIResponse(Response[Finisher]):

    def close(self):
        """Exhaust the list of finishers. No error is handled here.
        An exception will cause the closing operation to fail during iteration.
        """
        if self._finishers:
            while self._finishers:
                finisher = self._finishers.popleft()
                finisher(self)

    def __call__(self, environ: WSGIEnviron,
                 start_response: StartResponse) -> Iterable[bytes]:
        status = f'{self.status.value} {self.status.phrase}'
        start_response(status, list(self.headers.items()))
        return self
