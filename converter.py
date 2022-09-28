import io
import sys
import pdfrw
from fastapi import FastAPI, UploadFile, Response

app = FastAPI()


@app.post('/remove_annotation')
async def remove_annotation_request(pdf_file: UploadFile):
    # use async here to prevent too high concurrency
    file_bytes = await pdf_file.read()
    print(f"[upload: {pdf_file.filename}], file size: {len(file_bytes) / 1000 / 1000:.2f}MB")
    in_memory_file = io.BytesIO(file_bytes)
    out_memory_file = io.BytesIO()
    remove_annotation(in_memory_file, out_memory_file)
    out_bytes = out_memory_file.getvalue()
    print(f"len of out: {len(out_bytes)}")
    return Response(out_bytes, media_type='application/pdf')


def remove_annotation(in_file, out_file):
    reader = pdfrw.PdfReader(in_file)
    for p in reader.pages:
        if p.Annots:
            # See PDF reference, Sec. 12.5.6 for all annotation types
            p.Annots = [a for a in p.Annots if a.Subtype == "/Link"]
    pdfrw.PdfWriter(out_file, trailer=reader).write()


def cli():
    in_path = sys.argv[1]
    out = sys.argv[2]
    remove_annotation(in_path, out)


if __name__ == '__main__':
    cli()
