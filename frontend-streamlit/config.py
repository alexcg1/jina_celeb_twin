# Absolute path prefix. This lets us copy workspaces between machines. So we can index on a fast machine and query from a slow one
# data_dir_root = "/mnt/data/work/repos/personal/jina_celeb_twin/backend/" # local
data_dir_root = "/home/ubuntu/alexcg/celeb_twin/backend/" # aws

image_endpoint = "http://0.0.0.0:54321/search"
# image_endpoint = "http://examples.jina.ai:54321/search"

top_k = 10

# 1 = totally different, 0 = totally identical. We want a cut-off to avoid getting really false/inappropriate matches
score_filter = 1
