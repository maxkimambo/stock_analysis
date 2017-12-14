FROM maxkimambo/stock_analysis 

ADD . /home/ds/notebooks/app 
USER root
RUN pip install -r /home/ds/notebooks/app/requirements.txt
CMD python /home/ds/notebooks/app/import.py 
