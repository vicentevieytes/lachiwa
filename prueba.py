import datetime
from io import BytesIO
import random
import shutil
import tempfile
from zipfile import Path, ZipFile, ZipInfo


def zipinfo_contents_replace(
    zipfile: ZipFile, zipinfo: ZipInfo, search: str, replace: str
):
    """Given an entry in a zip file, extract the file and perform a search
    and replace on the contents. Returns the contents as a string."""
    dirname = tempfile.mkdtemp()
    fname = zipfile.extract(zipinfo, dirname)
    with open(fname, "r") as fd:
        contents = fd.read().replace(search, replace)
    shutil.rmtree(dirname)
    return contents


def format_time_for_doc(time):
    return time.strftime("%Y-%m-%d") + "T" + time.strftime("%H:%M:%S") + "Z"


MODE_DIRECTORY = 0x10


def make_canary_msexcel(url: str, template: Path):
    with open(template, "rb") as f:
        input_buf = BytesIO(f.read())
    output_buf = BytesIO()
    output_zip = ZipFile(output_buf, "w")
    now = datetime.datetime.now()
    now_ts = format_time_for_doc(now)
    created_ts = format_time_for_doc(
        now
        - datetime.timedelta(
            days=random.randint(1, 25),
            hours=random.randint(1, 24),
            seconds=random.randint(1, 60),
        )
    )
    with ZipFile(input_buf, "r") as doc:
        for entry in doc.filelist:
            if entry.external_attr & MODE_DIRECTORY:
                continue

            contents = zipinfo_contents_replace(
                zipfile=doc, zipinfo=entry, search="HONEYDROP_TOKEN_URL", replace=url
            )
            contents = contents.replace("aaaaaaaaaaaaaaaaaaaa", created_ts)
            contents = contents.replace("bbbbbbbbbbbbbbbbbbbb", now_ts)
            output_zip.writestr(entry, contents)
    output_zip.close()
    print("the output buffer is: ", output_buf.getvalue())
    return output_buf.getvalue()


if __name__ == "__main__":  # pragma: no cover
    make_canary_msexcel(
        "http://localhost:8351/?id=01J2JCWS970DQECKVWWQRDAG4P", "testdoc.zip")
