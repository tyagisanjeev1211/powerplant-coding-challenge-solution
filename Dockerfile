FROM redhat/ubi8

LABEL "Developed by"="Sanjeev Tyagi"
LABEL "medium.com"="https://medium.com/@tyagisanjeev_1211"

RUN echo 'root:q48stG1a' |chpasswd

## RUN dnf upgrade
RUN dnf -y install python3.11
RUN dnf -y install python3.11-pip
RUN pip3 install fastapi
RUN pip3 install uvicorn            ## Web server 
RUN pip3 install aiofiles           ## Static file (javascript, css, media files 
RUN pip3 install python-multipart   ## multipart HTML form. Like file upload 

RUN useradd styagi
RUN echo 'styagi:docker123' | chpasswd

RUN mkdir -p /home/styagi/app
ADD project /home/styagi/app/
RUN chown -R styagi:styagi /home/styagi

EXPOSE 8888

USER styagi 

WORKDIR /home/styagi/app/src/

CMD nohup python3 main.py 