FROM python:3.7

RUN apt-get update && apt-get install --no-install-recommends -y i2c-tools libi2c-dev libncurses5 libffi-dev gcc git 
RUN git clone https://github.com/DexterInd/RFR_Tools.git && cd RFR_Tools/miscellaneous/ && python3 setup.py install
RUN git clone https://github.com/DexterInd/GrovePi.git && cd GrovePi/Software/Python/ && pip install -r requirements.txt && python3 setup.py install
ADD requirements.txt  /requirements.txt
RUN pip install -r /requirements.txt
WORKDIR /code
CMD ["python" , "/code/collector.py"]
