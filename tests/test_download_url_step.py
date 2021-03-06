import hashlib
import responses
from georef_ar_etl.extractors import DownloadURLStep
from georef_ar_etl.exceptions import ProcessException
from . import ETLTestCase


# pylint: disable=no-member
class TestDownloadURLStep(ETLTestCase):
    _uses_db = False

    @responses.activate
    def test_download(self):
        """El paso debería descargar un archivo remoto, y devolver la ruta
        local del mismo."""
        filename = 'file.txt'
        url = 'https://example.com/file.txt'
        body = 'foobar'

        responses.add(responses.GET, url, status=200, body=body, stream=True)
        step = DownloadURLStep(filename, url)
        path = step.run(None, self._ctx)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(path, filename)

        with self._ctx.fs.open(path) as f:
            contents = f.read()

        self.assertEqual(body, contents)

    @responses.activate
    def test_download_error(self):
        """El paso debería lanzar una excepción apropiada si falla la petición
        HTTP."""
        url = 'https://example.com/file.txt'

        responses.add(responses.GET, url, status=404)
        step = DownloadURLStep('foobar', url)

        with self.assertRaises(ProcessException):
            step.run(None, self._ctx)

    @responses.activate
    def test_download_hash(self):
        """El paso debería calcular el hash MD5 del archivo de descarga."""
        filename = 'file.txt'
        url = 'https://example.com/file.txt'
        body = 'testing de hash md5'

        responses.add(responses.GET, url, status=200, body=body, stream=True)
        DownloadURLStep(filename, url).run(None, self._ctx)

        md5 = hashlib.md5()
        md5.update(body.encode())

        report_data = self._ctx.report.get_data('download_url')
        self.assertEqual(report_data[url], md5.hexdigest())
