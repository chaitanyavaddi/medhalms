import glob
import rcssmin
import rjsmin

for f in glob.glob('static/css/*.css'):
    with open(f, encoding='utf-8') as fh:
        content = fh.read()
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(rcssmin.cssmin(content))

for f in glob.glob('static/js/*.js'):
    with open(f, encoding='utf-8') as fh:
        content = fh.read()
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(rjsmin.jsmin(content))
