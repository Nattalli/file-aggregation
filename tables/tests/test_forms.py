import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from tables.forms import UploadFileForm


@pytest.mark.parametrize("file_name, content, content_type, is_valid", [
    ("test.csv", b"Advertiser,Brand,Start,End,Format,Platform,Impr\n", "text/csv", True),
    ("test.xls", b"Dummy XLS content", "application/vnd.ms-excel", True),
    ("test.xlsx", b"Dummy XLSX content", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", True),
    ("test.csv", b"", "text/csv", False)
])
def test_upload_file_form(file_name, content, content_type, is_valid):
    """
    Перевірка форми UploadFileForm з різними типами файлів.
    """
    file = SimpleUploadedFile(
        file_name,
        content,
        content_type=content_type
    )
    form = UploadFileForm(files={'file': file})

    assert form.is_valid() == is_valid
