FROM continuumio/miniconda3:latest

RUN apt-get update && \
    apt-get install -y cmake && \
    rm -rf /var/lib/apt/lists/*

COPY environment.yml .

RUN conda env create -f environment.yml && \
    conda clean -afy && \
    rm -rf /opt/conda/pkgs/*

ENV PATH /opt/conda/envs/hexwatershed/bin:$PATH

CMD ["/bin/bash"]
