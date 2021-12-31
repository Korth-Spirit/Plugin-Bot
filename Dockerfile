# Copyright (c) 2021 Johnathan P. Irvin
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
FROM python:3.9 as RUN
WORKDIR /code

COPY run.py requirements.txt /code/
COPY src/ /code/src/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENTRYPOINT ["./run.py"]

FROM python:3.9 as TEST
WORKDIR /code

COPY run.py run_tests.py requirements.txt /code/
COPY src/ /code/src/
COPY tests/ /code/tests/

RUN pip install pytest coverage ; pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENTRYPOINT ["./run_tests.py"]